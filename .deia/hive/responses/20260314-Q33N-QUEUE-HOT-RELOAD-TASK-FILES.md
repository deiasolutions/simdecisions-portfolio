# Q33N Task Files: BL-121 Queue Hot-Reload

**Date:** 2026-03-14
**Spec:** BL-121 Queue Runner Hot-Reload
**Q33N Model:** Haiku

---

## Task Files Created

### TASK-075: Queue Runner Hot-Reload
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-14-TASK-075-queue-hot-reload.md`
**Model:** Haiku
**Objective:** Add hot-reload capability to run_queue.py to detect and process specs added during runtime

**Deliverables:**
- `_rescan_queue()` helper function to detect new specs
- Modify main loop to call rescan at top of each iteration
- Merge new specs into processing queue (priority-sorted)
- Log `QUEUE_HOT_RELOAD` event when new specs detected
- Budget tracking includes all specs (initial + hot-reloaded)
- All `print()` calls use `flush=True`

**Test Requirements:**
- 7 tests covering: new spec detection, duplicate filtering, priority ordering, empty rescan, budget continuity, event logging, multiple new specs
- Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue_hot_reload.py`

**Constraints:**
- No main loop restructure — add rescan at top of iteration
- Preserve existing archive behavior
- File stays under 500 lines
- No stubs

---

## Acceptance Criteria Mapping (Spec → Task)

| Spec Criterion | Task Deliverable |
|----------------|------------------|
| Each iteration re-scans queue directory | `_rescan_queue()` called at top of loop |
| New specs detected and processed | `_rescan_queue()` filters new specs, merges into list |
| Already-processed specs not re-processed | Filter by checking `specs` list + `_done/` + `_needs_review/` |
| Already-in-progress specs not re-dispatched | Filter by checking existing `specs` list |
| Session tracking distinguishes initial vs hot-reload | `QUEUE_HOT_RELOAD` event logged |
| Log message when new specs detected | `"[QUEUE] Hot-reload: found N new spec(s)"` with `flush=True` |
| Budget tracking works correctly | `session_cost` accumulates across all specs |
| 6+ tests | 7 tests specified |
| Use `flush=True` on print() | Explicit requirement in deliverables |

---

## Review Checklist

- [x] **Deliverables match spec** — All 9 acceptance criteria covered
- [x] **File paths are absolute** — All paths in task use full Windows paths
- [x] **Test requirements present** — 7 tests, scenarios specified, test file path provided
- [x] **CSS uses var(--sd-*)** — N/A (Python-only task)
- [x] **No file over 500 lines** — Current file 400 lines, constraint specified
- [x] **No stubs or TODOs** — "No stubs" explicitly required in constraints
- [x] **Response file template present** — 8-section template included

---

## Dependencies
None. This task is self-contained and modifies only `run_queue.py` and adds one new test file.

---

## Ready for Dispatch
**Status:** ✅ READY
**Recommended dispatch:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-TASK-075-queue-hot-reload.md --model haiku --role bee --inject-boot
```

---

## Notes for Q33NR
- Single task file (bee-sized unit of work)
- Spec model assignment is `haiku` — task uses haiku
- No breaking changes to existing queue behavior
- Backward-compatible (queue still works if no new specs added)
- Edge cases explicitly handled (empty rescan, duplicates, moved specs)
- Test coverage comprehensive (7 scenarios including budget tracking)
