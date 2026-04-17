# BRIEFING: Investigate 4 Persistently-Failing Escalated Specs

**From:** Q33NR
**Date:** 2026-04-16
**Model:** Sonnet
**Role:** Queen
**Mode:** INVESTIGATE + REPORT ONLY — NO CODE, NO ACTION

---

## Objective

Four specs in `.deia/hive/queue/_escalated/` repeatedly failed with empty
output. Triage daemon escalated each after 3+ requeue attempts. They all
exhibit the same failure signature: stacked "Clean Retry" headers
prepended to the spec, and no bee response file produced.

Investigate each spec. Identify the root cause of repeated empty-output
failures. Recommend a concrete path forward. **Do not act.** Do not
modify code. Do not modify queue state. Do not dispatch bees. Write a
single report file.

"Too big" is not an acceptable diagnosis — Q88N has explicitly rejected
it. Look for real causes: ambiguous requirements, missing dependencies,
dispatcher bugs, flow bugs in run_queue.py, prompt issues, tool
constraints, environmental problems.

---

## Specs Under Investigation

All in `.deia/hive/queue/_escalated/`:

1. **SPEC-BL-146-BOT-ACTIVITY-PORT.md**
   Port Bot Activity + Bot Settings UI. No commits matching BL-146,
   nothing in `_done/`, no response file.

2. **SPEC-MW-058-queue-data-connection.md**
   Fix queue pane showing "Waiting for data" on workdesk. MW-series
   migration work. No commits, no response.

3. **SPEC-TRIAGE-ESCALATED-001.md**
   Ironic: a spec to evaluate escalated queue items, itself stuck in
   the escalated queue. No commits, no response.

4. **SPEC-WIKI-108-egg-integration.md**
   P2 wiki egg-integration. No commits, no response.

---

## Context

- `_escalated/` sibling files were already audited and reconciled by
  Q33NR. 9 completed specs had their stale escalation copies removed.
  1 duplicate (`SPEC-EVENT-LEDGER-GAMIFICATION` — live in backlog/)
  and 1 superseded (`SPEC-WIKI-SURVEY-000` → WIKI-110) removed.
  These 4 are the genuine unfinished remainder.

- All 4 show the same failure pattern: repeated "Clean Retry" headers
  and empty bee output. Something is swallowing the bee run. Could
  be: spec content confusing the bee into giving up, dispatcher
  not capturing output correctly for these specs, pre-existing
  files the specs reference being missing post-flatten, or schema
  assumptions that no longer hold.

- Current repo post-flatten: `hivenode/`, `simdecisions/`,
  `browser/`, `_tools/`. No more `packages/`. Paths referenced in
  older specs may be stale.

- Triage daemon: `hivenode/scheduler/triage_daemon.py` moves specs
  to `_escalated/` after 3 requeue attempts with empty output.

- Queue runner: `.deia/hive/scripts/queue/run_queue.py` dispatches
  specs. `queue_runner.log` may hold hints.

---

## Files To Read First

- `.deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md`
- `.deia/hive/queue/_escalated/SPEC-MW-058-queue-data-connection.md`
- `.deia/hive/queue/_escalated/SPEC-TRIAGE-ESCALATED-001.md`
- `.deia/hive/queue/_escalated/SPEC-WIKI-108-egg-integration.md`
- `.deia/hive/queue/SUBMISSION-CHECKLIST.md` (spec format + gates)
- `hivenode/scheduler/triage_daemon.py` (escalation logic)
- `.deia/hive/scripts/queue/run_queue.py` (dispatch logic)
- `queue_runner.log` (recent activity)

---

## Deliverable

A single report file written to:

`.deia/hive/responses/2026-04-16-Q33N-ESCALATED-TRIAGE-REPORT.md`

Report must contain, for each of the 4 specs:

- **Summary** — one paragraph: what the spec wants, why it exists.
- **Failure Analysis** — why it likely failed. Be specific. Cite
  file paths, missing deps, ambiguous requirements, obsolete paths.
- **Recommendation** — concrete next action. Options include:
  - "Rewrite spec with X clarification, then move to backlog/"
  - "Split into N smaller specs: A, B, C"
  - "Superseded by commit X / spec Y — delete"
  - "Blocked on dependency Z — queue Z first"
  - "Dispatcher bug — file a spec to fix run_queue.py"
  - Others as warranted.
- **Confidence** — low / medium / high.

Plus an overall section:

- **Common Root Cause (if any)** — is there a shared pattern across
  these 4? Dispatcher bug? Pre-flatten path drift?
- **Systemic Recommendation** — what change would prevent this
  class of failure in the future?

---

## Constraints

- NO code changes.
- NO file moves in `.deia/hive/queue/`.
- NO dispatching bees.
- NO git writes.
- Do not run long test suites.
- Report file is the only deliverable.

---

## Response Requirements

Standard 8-section response format per BOOT.md, written to
`.deia/hive/responses/2026-04-16-Q33N-ESCALATED-TRIAGE-REPORT-RESPONSE.md`
IN ADDITION to the main report file.
