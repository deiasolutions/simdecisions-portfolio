# TASK-BL203: Split Heartbeat into Liveness Ping + State Transition Log

## Objective
Split the build monitor heartbeat into two distinct signals: (1) a lightweight liveness ping sent frequently, and (2) state transition events emitted only when status actually changes.

## Context
Currently, the queue runner sends heartbeat signals that carry full state payloads on every ping, creating log noise and bandwidth waste. We need two separate channels:
- **Liveness ping**: Frequent (every 10-30s), lightweight (<100 bytes), just "I'm alive"
- **State transition log**: Only emitted when actual status changes occur (idle→building, building→done, etc.)

This aligns with SPEC-PIPELINE-001's monitoring requirements and reduces noise in build logs.

## Source Spec
From `.deia/hive/queue/_done/2026-03-17-SPEC-TASK-BL203-split-heartbeat.md`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_integration.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`

## Files You May Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (add liveness endpoint, modify heartbeat logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (send both signal types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_integration.py` (add tests for both signals)

## Files You Must NOT Modify
- Any files in `browser/` directory
- Any files in `engine/` directory
- Any other route files in `hivenode/routes/` besides `build_monitor.py`
- Any queue scripts besides `run_queue.py`
- Database schema files

## Deliverables
- [ ] Add `POST /build/ping` endpoint to `build_monitor.py`
  - Accepts minimal payload (just timestamp, no state)
  - Returns 200 OK with lightweight response
  - Response payload < 100 bytes
- [ ] Modify existing heartbeat logic to only emit state transitions
  - Track last known state
  - Only emit event when state actually changes
  - Include old_state and new_state in transition events
- [ ] Update `run_queue.py` to send both signal types:
  - Liveness ping every 30s (configurable)
  - State transition only when status changes
- [ ] Add tests in `test_build_monitor_integration.py`:
  - Test liveness ping endpoint (lightweight response)
  - Test state transition only fires on actual change
  - Test multiple pings without state change don't create duplicate transitions
  - Test state change does create transition event
  - Minimum 5 new tests

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass
- [ ] New tests cover:
  - Liveness ping response size < 100 bytes
  - State transitions only on actual changes
  - No duplicate transitions on repeated heartbeats
  - Both old_state and new_state in transition events
  - Edge case: first heartbeat (no previous state)

## Constraints
- No file over 500 lines (if build_monitor.py approaches 500 lines, refactor into modules)
- No stubs — full implementation
- No hardcoded colors (N/A for backend)
- All absolute paths in docs

## Acceptance Criteria
- [ ] Liveness ping endpoint exists at `POST /build/ping`
- [ ] Liveness ping response < 100 bytes
- [ ] State transitions only fire on actual status changes
- [ ] Transition events include old_state and new_state fields
- [ ] Queue runner sends both signal types appropriately
- [ ] All tests pass: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/routes/test_build_monitor_integration.py -v`
- [ ] No regressions in other build_monitor tests

## Model Assignment
haiku

## Priority
P0

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BL203-RESPONSE.md`

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
