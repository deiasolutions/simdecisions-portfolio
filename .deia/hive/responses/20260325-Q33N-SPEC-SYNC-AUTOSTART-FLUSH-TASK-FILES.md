# Q33N Task Files: SPEC-SYNC-AUTOSTART-FLUSH

**Date:** 2026-03-25
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Regent)
**Spec:** SPEC-SYNC-AUTOSTART-FLUSH

---

## Summary

I've analyzed the spec and existing codebase. **The sync infrastructure is 95% built.** The core issue is that sync is **disabled by default** in `main.py`. I've written **4 task files** to complete the remaining 5%:

1. **TASK-SYNC-AUTOSTART-A**: Enable sync by default (main.py startup logic)
2. **TASK-SYNC-AUTOSTART-B**: Make SyncQueue.flush() async (type correctness)
3. **TASK-SYNC-AUTOSTART-C**: Add RTD events for build monitor
4. **TASK-SYNC-AUTOSTART-D**: Verify graceful shutdown + add test

---

## Key Findings

### What Already Exists (Built)
✅ `SyncEngine` — bidirectional sync with conflict resolution (engine.py)
✅ `PeriodicSyncWorker` — runs sync on interval (worker.py)
✅ `SyncQueue` — offline write queue (sync_queue.py)
✅ Startup sync logic in `main.py` (lines 115-138)
✅ Ledger events (`SYNC_STARTED`, `SYNC_COMPLETED`, `SYNC_CONFLICT`)
✅ HTTP routes (`/sync/trigger`, `/sync/status`, `/sync/conflicts`, `/sync/resolve`)
✅ Comprehensive test suite (248 tests passing)

### What Needs Fixing
❌ Sync disabled by default (`main.py:94`: `sync_enabled = False` when no config)
❌ `SyncQueue.flush()` is sync but called with `await` (type mismatch)
❌ No RTD events for build monitor (only ledger events)
❌ No integration test for graceful shutdown

### What Does NOT Need Building
- ✅ Cloud storage routes (done in SPEC-CLOUD-STORAGE-RAILWAY)
- ✅ Conflict resolution logic (already in SyncEngine)
- ✅ Offline mode queue accumulation (already in CloudAdapter)
- ✅ SyncLog for conflict tracking (already exists)

---

## Task Files Created

### TASK-SYNC-AUTOSTART-A: Enable Sync by Default
**File:** `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-A-ENABLE-BY-DEFAULT.md`

**Objective:** Change `main.py` to default `sync_enabled = True` when config file missing

**Key changes:**
- Line 94: `sync_enabled = sync_config.get("enabled", True)` (was `False`)
- Line 130: `interval_seconds = sync_config.get("interval_seconds", 60)` (keep default)
- Config file still allows override (`enabled: false` disables sync)

**Tests needed:**
- No config file → sync starts with 60s interval
- Config `enabled: false` → sync disabled
- Config `enabled: true, interval_seconds: 120` → sync starts with 120s interval

**Estimated size:** ~10 line change, ~50 lines of tests
**Estimated effort:** 15 minutes

---

### TASK-SYNC-AUTOSTART-B: Make SyncQueue.flush() Async
**File:** `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-B-ASYNC-FLUSH.md`

**Objective:** Convert `SyncQueue.flush()` from sync to async (currently type mismatch)

**Key changes:**
- `sync_queue.py:78`: `def flush(...)` → `async def flush(...)`
- Wrap blocking I/O in `asyncio.to_thread()` (file reads, adapter writes)
- Update `main.py:122`: keep `await sync_queue.flush(cloud_adapter)` (already correct)
- Tests already mock as `AsyncMock`, so minimal test changes

**Why needed:**
- `worker.py:101` calls `await self.sync_queue.flush(...)` but flush is sync
- Works in Python but semantically incorrect
- Blocking I/O in async context is bad practice

**Tests needed:**
- Flush with 5 queued, all succeed → `{flushed: 5, pending: 0}`
- Flush with 5 queued, 3 succeed, 2 fail → `{flushed: 3, pending: 2}`
- Concurrent flush calls (idempotent)

**Estimated size:** ~30 line change in sync_queue.py, ~20 lines of tests
**Estimated effort:** 30 minutes

---

### TASK-SYNC-AUTOSTART-C: Add RTD Events for Sync Status
**File:** `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-C-RTD-EVENTS.md`

**Objective:** Emit RTD events during sync cycles for build monitor

**Key changes:**
- Import RTD emitter in `worker.py` and `engine.py`
- Emit `sync:cycle:started` before `engine.sync()`
- Emit `sync:cycle:completed` after `engine.sync()` with stats
- Emit `sync:queue:flushed` after `sync_queue.flush()` with results
- Emit `sync:conflict:detected` when conflict occurs (additive to ledger event)

**RTD event format:**
```python
{
    "event_type": "sync:cycle:completed",
    "timestamp": "2026-03-25T10:30:00Z",
    "payload": {"pushed": 5, "pulled": 3, "conflicts": 1, "skipped": 12}
}
```

**Tests needed:**
- Verify RTD events emitted with correct payloads
- Sync cycle with conflict → `sync:conflict:detected` event
- Queue flush → `sync:queue:flushed` event

**Estimated size:** ~40 lines across worker.py and engine.py, ~60 lines of tests
**Estimated effort:** 45 minutes

---

### TASK-SYNC-AUTOSTART-D: Verify Graceful Shutdown + Add Test
**File:** `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-D-GRACEFUL-SHUTDOWN.md`

**Objective:** Verify shutdown logic works and add integration test

**Key changes:**
- Add `test_graceful_shutdown_sync_worker()` integration test
- Start worker, wait for 1 cycle, call stop(), verify clean shutdown
- Verify `worker._task is None` after stop
- Verify no pending asyncio tasks
- Shutdown must complete within 3 seconds

**Current shutdown logic (main.py:256-260):**
```python
if periodic_worker:
    await periodic_worker.stop()
if file_watcher:
    file_watcher.stop()
```

**This looks correct**, but no test proves it. Task verifies and tests it.

**Tests needed:**
- Shutdown during active sync → clean cancellation
- Shutdown before any sync → immediate stop
- Shutdown with FileWatcher running → both stop cleanly
- Double shutdown → idempotent, no error

**Estimated size:** ~80 lines of tests, 0-10 lines of fixes (if needed)
**Estimated effort:** 30 minutes

---

## Dependency Graph

```
TASK-A (Enable by default) ← independent
TASK-B (Async flush)       ← independent (type correctness fix)
TASK-C (RTD events)        ← depends on TASK-B (needs async flush to work correctly)
TASK-D (Graceful shutdown) ← depends on TASK-A + TASK-B (tests full lifecycle)
```

**Recommended dispatch order:**
1. Dispatch TASK-A and TASK-B in parallel (independent)
2. Wait for both to complete
3. Dispatch TASK-C (needs B done)
4. Dispatch TASK-D last (integration test, needs A+B+C done)

---

## Test Coverage Summary

**Existing tests:** 248 passing (sync_engine, sync_worker, sync_log, routes)

**New tests (from tasks):**
- TASK-A: 4 tests (config file scenarios)
- TASK-B: 5 tests (async flush scenarios)
- TASK-C: 5 tests (RTD event emission)
- TASK-D: 4 tests (graceful shutdown scenarios)

**Total new tests:** ~18 tests

**Estimated total after completion:** 248 + 18 = **266 passing tests** for sync subsystem

---

## Smoke Test Plan

After all tasks complete:

```bash
# 1. Run sync tests
cd hivenode && python -m pytest tests/hivenode/sync/ -v

# 2. Run all tests (no regressions)
cd hivenode && python -m pytest tests/ -v

# 3. Manual smoke test
# Start hivenode, verify sync worker starts, check logs for sync cycles
python -m hivenode.main
# Wait 60 seconds, check logs for "Sync cycle completed"
```

---

## Acceptance Criteria Mapping

Spec acceptance criteria → Task mapping:

| Acceptance Criteria | Task |
|---------------------|------|
| Sync worker starts automatically with hivenode | TASK-A |
| Sync runs on configurable interval (default 60s) | TASK-A |
| SyncQueue flushes to cloud when reachable | TASK-B |
| Offline mode: queue accumulates, flushes on reconnect | ✅ Already built (CloudAdapter) |
| Graceful shutdown (no orphan sync processes) | TASK-D |
| Conflicts logged to Event Ledger | ✅ Already built (SyncEngine line 274) |
| Tests for auto-start, flush, offline/online transitions | TASK-A, TASK-B, TASK-D |
| Sync status RTD events for build monitor | TASK-C |

---

## Files Modified (Predicted)

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (TASK-A: 2 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` (TASK-B: ~30 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (TASK-C: ~20 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (TASK-C: ~20 lines)

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sync_autostart.py` (TASK-A: ~80 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_queue_async.py` (TASK-B: ~100 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_rtd_events.py` (TASK-C: ~120 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_graceful_shutdown.py` (TASK-D: ~100 lines)

**Total lines modified:** ~100
**Total lines added (tests):** ~400

---

## Notes for Q33NR

1. **Sync is already 95% built.** This spec is mostly "enable the switch" + add monitoring.

2. **No major architectural changes.** All changes are:
   - Configuration defaults (TASK-A)
   - Type correctness (TASK-B)
   - Observability (TASK-C)
   - Test coverage (TASK-D)

3. **All tasks are small** (~30-120 lines of changes + tests). Total effort: ~2 hours for a bee.

4. **TDD enforced.** Every task requires tests first.

5. **No hardcoded colors, no files over 500 lines, no stubs** (per BOOT.md).

6. **Model assignment:** Recommend **Haiku** for TASK-A and TASK-D (simple changes), **Sonnet** for TASK-B and TASK-C (async/event patterns).

7. **Dispatch recommendation:** Parallel A+B, then C, then D (see dependency graph above).

---

## Ready for Review

All 4 task files are written and ready for your review:
- `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-A-ENABLE-BY-DEFAULT.md`
- `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-B-ASYNC-FLUSH.md`
- `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-C-RTD-EVENTS.md`
- `.deia/hive/tasks/2026-03-25-TASK-SYNC-AUTOSTART-D-GRACEFUL-SHUTDOWN.md`

Please review and approve dispatch or request corrections.
