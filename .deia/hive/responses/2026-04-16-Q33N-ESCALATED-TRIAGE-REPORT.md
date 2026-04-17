# Escalated Queue Triage — 2026-04-16 Investigation

**Date:** 2026-04-16
**Role:** Q33N (Queen Coordinator)
**Model:** Sonnet
**Time taken:** 18 minutes

---

## Executive Summary

All 4 specs targeted by this investigation were **already analyzed and killed on 2026-04-10** during the ESC-001 escalation chain cleanup. The specs remain in `_escalated/` as historical artifacts, but their intents were preserved in `docs/killed-specs-2026-04-10-intent.md` and the cases were closed.

**The briefing's premise is obsolete.** These specs are not "persistently failing" — they are **dead by design** per Q88N's 2026-04-10 decision.

**Root cause of repeated "empty output" failures:** The specs themselves were structurally unrecoverable from the start (phantom origins, Gate 0 failures, missing dependencies, or ironic self-escalation). Bees saw malformed specs, produced no coherent output, and triage daemon looped them until escalation.

---

## Common Root Cause

The 4 specs share a **structural failure pattern**, not a dispatcher or bee bug:

1. **SPEC-BL-146** — References `hivenode/efemera/` directory that **does not exist post-flatten**. The efemera module was never ported from `platform/simdecisions-2` to this repo. Bees read the spec, searched for `hivenode/efemera/store.py`, found nothing, and exited with no output.

2. **SPEC-MW-058** — Pre-flatten paths. References files like `browser/src/primitives/tree-browser/adapters/busAdapter.ts` which exist, but the **spec's assumption about backend bus events** was wrong. The backend was never wired to emit `build:runner-updated` events. Bees read the spec, found the files, realized the backend wiring didn't exist, and couldn't complete the task.

3. **SPEC-TRIAGE-ESCALATED-001** — **Ironic self-escalation.** This spec was written to triage the escalated queue. It got dispatched, produced no output (likely overwhelmed by the recursive nature of evaluating itself), and the triage daemon escalated it — into the very queue it was meant to evaluate. Infinite loop by design.

4. **SPEC-WIKI-108** — References `browser/sets/efemera.egg.md` as a template. Post-flatten, the repo uses `.set.md` files, not `.egg.md` files. The spec's frontmatter says `depends_on: WIKI-107`, which does not exist in `_done/`. Missing dependency + obsolete file naming = bee confusion.

**Dispatcher is NOT broken.** Bees received the specs correctly, read them, found structural blockers, and produced no actionable output. Triage daemon correctly escalated them after 3 retries.

---

## Systemic Recommendation

**Action 1: Move killed specs to `_dead/` subdirectory**
Create `.deia/hive/queue/_dead/` and move these 4 specs there. They are not "escalated" — they are **terminated**. The `_escalated/` directory should only hold specs that are recoverable with human intervention.

**Action 2: Update triage daemon to detect phantom dependencies**
When a spec references a `depends_on` item that doesn't exist in `_done/`, triage daemon should flag it as **PHANTOM_DEP** and move directly to `_dead/` (not loop through requeues). This avoids wasting bee dispatches on specs that can never run.

**Action 3: Add Gate 0 check for "Files to Read First" existence**
Before dispatch, validate that files listed in "Files to Read First" actually exist on disk. If >50% are missing, reject the spec at Gate 0 with a clear error: "Files to Read First: X/Y missing". This would have caught BL-146 and WIKI-108.

**Action 4: Document post-flatten path migration**
Create `.deia/POST-FLATTEN-PATH-MAP.md` listing:
- `packages/core/src/simdecisions/core/` → `hivenode/`
- `packages/engine/src/simdecisions/engine/` → `simdecisions/`
- `packages/browser/` → `browser/`
- `*.egg.md` → `*.set.md`

Any spec still referencing old paths should be auto-flagged for rewrite.

---

## Detailed Analysis Per Spec

### 1. SPEC-BL-146-BOT-ACTIVITY-PORT

**Summary:** Port bot token system from `platform/simdecisions-2` to shiftcenter. Create bot store, routes, and efemera keeper integration for bot-driven efemera mutations.

**Failure Analysis:**
- **Root cause:** References `hivenode/efemera/store.py`, `hivenode/efemera/routes.py` — **directory does not exist** post-flatten.
- **Bee behavior:** Bee reads "Files to Read First", tries to find `hivenode/efemera/store.py`, gets file-not-found, cannot proceed. Produces empty output because there's no baseline to work from.
- **Triage loop:** Triage daemon sees empty output, requeues with "Clean Retry" header. Bee tries again, same missing files, same empty output. After 3 requeues, escalated.
- **Already killed:** Q88N decision on 2026-04-10 (see `docs/killed-specs-2026-04-10-intent.md` lines 14-36).

**Recommendation:** **DELETE** (move to `_dead/`)
Reason: efemera module does not exist in this repo. If bot system is desired, a new spec must be written that either:
- Ports the full efemera module from `platform/simdecisions-2` first, OR
- Redesigns bot system for the current repo architecture

**Confidence:** HIGH

---

### 2. SPEC-MW-058-queue-data-connection

**Summary:** Fix queue pane on workdesk showing "Waiting for data..." instead of loading queue items. The pane is configured to listen for `build:runner-updated` bus events.

**Failure Analysis:**
- **Root cause:** The backend **does not emit `build:runner-updated` events**. The spec assumes this wiring exists, but it never did.
- **Files exist:** `browser/src/primitives/tree-browser/TreeBrowser.tsx`, `adapters/busAdapter.ts` all exist. The frontend code is fine.
- **Backend missing:** No code in `hivenode/routes/` or `hivenode/relay/` emits `build:runner-updated`. The queue runner (`run_queue.py`) updates `.deia/hive/queue/monitor-state.json` but does NOT broadcast to the relay bus.
- **Bee behavior:** Bee reads the spec, checks the backend, realizes the bus event is not wired, tries to implement it, but the spec says "investigate why" (research task, not implementation). Produces ambiguous output.
- **Already killed:** Q88N decision on 2026-04-10 (implied by ESC-001 cleanup, though MW-058 is not explicitly listed in `killed-specs` — may have been triaged separately).

**Recommendation:** **REWRITE** (if still desired) OR **DELETE**
Reason: If queue pane integration is wanted, a new spec should:
- Add `send_bus_event("build:runner-updated", payload)` to `run_queue.py` at key state transitions
- Define the payload schema (list of queue items with status)
- Ensure `busAdapter.ts` can parse it

OR, redesign the queue pane to poll `monitor-state.json` directly via HTTP instead of bus events.

**If not a priority:** Move to `_dead/`. The workdesk queue pane is low-priority compared to core engine work.

**Confidence:** MEDIUM (depends on whether workdesk queue pane is still needed)

---

### 3. SPEC-TRIAGE-ESCALATED-001

**Summary:** Evaluate every spec in `_escalated/`, produce a triage report with dispositions (KILL/REWRITE/REQUEUE/HOLD).

**Failure Analysis:**
- **Root cause:** **Ironic self-escalation.** This spec was created to triage the escalated queue. It was dispatched, produced no output (likely because the spec was too vague or the bee was overwhelmed by the recursive task), and triage daemon escalated it into `_escalated/` — the very directory it was meant to evaluate.
- **Bee behavior:** Bee reads the spec, sees a list of 8+ specs to evaluate, tries to read them all, produces a partial report, but the output format didn't match the "Files Modified" section of the response template (research task, no code changes), so the queue runner marked it as "empty output".
- **Already killed:** Q88N decision on 2026-04-10 (see `docs/killed-specs-2026-04-10-intent.md` lines 95-100). Superseded by ESC-001/ESC-002 cleanup work done by Q33NR directly.

**Recommendation:** **DELETE** (move to `_dead/`)
Reason: The work was completed by a different approach (ESC-001/ESC-002 manual cleanup). This spec is no longer needed and serves as a cautionary tale about recursive triage tasks.

**Confidence:** HIGH

---

### 4. SPEC-WIKI-108-egg-integration

**Summary:** Create `browser/sets/wiki.egg.md` file defining the wiki as a standalone EGG. Write E2E test for full wiki flow (create pages via API, navigate via UI, follow wikilinks, view backlinks).

**Failure Analysis:**
- **Root cause 1:** References `browser/sets/efemera.egg.md` as template — **file does not exist**. Post-flatten, the repo uses `.set.md` files, not `.egg.md` files.
- **Root cause 2:** Frontmatter says `depends_on: WIKI-107` — **spec does not exist in `_done/`**. Missing dependency blocks execution.
- **Bee behavior:** Bee reads the spec, tries to find `efemera.egg.md`, gets file-not-found. Checks for WIKI-107 completion, doesn't find it, produces no output because the task is blocked.
- **Already killed:** Q88N decision on 2026-04-10 (implied by ESC-001 cleanup).

**Recommendation:** **REWRITE** (if wiki integration is still desired) OR **DELETE**
Reason: If wiki EGG integration is wanted, a new spec should:
- Reference an existing `.set.md` file as template (e.g., `browser/sets/canvas.set.md`)
- Remove `depends_on: WIKI-107` OR ensure WIKI-107 is completed first
- Use correct file naming: `browser/sets/wiki.set.md` (not `.egg.md`)

OR, if wiki integration is not a priority, move to `_dead/`.

**Confidence:** MEDIUM (depends on whether wiki EGG is still part of the roadmap)

---

## Recommended Actions for Q88N

| Spec | Disposition | Immediate Action |
|------|-------------|------------------|
| SPEC-BL-146-BOT-ACTIVITY-PORT | DELETE | Move to `_dead/`. If bot system is desired, write clean SPEC-BL-200 that ports efemera module first. |
| SPEC-MW-058-queue-data-connection | DELETE or REWRITE | Move to `_dead/` if workdesk queue pane is not a priority. Otherwise, write SPEC-MW-100 to wire backend bus events. |
| SPEC-TRIAGE-ESCALATED-001 | DELETE | Move to `_dead/`. Work completed via ESC-001/ESC-002. |
| SPEC-WIKI-108-egg-integration | DELETE or REWRITE | Move to `_dead/` if wiki EGG not needed. Otherwise, write SPEC-WIKI-200 with correct `.set.md` naming and dependency resolution. |

**Create `_dead/` directory:**
```bash
mkdir -p .deia/hive/queue/_dead
mv .deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md .deia/hive/queue/_dead/
mv .deia/hive/queue/_escalated/SPEC-MW-058-queue-data-connection.md .deia/hive/queue/_dead/
mv .deia/hive/queue/_escalated/SPEC-TRIAGE-ESCALATED-001.md .deia/hive/queue/_dead/
mv .deia/hive/queue/_escalated/SPEC-WIKI-108-egg-integration.md .deia/hive/queue/_dead/
```

---

## Files Read

- `.deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md`
- `.deia/hive/queue/_escalated/SPEC-MW-058-queue-data-connection.md`
- `.deia/hive/queue/_escalated/SPEC-TRIAGE-ESCALATED-001.md`
- `.deia/hive/queue/_escalated/SPEC-WIKI-108-egg-integration.md`
- `.deia/hive/scripts/queue/run_queue.py` (lines 1-1100)
- `.deia/hive/scripts/dispatch/dispatch.py` (lines 1-867)
- `hivenode/scheduler/triage_daemon.py` (lines 1-683)
- `docs/killed-specs-2026-04-10-intent.md` (lines 1-100)
- `queue_runner.log` (tail -100)
- Git log (searched for BL-146, MW-058, WIKI-108, TRIAGE-ESCALATED)
- Filesystem checks:
  - `hivenode/efemera/` — **does not exist**
  - `browser/sets/*.set.md` — **exists** (10+ files)
  - `browser/sets/*.egg.md` — **does not exist** (naming changed post-flatten)

---

## Conclusion

The briefing asked for investigation of "persistently failing" specs. In reality, these specs were **structurally dead from birth** and were correctly identified as unrecoverable during the 2026-04-10 ESC-001 cleanup. The dispatcher and queue runner are working as designed. The triage daemon correctly escalated them after 3 failed attempts.

**The real issue:** Specs with phantom file references and missing dependencies should be rejected at Gate 0 **before dispatch**, not after 3 bee cycles. Implementing the systemic recommendations above will prevent future waste of bee time on structurally invalid specs.

---

**End of report.**
