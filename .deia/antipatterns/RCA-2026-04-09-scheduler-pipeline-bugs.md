# RCA: Scheduler Pipeline — Three Cascading Bugs

**Date:** 2026-04-09
**Duration of impact:** ~6 hours (factory build stalled)
**Fixed by:** Q33N debug dispatch + manual fixes

---

## Summary

The scheduler/dispatcher/queue-runner pipeline had three independent bugs that combined to prevent any FACTORY specs from being dispatched. The entire factory build sat idle while the scheduler reported all tasks as "blocked" or "unknown."

---

## Bug 1: Task ID Collision in `_done/`

**Root cause:** Old FACTORY-001 through FACTORY-009 specs from a previous build iteration (different objectives, different content) remained in `queue/_done/`. New FACTORY-001 through FACTORY-009 specs in `queue/backlog/` had the same task IDs. The scheduler's `compute_schedule()` saw the old `_done/` files and marked the new backlog specs as already completed — skipping them entirely.

**Symptom:** Schedule showed only 2 tasks instead of 14+. Most FACTORY specs were invisible.

**Fix:** Archived old specs to `_done/_archive_old_factory/`. Scheduler immediately saw the new specs.

**Antipattern:** Reusing task ID ranges across build iterations without clearing `_done/`.

**Prevention:** Either namespace task IDs by build iteration (e.g., `FACTORY-V2-001`) or archive `_done/` before starting a new build with overlapping IDs.

---

## Bug 2: Dependency String Mismatch in Dispatcher

**Root cause:** Specs list deps with parenthetical explanations, e.g.:
```
- SPEC-FACTORY-006 (backend `/factory/responses` endpoint)
```
The dispatcher's `_verify_deps_satisfied()` compared the full string against `done_ids` which only contained bare IDs like `FACTORY-006`. The parenthetical description caused every comparison to fail.

**Symptom:** Tasks showed deps as unsatisfied even when the dep specs were in `_done/`.

**Fix:** Rewrote `_norm()` in `dispatcher_daemon.py` to strip parenthetical descriptions and extract just the task ID using digit-based parsing (matching the spec_parser's existing logic).

**File:** `hivenode/scheduler/dispatcher_daemon.py` — `_norm()` function

**Prevention:** Normalize dep strings at parse time, not at comparison time. The spec_parser already does this for body-parsed specs; the dispatcher was using a simpler normalizer that didn't handle it.

---

## Bug 3: Task ID Extraction Inconsistency in Scheduler

**Root cause:** Two different functions extracted task IDs from spec filenames:
- `extract_task_id()` — sophisticated, digit-based, produces 3-part IDs (e.g., `MW-VERIFY-001`)
- `_extract_task_id_from_spec()` — simple 2-part split, produces 2-part IDs (e.g., `MW-VERIFY`)

The scheduler used `extract_task_id()` for backlog scanning but `_extract_task_id_from_spec()` for building done/active sets. The ID mismatch meant `task.id in backlog_specs` always failed for multi-part IDs, causing tasks to fall through to stale `dispatched.jsonl` entries with "unknown" status.

**Symptom:** Tasks showed status "unknown" instead of "ready" even with zero deps.

**Fix:** Aligned `_extract_task_id_from_spec()` with `extract_task_id()` — both now use digit-based extraction (take parts up to and including first part containing digits).

**File:** `hivenode/scheduler/scheduler_daemon.py` — `_extract_task_id_from_spec()` function

**Prevention:** Single source of truth for ID extraction. Should be ONE function called from everywhere, not two functions with subtly different logic.

---

## Bug 4: Freetext Dependencies (ongoing)

**Root cause:** Specs list freetext descriptions in `## Depends On` instead of `SPEC-*` IDs:
```
## Depends On
- Gate enforcer bus events (already exist)
- P0 complete
- Existing voice hook
```

The scheduler resolves deps by matching against `SPEC-*.md` filenames in `_done/`. Freetext strings never match, so these tasks are permanently blocked — even when the referenced code already exists on disk.

**Symptom:** FACTORY-004 sat blocked for the entire build. FACTORY-101, 103, 104 remain blocked by freetext deps.

**Fix (FACTORY-004):** Changed `## Depends On` to `None`. Documented as `ANTIPATTERN-AP-SPEC-002`.

**Remaining:** FACTORY-101 (`P0 complete`, `MCP tools already exist`), FACTORY-103 (`Existing voice hook`), FACTORY-104 (`Existing diff-viewer primitive`, `per survey)`)

**Prevention:**
- Only `SPEC-*` IDs in `## Depends On`
- Already-built code goes under `## Reference Files`
- Add GATE0 validation: reject specs with non-SPEC deps

---

## Timeline

| Time | Event |
|------|-------|
| ~12:00 | Factory specs submitted to backlog |
| 12:00–16:00 | Scheduler reports all tasks "blocked" — zero dispatches |
| 16:13 | Dispatcher daemon restarted, still no dispatches |
| ~16:30 | Q33N dispatched to debug scheduler |
| ~16:45 | Bug 1 found (ID collision), old specs archived |
| ~16:50 | FACTORY-002, 003, 005, 006, 007, 009 dispatched — Wave 1 running |
| ~17:00 | Bug 2 found (dep string mismatch), `_norm()` fixed |
| ~17:05 | Bug 3 found (ID extraction), `_extract_task_id_from_spec()` aligned |
| ~17:15 | Bug 4 found (freetext dep), FACTORY-004 unblocked |
| 17:20 | FACTORY-004 dispatched to `_active/` |

---

## Lessons

1. **One ID extractor, not two.** If you need a task ID from a filename, call the same function everywhere.
2. **Normalize at parse time.** Don't carry raw user strings through the pipeline and normalize at comparison time — normalize once, early.
3. **Freetext deps are invisible blockers.** The scheduler can't resolve them, won't warn about them, and the task sits silently blocked forever.
4. **Archive `_done/` between build iterations.** Task ID collisions are silent — the scheduler just skips your new specs.
5. **The rejection loop bug** (WIKI-SURVEY-000) shows that error handling paths need idempotency too — a rejected spec that gets re-queued and re-rejected should not spawn infinite `.rejection.rejection.rejection` files.
