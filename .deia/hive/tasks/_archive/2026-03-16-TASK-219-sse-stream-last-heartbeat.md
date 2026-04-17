# TASK-219: SSE Stream Include Last Heartbeat in Snapshot

## Objective
Update the SSE `/build/stream` snapshot event to include `last_heartbeat` field in task data so the frontend can use it for liveness checks.

## Context
After TASK-216, task entries have a `last_heartbeat` timestamp. The `/build/status` REST endpoint returns tasks with this field, but the SSE `snapshot` event must also include it so the frontend receives complete data.

The SSE stream sends a snapshot on connection via the `get_status()` method, which already returns task data. We need to ensure `last_heartbeat` is preserved in the task dict.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (lines 288-327: `get_status` method and lines 454-476: SSE stream handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (lines 154-169: task dict structure in `record_heartbeat`)

## Deliverables
- [ ] Verify that `get_status()` method returns `last_heartbeat` field in task dicts (it should, since it reads from `self.tasks`)
- [ ] If not present, add `last_heartbeat` to the task dict returned by `get_status()`
- [ ] Add integration test that verifies SSE snapshot contains `last_heartbeat` field
- [ ] Document the field in the `BuildStatusResponse` TypeScript interface (frontend test file)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - SSE snapshot includes `last_heartbeat` for tasks that have it
  - SSE snapshot handles tasks without `last_heartbeat` field (backward compat)
  - REST `/build/status` and SSE snapshot return identical task data structure
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_sse.py`
- [ ] Minimum 3 tests covering snapshot data completeness

## Constraints
- No file over 500 lines
- No stubs
- Preserve existing SSE keepalive and error handling
- Do NOT modify the heartbeat event structure (only snapshot)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-219-RESPONSE.md`

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
