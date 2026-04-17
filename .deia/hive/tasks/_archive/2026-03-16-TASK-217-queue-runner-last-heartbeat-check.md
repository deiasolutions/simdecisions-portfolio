# TASK-217: Queue Runner Last Heartbeat Liveness Check

## Objective
Update queue runner liveness detection to use `last_heartbeat` timestamp instead of `last_seen`, now that `last_seen` only updates on state transitions.

## Context
After TASK-216, `last_seen` in task entries only updates on state transitions (status changes, new messages). Liveness detection needs a timestamp that updates on EVERY heartbeat. We're adding `last_heartbeat` field for this purpose.

The dispatch handler's `_is_heartbeat_stale()` method currently checks `last_seen` from the `/build/status` API. It should now check `last_heartbeat` instead.

Dead bee detection: if `now - last_heartbeat > 900s` (15 minutes), bee is considered dead (matches current WATCHDOG_STALE_SECONDS).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` (lines 192-208: `_is_heartbeat_stale` method)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (to understand new `last_heartbeat` field from TASK-216)

## Deliverables
- [ ] Modify `dispatch_handler.py::_is_heartbeat_stale()` to check `last_heartbeat` instead of `last_seen`
- [ ] Preserve existing timeout behavior (900 seconds = 15 minutes)
- [ ] Handle case where `last_heartbeat` field doesn't exist (backward compatibility with old monitor state)
- [ ] Add comment explaining the distinction between `last_heartbeat` (liveness) and `last_seen` (state transitions)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Fresh heartbeat (within 15 min) → bee is alive
  - Stale heartbeat (> 15 min) → bee is dead
  - Task with no `last_heartbeat` field (old monitor state) → fall back to `last_seen`
  - Task not found in monitor → not stale (hasn't started)
  - Monitor API unreachable → not stale (don't kill on monitor failure)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\_tools\test_dispatch_handler_liveness.py`
- [ ] Minimum 5 tests covering all edge cases above

## Constraints
- No file over 500 lines
- No stubs
- Preserve existing error handling (don't kill on monitor failure)
- Maintain 900-second timeout constant

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-217-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
