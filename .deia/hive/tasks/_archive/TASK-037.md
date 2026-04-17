# TASK-037: Sync CLI + Periodic Worker

**Assigned to:** BEE
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 (Wave 3)
**Date:** 2026-03-12
**Depends on:** TASK-035 (sync engine)

---

## Objective

Wire the sync engine (TASK-035) to CLI commands and periodic triggers. This includes:
1. CLI commands (`8os sync`, `8os sync --status`)
2. Periodic sync worker (background task)
3. File watcher for on-write sync
4. Startup sync (pull changes from cloud on hivenode startup)

---

## What Already Exists

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py` — 8os CLI with up/down/status commands (TASK-026)
- TASK-035's SyncEngine (dependency — must be completed first)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — FastAPI app with lifespan

---

## What to Build

### 1. CLI Commands

**Update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`

**Add commands:**

**`8os sync`** — trigger immediate sync cycle
- Calls `POST /sync/trigger` on local hivenode
- Prints sync stats (pushed, pulled, conflicts, skipped)
- Example:
  ```
  $ 8os sync
  Syncing home:// ↔ cloud://...
  Pushed: 5, Pulled: 3, Conflicts: 1, Skipped: 12
  ```

**`8os sync --status`** — show last sync time, pending count, conflicts
- Calls `GET /sync/status` on local hivenode
- Example:
  ```
  $ 8os sync --status
  Last sync: 2026-03-12 10:30:00
  Pending: 3
  Conflicts: 1
  ```

**Implementation notes:**
- Use `httpx` to call local hivenode routes
- Handle errors gracefully (e.g., hivenode not running)
- Exit codes: 0 = success, 1 = error

---

### 2. Periodic Sync Worker

**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py`

**PeriodicSyncWorker class:**
- `__init__(sync_engine, sync_queue, interval_seconds)`
- `start()` — start background task
- `stop()` — stop background task

**Worker behavior:**
1. Run sync on interval (default 300s from config)
2. Also flush SyncQueue on each cycle
3. Log sync events to ledger
4. Handle errors gracefully (log, don't crash)

**Integration with hivenode startup:**
Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` lifespan:
- On startup: if `sync.enabled: true` in config, start PeriodicSyncWorker
- On shutdown: stop PeriodicSyncWorker

**Config:**
```yaml
sync:
  enabled: true
  interval_seconds: 300
  on_write: true
```

---

### 3. File Watcher (On-Write Sync)

**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\watcher.py`

**FileWatcher class:**
- `__init__(sync_log, volume_paths, ignore_patterns)`
- `start()` — start watching
- `stop()` — stop watching

**Watcher behavior:**
1. Use `watchdog` library to monitor volume paths
2. On file write: queue sync entry in sync_log
3. Respect sync_ignore patterns
4. Only runs if `sync.on_write: true` in config

**Implementation notes:**
- Use `watchdog.observers.Observer` for file system events
- Use `watchdog.events.FileSystemEventHandler` for event handling
- Watch both `home://` and `cloud://` volume paths
- Debounce file writes (wait 1s after last write before queueing)

**Integration with hivenode startup:**
Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` lifespan:
- On startup: if `sync.on_write: true` in config, start FileWatcher
- On shutdown: stop FileWatcher

---

### 4. Startup Sync

**Update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

**Lifespan changes:**
1. On hivenode startup: pull changes from cloud since last sync timestamp
2. Flush any pending SyncQueue entries
3. Log startup sync to ledger

**Implementation:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... existing initialization ...

    # Startup sync
    if settings.sync_enabled:
        sync_engine = SyncEngine(...)
        await sync_engine.sync("cloud", "home")  # Pull from cloud
        await sync_queue.flush(cloud_adapter)

    yield

    # ... existing cleanup ...
```

---

## Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_worker.py`

**Test coverage (~10 tests):**
1. CLI `8os sync` command — success
2. CLI `8os sync` command — hivenode not running
3. CLI `8os sync --status` command
4. PeriodicSyncWorker scheduling (runs on interval)
5. PeriodicSyncWorker flush (flushes SyncQueue on each cycle)
6. PeriodicSyncWorker error handling (logs errors, doesn't crash)
7. FileWatcher detects file writes
8. FileWatcher respects sync_ignore patterns
9. FileWatcher debouncing (multiple writes = single queue entry)
10. Startup sync (pulls from cloud on startup)

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — all functions fully implemented
- PeriodicSyncWorker must be gracefully stoppable (no zombie threads)
- FileWatcher must respect ignore patterns (no infinite loops on log files)
- Startup sync must not block hivenode startup (run in background)

---

## Dependencies

**Python libraries:**
- `watchdog` — for file system watching (add to `pyproject.toml`)

---

## Deliverables

1. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py` (add `8os sync` commands)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\watcher.py`
4. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lifespan startup sync + workers)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_worker.py`
6. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` to add `watchdog` dependency

---

**End of TASK-037**
