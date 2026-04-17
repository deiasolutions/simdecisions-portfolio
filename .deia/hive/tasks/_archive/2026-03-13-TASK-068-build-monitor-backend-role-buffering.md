# TASK-068: Build Monitor Backend — Role Labels + Python Buffering

## Objective
Add `role` field to heartbeat schema and fix Python stdout buffering in queue runner scripts.

## Context
The build monitor tracks dispatch processes via heartbeat POSTs to `/build/heartbeat`. Currently, heartbeats don't include role information (bee, queen, queue runner), making it hard to distinguish task types in the UI.

Additionally, Python's stdout buffering delays print() output, causing monitor UI to lag behind actual queue runner state.

This task fixes both issues:
- Add optional `role` field to HeartbeatPayload
- Update send_heartbeat() in dispatch.py to include role
- Update queue runner scripts to send role="QR" for queue-level events
- Add flush=True to all print() calls in run_queue.py, spec_processor.py, dispatch_handler.py

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — HeartbeatPayload schema, BuildState
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — send_heartbeat function
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue runner main loop
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` — process_spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — watchdog, call_dispatch

## Deliverables

### Backend Schema Changes
- [ ] Add `role: Optional[str]` field to HeartbeatPayload in build_monitor.py
- [ ] Update BuildState.record_heartbeat() to store role in task state
- [ ] Update BuildState task dict to include `role` field

### Dispatch Script Updates
- [ ] Update send_heartbeat() signature in dispatch.py to accept `role` parameter
- [ ] Update dispatch_bee() in dispatch.py to pass role="B" for bee dispatches
- [ ] Update dispatch_bee() to pass role="Q" for queen dispatches
- [ ] Update initial "dispatched" heartbeat to include role

### Queue Runner Role Labels
- [ ] Update run_queue.py to import send_heartbeat (or create local wrapper)
- [ ] Queue-level events (wave_start, wave_end, budget warnings) send heartbeats with role="QR"
- [ ] Use task_id="queue-runner" for queue-level heartbeats

### Python Buffering Fix
- [ ] All print() calls in run_queue.py use flush=True
- [ ] All print() calls in spec_processor.py use flush=True
- [ ] All print() calls in dispatch_handler.py use flush=True

## Test Requirements

### Test File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_build_monitor.py`
Add test cases:
- [ ] `test_heartbeat_with_role_storage` — POST heartbeat with role="B", verify it's stored in task state
- [ ] `test_heartbeat_without_role` — POST heartbeat with no role (legacy), verify it still works
- [ ] `test_role_passthrough_in_status` — POST heartbeat with role="Q", GET /build/status, verify role appears in task object

### Manual Verification
- [ ] Run queue with 1 spec, verify stdout prints appear immediately (no buffering lag)
- [ ] Check build monitor receives role field in heartbeat messages

### Edge Cases
- [ ] Legacy heartbeats (no role field) don't break BuildState
- [ ] Role field is optional in HeartbeatPayload schema
- [ ] Role is None/null when not provided

## Constraints
- **No file over 500 lines** — modularize if needed
- **CSS: var(--sd-*) only** — not applicable (backend only)
- **No stubs** — all functions fully implemented
- **Do NOT break existing heartbeat API** — add role as optional field only
- **flush=True is a mechanical find-and-replace** — do not refactor print statements

## Acceptance Criteria

### Fix 1: Role labels in heartbeat messages
- [ ] `send_heartbeat()` in dispatch.py includes a `role` field: "Q" (queen), "B" (bee), or "QR" (queue runner)
- [ ] `HeartbeatPayload` in build_monitor.py gets `role: Optional[str]` field
- [ ] dispatch.py: pass role="B" for bee dispatches, role="Q" for queen dispatches
- [ ] run_queue.py: send heartbeats with role="QR" for queue-level events (wave_start, wave_end, budget warnings)
- [ ] Test: heartbeat with role="B" stores role in task state

### Fix 5: Python stdout buffering fix
- [ ] All `print()` calls in `run_queue.py` use `flush=True`
- [ ] All `print()` calls in `spec_processor.py` use `flush=True`
- [ ] All `print()` calls in `dispatch_handler.py` use `flush=True`
- [ ] Test: not needed, this is a one-liner fix per print call

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-068-RESPONSE.md`

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

## Model Assignment
haiku

## Test Commands
```bash
# Python backend tests
cd hivenode && python -m pytest tests/hivenode/test_build_monitor.py -v

# Queue runner tests (verify no regressions)
cd .deia/hive/scripts/queue && python -m pytest tests/ -v
```
