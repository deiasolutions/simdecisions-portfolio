# TASK-192: Volume Sync E2E Verification Tests

**Date:** 2026-03-16
**Model Assignment:** Sonnet
**Priority:** P1
**Estimated Complexity:** M

---

## Objective

Write comprehensive end-to-end tests that verify the volume sync infrastructure works between home:// and cloud:// volumes. This is a VERIFICATION task — the sync code exists and is complete. We need tests that prove it works end-to-end with real volumes.

---

## Context

The volume sync system is fully implemented and wired into main.py:

1. **SyncEngine** (`hivenode/sync/engine.py`) — bidirectional sync with content hash comparison, conflict resolution (last-write-wins), provenance tracking, Event Ledger integration
2. **SyncLog** (`hivenode/sync/sync_log.py`) — SQLite database tracking sync operations (pending, synced, conflict, failed)
3. **SyncQueue** (`hivenode/storage/adapters/sync_queue.py`) — queues writes when cloud:// is offline, flushes on reconnect
4. **PeriodicSyncWorker** (`hivenode/sync/worker.py`) — background task running sync cycles at configurable intervals (default 300s)
5. **Sync Routes** (`hivenode/routes/sync_routes.py`) — HTTP endpoints: `/sync/trigger`, `/sync/status`, `/sync/conflicts`, `/sync/resolve`

Existing tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` cover basic sync operations BUT use local temp directories for both volumes. This task requires E2E tests that verify sync works between real home:// and cloud:// volumes (or simulated cloud adapter with HTTP).

**From SPEC-HIVENODE-E2E-001.md Section 6:**
- On file write to home://, change queued for push to cloud://
- On file write to cloud://, change queued for push to home:// on next connect
- Periodic sync every 5 minutes (configurable) ✅ Already implemented
- Manual sync via 8os sync CLI command ✅ Already implemented
- On hivenode startup, pull changes from cloud since last sync ✅ Already implemented (main.py line 114)
- Conflict resolution: last-write-wins, both versions preserved (.conflict file) ✅ Already implemented
- sync_log.db tracks all sync operations ✅ Already implemented
- Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events ✅ Already implemented
- Offline queue: writes to offline volume queued, flushed on reconnect ✅ Already implemented
- **10+ tests including conflict scenarios** ❌ NEEDS E2E VERIFICATION

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (SyncEngine implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\sync_log.py` (SyncLog database)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (PeriodicSyncWorker)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` (SyncQueue)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py` (HTTP routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` (existing tests — reference for fixtures)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 6: Volume Sync requirements)

---

## Deliverables

### Primary Deliverable

- [ ] **NEW FILE:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py`
  - Minimum 12 E2E tests (one per scenario below)
  - All tests pass
  - File under 500 lines (split into multiple files if needed)
  - Tests use real components (SyncEngine, SyncLog, VolumeRegistry) — not mocks
  - Tests clean up temp directories after each test

### Test Scenarios (12 Required)

1. **Write to home://, verify appears on cloud:// after sync**
   - Write file via home adapter
   - Trigger sync manually
   - Verify file exists on cloud adapter
   - Verify content hash matches
   - Verify sync_log entry created with status='synced'

2. **Write to cloud://, verify appears on home:// after sync**
   - Write file via cloud adapter
   - Trigger sync manually
   - Verify file exists on home adapter
   - Verify content hash matches

3. **Modify same file on both sides, verify conflict resolution**
   - Write file with content A on home://
   - Write file with content B on cloud://
   - Give cloud:// newer timestamp (use time.sleep)
   - Trigger sync
   - Verify cloud:// content wins (content B at original path)
   - Verify home:// content preserved as `.conflict.<timestamp>` file
   - Verify SYNC_CONFLICT event in ledger
   - Verify sync_log entry marked as 'conflict'

4. **File only on home://, verify pushed to cloud://**
   - Write new file on home://
   - Cloud:// has no such file
   - Trigger sync
   - Verify file appears on cloud://

5. **File only on cloud://, verify pulled to home://**
   - Write new file on cloud://
   - home:// has no such file
   - Trigger sync
   - Verify file appears on home://

6. **Identical files on both sides, verify skipped**
   - Write identical file on both home:// and cloud://
   - Trigger sync
   - Verify stats["skipped"] == 1
   - Verify no provenance changes

7. **Offline cloud://, verify write queued**
   - Simulate cloud:// offline (mock adapter raises ConnectionError)
   - Write file to home://
   - Verify write queued in SyncQueue
   - Simulate cloud:// back online
   - Flush queue
   - Verify file appears on cloud://

8. **GET /sync/status returns correct counts**
   - Create 2 pending sync entries via sync_log.queue_sync()
   - Create 1 conflict entry via sync_log.mark_conflict()
   - Call GET /sync/status via TestClient
   - Verify pending_count == 2
   - Verify conflict_count == 1

9. **GET /sync/conflicts returns conflict list**
   - Create 2 conflicts via sync_log
   - Call GET /sync/conflicts via TestClient
   - Verify 2 entries returned
   - Verify each has: id, path, source_volume, target_volume, error

10. **POST /sync/resolve marks conflict as resolved**
    - Create conflict entry via sync_log
    - Call POST /sync/resolve with conflict_id
    - Verify conflict no longer in GET /sync/conflicts
    - Verify sync_log status changed to 'synced'

11. **Manual sync via POST /sync/trigger**
    - Write file on home://
    - Call POST /sync/trigger with source=home, target=cloud via TestClient
    - Verify response contains pushed=1

12. **Periodic worker runs sync automatically** (OPTIONAL — can be commented out if timing is unreliable)
    - Start PeriodicSyncWorker with interval_seconds=5
    - Write file on home://
    - Wait 6 seconds (use asyncio.sleep)
    - Verify file appears on cloud://
    - Stop worker

---

## Test Requirements

### TDD NOT Required

This is a VERIFICATION task for existing code. Write tests AFTER reading the implementation. The goal is to verify the existing sync engine works correctly.

### Test Implementation Notes

- Use temp directories for home:// and cloud:// base paths
- Use real VolumeRegistry with real LocalStorageAdapter for both volumes
- OR: Use MockTransport for cloud adapter to simulate HTTP calls
- Use real SyncLog with temp SQLite database
- Use real LedgerWriter with temp SQLite database
- Use real ProvenanceStore with temp SQLite database
- Run sync_engine.sync() directly OR call HTTP routes via TestClient
- All file paths must be absolute
- All tests must clean up temp directories (use pytest fixtures with try/finally or tempfile.TemporaryDirectory)

### Expected Test Count

**Minimum 12 tests.** If test file exceeds 500 lines, split into:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e_basic.py` (tests 1-6, 11)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e_conflicts.py` (tests 3, 7, 8-10, 12)

---

## Constraints

1. **NO NEW FEATURES.** All code exists. Only write TESTS.
2. **File paths must be absolute** in task files and test output.
3. **Tests must use real components** (SyncEngine, SyncLog, VolumeRegistry) — not mocks (except for simulating offline cloud adapter).
4. **Tests must clean up** temp directories after each test.
5. **Test file must be under 500 lines.** If it grows beyond 500, split into two files.
6. **TDD is NOT required** for verification tasks — the code exists, we're testing it.
7. **All tests must pass** on first run. If tests fail, it means the sync implementation has a bug — report it in the response file.
8. **No stubs.** Every test must be fully implemented.
9. **No hardcoded colors.** (Not applicable — this is backend tests only.)
10. **CSS variables only.** (Not applicable — this is backend tests only.)

---

## Acceptance Criteria

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py` created OR split into `test_sync_e2e_basic.py` and `test_sync_e2e_conflicts.py`
- [ ] Minimum 12 tests written (one per scenario above)
- [ ] All tests pass when run via `python -m pytest tests/hivenode/sync/test_sync_e2e.py -v`
- [ ] Tests verify: file write to home:// → appears on cloud:// after sync
- [ ] Tests verify: file write to cloud:// → appears on home:// after sync
- [ ] Tests verify: conflict resolution (last-write-wins, .conflict file created)
- [ ] Tests verify: sync_log.db tracks all sync operations
- [ ] Tests verify: Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events
- [ ] Tests verify: offline queue (writes to offline volume queued, flushed on reconnect)
- [ ] Tests verify: HTTP routes (POST /sync/trigger, GET /sync/status, GET /sync/conflicts, POST /sync/resolve)
- [ ] Each test cleans up temp directories
- [ ] No test file exceeds 500 lines
- [ ] Test output includes pass/fail counts

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-192-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary (copy paste last 20 lines of pytest output)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Notes for BEE

- Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` for fixture patterns
- Use `tempfile.TemporaryDirectory()` context manager for temp directories
- Use `pytest.mark.asyncio` decorator for async tests
- Use `time.sleep(0.1)` to ensure timestamp differences in conflict tests
- Use `TestClient` from FastAPI for HTTP route tests (see existing test_sync_engine.py for examples)
- If a test fails, DO NOT mark it as passing — report the failure in the response file
- If the sync implementation has bugs, DO NOT fix them — report them as "Issues / Follow-ups"
- This is a verification task — your job is to test what exists, not to build new features
