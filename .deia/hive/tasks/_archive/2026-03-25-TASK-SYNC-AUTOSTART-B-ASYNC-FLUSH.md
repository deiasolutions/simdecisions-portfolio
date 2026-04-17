# TASK-SYNC-AUTOSTART-B: Make SyncQueue.flush() Async

## Objective

Convert `SyncQueue.flush()` from synchronous to asynchronous to match how `PeriodicSyncWorker` calls it (with `await`).

## Context

**Current issue**:
- `PeriodicSyncWorker._run()` calls `await self.sync_queue.flush(target_adapter)` (line 101 of worker.py)
- BUT `SyncQueue.flush()` is defined as synchronous (line 78 of sync_queue.py: `def flush(...)`)
- This works in Python because `await` on a non-coroutine just returns the value, but it's semantically incorrect and causes type checker warnings

**Why it should be async**:
- `CloudAdapter.write()` is synchronous but could block on network I/O
- Flushing multiple queued writes could take significant time
- Async allows other tasks to run while waiting for I/O
- Tests already mock `sync_queue.flush` as `AsyncMock` (test_sync_worker.py:78, 394)

**What needs to change**:
1. `SyncQueue.flush()` → `async def flush()`
2. `cloud_adapter.write()` calls inside flush remain synchronous (httpx.Client is sync)
3. Wrap blocking I/O in `asyncio.to_thread()` to avoid blocking event loop
4. Update tests that currently expect synchronous flush

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` (lines 78-129)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (lines 96-103)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 120-122)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_worker.py` (lines 67-100)

## Deliverables

- [ ] Convert `SyncQueue.flush()` to `async def flush()`
- [ ] Use `asyncio.to_thread()` to wrap blocking I/O (file reads, adapter writes)
- [ ] Update `main.py` startup sync to `await sync_queue.flush(cloud_adapter)`
- [ ] Update any tests that expect synchronous flush
- [ ] No changes to CloudAdapter interface (stays synchronous)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Flush with empty queue → returns `{"flushed": 0, "pending": 0}`
  - Flush with 5 queued writes, all succeed → returns `{"flushed": 5, "pending": 0}`
  - Flush with 5 queued writes, 3 succeed, 2 fail → returns `{"flushed": 3, "pending": 2}`
  - Adapter write raises exception → queue file preserved, counted as pending
  - Concurrent flush calls (should be safe, idempotent)

## Constraints

- No file over 500 lines
- TDD
- Python 3.13
- `SyncQueue.flush()` must be async
- CloudAdapter interface stays synchronous (httpx.Client)
- Use `asyncio.to_thread()` for blocking I/O
- Must not break existing tests

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-SYNC-AUTOSTART-B-RESPONSE.md`

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
