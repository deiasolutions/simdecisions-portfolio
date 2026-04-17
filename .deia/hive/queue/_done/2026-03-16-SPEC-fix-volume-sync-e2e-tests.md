# SPEC: Fix Volume Sync E2E Test Failures

## Priority
P1

## Objective
Fix 2 failing tests in tests/hivenode/sync/test_sync_e2e.py:
1. test_e2e_conflict_resolution — assertion expects 1 conflict file but gets 2
2. test_e2e_offline_queue — TypeError on await of non-async flush() method

## Context
Original work: TASK-192 from w3-07-volume-sync-e2e
Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py`
Current status: 10/12 tests passing

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py` (test file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (SyncEngine implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\queue.py` (SyncQueue implementation)

## Error Details

### Error 1: test_e2e_conflict_resolution (line 266)
```
assert len(conflict_files) == 1
AssertionError: assert 2 == 1
  where 2 = len(['conflict_test.conflict.20260316-232222.md', 'conflict_test.md'])
```
**Root cause:** Test expects 1 conflict marker file but SyncEngine creates both the original file and a conflict marker file. Fix the assertion or the conflict resolution logic to match expected behavior.

### Error 2: test_e2e_offline_queue (line 430)
```
flush_result = await sync_queue.flush(cloud)
TypeError: object dict can't be used in 'await' expression
```
**Root cause:** `sync_queue.flush()` is not an async function. Either:
1. Remove the `await` keyword if flush() is synchronous, OR
2. Make flush() async if it should be

## Acceptance Criteria
- [ ] test_e2e_conflict_resolution passes (fix assertion or conflict logic)
- [ ] test_e2e_offline_queue passes (fix await/async issue)
- [ ] All 10 previously passing tests still pass (no regressions)
- [ ] Final test count: 12/12 passing
- [ ] No stubs or TODOs
- [ ] CSS uses var(--sd-*) only (if any CSS changes)

## Test Command
```bash
cd tests/hivenode && python -m pytest sync/test_sync_e2e.py -v
```

## Model Assignment
haiku

## Constraints
- Do not break existing passing tests
- Fix only the reported errors, do not refactor
- No file over 500 lines
- TDD: write test fix first, then code fix if needed
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-16-SPEC-fix-volume-sync-e2e-tests", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-16-SPEC-fix-volume-sync-e2e-tests", "files": ["tests/hivenode/sync/test_sync_e2e.py"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done, release early: POST http://localhost:8420/build/release

## Smoke Test
```bash
cd tests/hivenode && python -m pytest sync/test_sync_e2e.py::test_e2e_conflict_resolution -v
cd tests/hivenode && python -m pytest sync/test_sync_e2e.py::test_e2e_offline_queue -v
cd tests/hivenode && python -m pytest sync/test_sync_e2e.py -v
```
Expected: 12 passed, 0 failed
