# TASK-SYNC-AUTOSTART-D: Verify Graceful Shutdown + Add Test

## Objective

Verify that sync worker stops gracefully on hivenode shutdown and add an integration test to prove no orphan sync processes remain.

## Context

`main.py` already has cleanup logic in the lifespan context manager (lines 256-260):
```python
# Cleanup
if periodic_worker:
    await periodic_worker.stop()
if file_watcher:
    file_watcher.stop()
```

`PeriodicSyncWorker.stop()` (lines 62-76 of worker.py):
- Sets `_stopped = True`
- Cancels the background task
- Waits for task to complete (with CancelledError handling)
- Sets `_task = None`

**This looks correct**, but there's no test proving it works end-to-end.

**What needs verification**:
1. PeriodicSyncWorker stops within 3 seconds of hivenode shutdown
2. No orphan asyncio tasks remain after shutdown
3. No sync operations continue after stop() is called
4. FileWatcher stops cleanly (if running)

**Test scenario**:
- Start hivenode with sync enabled
- Wait for at least one sync cycle to complete
- Trigger shutdown (call lifespan shutdown)
- Verify:
  - PeriodicSyncWorker._task is None after shutdown
  - No pending asyncio tasks for sync worker
  - FileWatcher thread is stopped (if was running)
  - No exceptions raised during shutdown

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 256-275)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (lines 62-76)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\watcher.py` (stop() method)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_worker.py` (lines 136-167)

## Deliverables

- [ ] Add integration test: `test_graceful_shutdown_sync_worker()`
- [ ] Test starts PeriodicSyncWorker, waits for 1 cycle, calls stop(), verifies clean shutdown
- [ ] Test verifies `worker._task is None` after stop()
- [ ] Test verifies no pending asyncio tasks for sync worker
- [ ] Test verifies shutdown completes within 3 seconds
- [ ] (Optional) If shutdown logic needs fixes, fix them — but current code looks correct

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Shutdown during active sync cycle → sync completes or cancels cleanly
  - Shutdown before any sync cycle → worker stops immediately
  - Shutdown with FileWatcher running → both stop cleanly
  - Double shutdown (stop called twice) → no error, idempotent

## Constraints

- No file over 500 lines
- TDD
- Python 3.13
- Test must run in < 5 seconds
- Use `asyncio.wait_for()` to enforce timeout
- Shutdown must complete within 3 seconds (configurable in test)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-SYNC-AUTOSTART-D-RESPONSE.md`

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
