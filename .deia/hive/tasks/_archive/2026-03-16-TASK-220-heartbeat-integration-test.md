# TASK-220: Heartbeat Split Integration Test

## Objective
Write end-to-end integration test that verifies the complete heartbeat split behavior: silent pings update timestamp but don't grow log, state transitions append to log.

## Context
This is the final integration test to verify all pieces work together:
- TASK-216: Backend state transition detection
- TASK-217: Queue runner liveness check
- TASK-218: Frontend freshness filtering
- TASK-219: SSE snapshot includes `last_heartbeat`

The integration test should simulate a realistic bee lifecycle and verify:
1. Repeated "running" heartbeats don't bloat the log
2. State transitions (dispatched → running, new messages) do get logged
3. Liveness detection works correctly
4. Frontend receives correct data

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (complete module)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (existing E2E test patterns)

## Deliverables
- [ ] E2E test that:
  - POSTs initial "dispatched" heartbeat → verify log has 1 entry
  - POSTs "running" heartbeat → verify log has 2 entries
  - POSTs 5 more "running" heartbeats with no message → verify log still has 2 entries
  - POSTs "running" heartbeat with new message "Tests: 12/12 passed" → verify log has 3 entries
  - POSTs 3 more "running" heartbeats with same message → verify log still has 3 entries
  - POSTs "complete" heartbeat → verify log has 4 entries
  - Verifies `last_heartbeat` timestamp advanced on every POST
  - Verifies `last_seen` timestamp only advanced on logged events
- [ ] Test verifies `/build/status` REST endpoint returns correct task data
- [ ] Test verifies task entry has correct `last_heartbeat`, `last_seen`, and `last_logged_message` values
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_integration.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Single comprehensive E2E test covering the full lifecycle
- [ ] Test uses real HTTP requests via TestClient (FastAPI pattern)
- [ ] Test verifies exact log entry counts at each step
- [ ] Test verifies timestamp updates (not exact values, just that they advanced)

## Constraints
- No file over 500 lines
- No stubs
- Use FastAPI TestClient for HTTP requests
- Do NOT start a real server subprocess (use TestClient)
- Clean up monitor state between test runs (fresh BuildState instance)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-220-RESPONSE.md`

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
