# BRIEFING: Volume Sync home:// <-> cloud:// End-to-End

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-3006-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Priority:** P1
**Model Assignment:** Sonnet

---

## Objective

Verify that the volume sync infrastructure already built works end-to-end between local hivenode (home://) and cloud hivenode (cloud://). This is NOT a build task — it's a VERIFICATION task. The code exists. We need comprehensive E2E tests to prove it works.

---

## Context

### What Already Exists

The sync infrastructure is COMPLETE and wired into main.py:

1. **Sync Engine** (`hivenode/sync/engine.py`)
   - Bidirectional sync with content hash comparison
   - Conflict resolution (last-write-wins, preserve both versions)
   - Provenance tracking
   - Event Ledger integration

2. **Sync Log** (`hivenode/sync/sync_log.py`)
   - SQLite database tracking sync operations
   - Status: pending, synced, conflict, failed
   - Schema matches SPEC-HIVENODE-E2E-001.md Section 6

3. **Sync Queue** (`hivenode/storage/adapters/sync_queue.py`)
   - Queues writes when cloud:// is offline
   - Flushes on reconnect
   - Base64-encoded content in JSON files

4. **Periodic Worker** (`hivenode/sync/worker.py`)
   - Background task running sync cycles at configurable intervals
   - Default: 300 seconds (5 minutes)
   - Configurable via `~/.shiftcenter/config.yml`

5. **File Watcher** (`hivenode/sync/watcher.py`)
   - Detects local file changes using watchdog
   - Triggers immediate sync if `sync.on_write: true` in config

6. **Sync Routes** (`hivenode/routes/sync_routes.py`)
   - `POST /sync/trigger` — manual sync
   - `GET /sync/status` — last sync time, pending count, conflict count
   - `GET /sync/conflicts` — list conflicts
   - `POST /sync/resolve` — resolve conflict by picking winner

7. **8os CLI Integration** (`hivenode/cli.py`)
   - `8os sync` — trigger manual sync
   - `8os sync --status` — show sync status

8. **Existing Tests** (`tests/hivenode/sync/test_sync_engine.py`)
   - 15+ tests covering sync log, engine push/pull/conflict, HTTP routes
   - BUT: Tests use local temp directories, NOT real home:// and cloud:// volumes

---

## What's Missing

The spec (SPEC-HIVENODE-E2E-001.md Section 6) requires:

1. **On file write to home://, change queued for push to cloud://**
2. **On file write to cloud://, change queued for push to home:// on next connect**
3. **Periodic sync every 5 minutes (configurable)** ✅ Already implemented
4. **Manual sync via 8os sync CLI command** ✅ Already implemented
5. **On hivenode startup, pull changes from cloud since last sync** ✅ Already implemented (main.py line 114)
6. **Conflict resolution: last-write-wins, both versions preserved (.conflict file)** ✅ Already implemented
7. **sync_log.db tracks all sync operations** ✅ Already implemented
8. **Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events** ✅ Already implemented
9. **Offline queue: writes to offline volume queued, flushed on reconnect** ✅ Already implemented
10. **10+ tests including conflict scenarios** ❌ NEEDS E2E VERIFICATION

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (SyncEngine implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\sync_log.py` (SyncLog database)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (PeriodicSyncWorker)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` (SyncQueue)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py` (HTTP routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` (existing tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 6: Volume Sync)

---

## Task Breakdown

### TASK-192: E2E Sync Tests (High Priority)

**Objective:** Write comprehensive E2E tests that verify sync works between real home:// and cloud:// volumes (or simulated cloud adapter with HTTP).

**Test Scenarios:**

1. **Write to home://, verify appears on cloud:// after sync**
   - Write file via home adapter
   - Trigger sync manually
   - Verify file exists on cloud adapter
   - Verify content hash matches
   - Verify sync_log entry created

2. **Write to cloud://, verify appears on home:// after sync**
   - Write file via cloud adapter
   - Trigger sync manually
   - Verify file exists on home adapter
   - Verify content hash matches

3. **Modify same file on both sides, verify conflict resolution**
   - Write file with content A on home://
   - Write file with content B on cloud://
   - Give cloud:// newer timestamp
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
   - Simulate cloud:// offline (mock raises ConnectionError)
   - Write file to home://
   - Verify write queued in SyncQueue
   - Simulate cloud:// back online
   - Flush queue
   - Verify file appears on cloud://

8. **GET /sync/status returns correct counts**
   - Create 2 pending sync entries
   - Create 1 conflict entry
   - Call GET /sync/status
   - Verify pending_count == 2
   - Verify conflict_count == 1

9. **GET /sync/conflicts returns conflict list**
   - Create 2 conflicts
   - Call GET /sync/conflicts
   - Verify 2 entries returned
   - Verify each has: id, path, source_volume, target_volume, error

10. **POST /sync/resolve marks conflict as resolved**
    - Create conflict
    - Call POST /sync/resolve with conflict_id
    - Verify conflict no longer in GET /sync/conflicts
    - Verify sync_log status changed to 'synced'

11. **Manual sync via POST /sync/trigger**
    - Write file on home://
    - Call POST /sync/trigger with source=home, target=cloud
    - Verify response contains pushed=1

12. **Periodic worker runs sync automatically** (optional — hard to test without waiting 5 minutes)
    - Start PeriodicSyncWorker with interval_seconds=5
    - Write file on home://
    - Wait 6 seconds
    - Verify file appears on cloud://
    - Stop worker

**Implementation Notes:**

- Use temp directories for home:// and cloud:// base paths
- Use real VolumeRegistry with real LocalStorageAdapter for both
- OR: Use MockTransport for cloud adapter to simulate HTTP calls
- Use real SyncLog with temp SQLite database
- Use real LedgerWriter with temp SQLite database
- Use real ProvenanceStore with temp SQLite database
- Run sync_engine.sync() directly OR call HTTP routes via TestClient
- All file paths must be absolute
- All tests must clean up temp directories

**Deliverables:**

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py` (NEW file)
- 12+ tests (one per scenario above)
- All tests pass
- Test file under 500 lines (split into multiple files if needed)

**Test Count Requirement:** Minimum 12 tests

---

### TASK-193: Smoke Test Script (Lower Priority)

**Objective:** Create a manual smoke test script that Dave can run to verify sync works on his actual local hivenode + Railway cloud hivenode.

**Script:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\smoke_sync.py`

**What it does:**

1. Verify local hivenode is running (check `http://localhost:8420/health`)
2. Verify cloud hivenode is reachable (check Railway health endpoint)
3. Write a test file to home:// via `POST /storage/write`
4. Trigger sync via `POST /sync/trigger`
5. Read the file from cloud:// via `POST /storage/read`
6. Verify content matches
7. Delete test file from both volumes
8. Print success message

**Deliverables:**

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\smoke_sync.py` (NEW file)
- Runnable via `python tests/smoke/smoke_sync.py`
- Prints clear success/failure messages
- Cleans up test files

**Test Count Requirement:** This is a script, not a test file. No test count.

---

## Acceptance Criteria (from Original Spec)

- [x] On file write to home://, change queued for push to cloud:// — VERIFY with TASK-192 test #1
- [x] On file write to cloud://, change queued for push to home:// on next connect — VERIFY with TASK-192 test #2
- [x] Periodic sync every 5 minutes (configurable) — Already implemented, optionally verify with TASK-192 test #12
- [x] Manual sync via 8os sync CLI command — Already implemented, verify with TASK-192 test #11
- [x] On hivenode startup, pull changes from cloud since last sync — Already implemented (main.py line 114)
- [x] Conflict resolution: last-write-wins, both versions preserved (.conflict file) — VERIFY with TASK-192 test #3
- [x] sync_log.db tracks all sync operations — VERIFY with TASK-192 tests #1-11
- [x] Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events — VERIFY with TASK-192 test #3
- [x] Offline queue: writes to offline volume queued, flushed on reconnect — VERIFY with TASK-192 test #7
- [x] 10+ tests including conflict scenarios — DELIVER with TASK-192 (12 tests minimum)

---

## Smoke Test (from Original Spec)

This smoke test is TASK-193:

- [ ] Write file on local hivenode -> appears on cloud after sync
- [ ] Write file on cloud -> appears on local after sync
- [ ] Write same file on both before sync -> conflict file created, latest wins

---

## Dependencies

**Depends on:** w3-06-cloud-adapter-e2e (COMPLETE — in `_done/`)

The cloud adapter is built and verified. Now we verify sync works between home:// and cloud://.

---

## Constraints

1. **NO NEW FEATURES.** All code exists. Only write TESTS.
2. **File paths must be absolute** in task files.
3. **Tests must use real components** (SyncEngine, SyncLog, VolumeRegistry) — not mocks.
4. **Tests must clean up** temp directories after each test.
5. **Test file must be under 500 lines.** If it grows beyond 500, split into `test_sync_e2e_basic.py` and `test_sync_e2e_conflicts.py`.
6. **TDD is NOT required** for verification tasks — the code exists, we're testing it.
7. **All tests must pass** on first run. If tests fail, it means the sync implementation has a bug — file a fix spec.

---

## Response Requirements

Q33N must write task files for:

1. **TASK-192** (E2E tests — sonnet)
2. **TASK-193** (smoke script — haiku)

Each task file must include:
- Objective
- Context
- Files to Read First (absolute paths)
- Deliverables (absolute paths)
- Test Requirements (specific count, specific scenarios)
- Constraints (absolute paths, TDD, no stubs, CSS vars, 500-line limit)
- Response Requirements (8-section template)

---

## Next Steps for Q33N

1. Read this briefing
2. Read all files listed in "Files to Read First"
3. Write TASK-192.md for E2E tests
4. Write TASK-193.md for smoke script
5. Return task files to Q33NR for review
6. After Q33NR approval, dispatch bees
7. After bees complete, verify all 12+ tests pass
8. Report results to Q33NR

---

**End of Briefing**
