# TASK-216: Heartbeat State Transition Detection Logic

## Objective
Implement state transition detection logic in build monitor heartbeat handler to distinguish silent pings from logged events.

## Context
Currently every heartbeat appends to the `log[]` array in monitor-state.json, causing file bloat (17K+ lines of repeated "running" entries). We need to separate liveness pings (update timestamp only) from state transitions (append to log).

A heartbeat is a **STATE TRANSITION** (should be logged) if:
1. The task's status changed (e.g. dispatched → running), OR
2. The heartbeat contains a message that differs from the last logged message for that task, AND the message is not "Processing..."

Otherwise it's a **SILENT PING** — just update `last_heartbeat` timestamp on the task entry.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (lines 118-218: `record_heartbeat` method)

## Deliverables
- [ ] Add `last_heartbeat` field to task entries (ISO timestamp string)
- [ ] Add `last_logged_message` field to task entries (optional string)
- [ ] Implement `_is_state_transition()` helper method in `BuildState` class
- [ ] Modify `record_heartbeat()` to:
  - ALWAYS update `tasks[task_id].last_heartbeat` on every heartbeat
  - ONLY append to `log[]` when `_is_state_transition()` returns True
  - Update `last_logged_message` when appending to log
- [ ] Preserve existing separator logic and SSE broadcast behavior
- [ ] Update `_save_to_disk()` to persist `last_heartbeat` and `last_logged_message` fields

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Status change (dispatched → running) → appends to log
  - Same status, same message → no log append, updates last_heartbeat
  - Same status, new message (not "Processing...") → appends to log
  - Same status, "Processing..." message → no log append
  - New task (first heartbeat) → appends to log
  - Repeated "running" status with no message → no log append
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_state_transition.py`
- [ ] Minimum 8 tests covering all edge cases above

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (N/A for this task)
- No stubs
- Do NOT modify SSE stream logic or claim system
- Preserve all existing fields in task entries and log entries
- Backward compatible with existing monitor-state.json files

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-216-RESPONSE.md`

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
