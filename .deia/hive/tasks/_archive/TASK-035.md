# TASK-035: Volume Sync Engine

**Assigned to:** BEE
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 (Wave 3)
**Date:** 2026-03-12
**Depends on:** None

---

## Objective

Build the bidirectional sync engine for `home://` ↔ `cloud://` volumes. This includes:
1. Sync log database (SQLite) for tracking sync operations
2. SyncEngine class for bidirectional content hash comparison and sync
3. Conflict resolution (last-write-wins, both versions preserved)
4. Sync ignore patterns (gitignore syntax)
5. HTTP routes for triggering sync, status, and conflict resolution

---

## What Already Exists

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` — CloudAdapter with httpx (TASK-030)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` — SyncQueue for offline writes (TASK-030)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\transport.py` — FileTransport with provenance + ledger integration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\provenance.py` — ProvenanceStore with content hash tracking
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — LedgerWriter for event logging

---

## What to Build

### 1. Sync Log Database

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\sync_log.py`

**Schema:**
```sql
CREATE TABLE sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    source_volume TEXT NOT NULL,
    target_volume TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    queued_at TEXT NOT NULL,
    synced_at TEXT,
    error TEXT
);
```

**Operations:**
- `queue_sync(path, hash, source, target)` — add pending sync entry
- `mark_synced(id)` — update status='synced' + synced_at timestamp
- `mark_conflict(id, error)` — update status='conflict' + error message
- `mark_failed(id, error)` — update status='failed' + error message
- `get_pending()` — all entries with status='pending'
- `get_conflicts()` — all entries with status='conflict'

---

### 2. Sync Engine

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py`

**SyncEngine class:**
- `__init__(volume_registry, ledger_writer, provenance_store, sync_log)`
- `sync(source_volume, target_volume)` — bidirectional sync cycle

**Sync logic:**
1. Get all files from both volumes (recursive list)
2. For each file:
   - Compare content_hash of local vs remote (from ProvenanceStore)
   - **Hashes match** → skip (already synced)
   - **Local newer** → push local to remote
   - **Remote newer** → pull remote to local
   - **Both changed since last sync** → CONFLICT
3. Conflict resolution: last-write-wins by timestamp. Both versions preserved:
   - Winner overwrites file at original path
   - Loser saved as `{filename}.conflict.{timestamp}.{ext}`
4. Log all operations to Event Ledger:
   - `SYNC_STARTED` — at start of sync cycle
   - `SYNC_COMPLETED` — at end of sync cycle (with stats: pushed, pulled, conflicts)
   - `SYNC_CONFLICT` — when a conflict is detected
   - `SYNC_QUEUED` — when a file is queued for sync
   - `SYNC_FLUSHED` — when queued writes are flushed

**Return value:**
```python
{
    "pushed": 5,
    "pulled": 3,
    "conflicts": 1,
    "skipped": 12
}
```

---

### 3. Sync Ignore Patterns

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\ignore.py`

**Functions:**
- `load_ignore_patterns(ignore_file_path)` — read `~/.shiftcenter/sync_ignore` (gitignore syntax)
- `should_sync(path, patterns)` — return `True` if path should be synced

**Always skip:**
- `.git/`
- `node_modules/`
- `__pycache__/`

**Gitignore syntax support:**
- `*.log` — glob patterns
- `/foo/` — directory anchoring
- `!important.log` — negation

Use `pathspec` library for gitignore parsing.

---

### 4. Sync HTTP Routes

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py`

**Routes:**

**POST `/sync/trigger`** — trigger a sync cycle
- Body: `{"source": "home", "target": "cloud"}`
- Response: `{"pushed": 5, "pulled": 3, "conflicts": 1, "skipped": 12}`

**GET `/sync/status`** — last sync time, pending count, conflict count
- Response:
  ```json
  {
    "last_sync_at": "2026-03-12T10:30:00Z",
    "pending_count": 3,
    "conflict_count": 1
  }
  ```

**GET `/sync/conflicts`** — list all conflicts
- Response:
  ```json
  {
    "conflicts": [
      {
        "id": 1,
        "path": "docs/test.md",
        "source_volume": "home",
        "target_volume": "cloud",
        "error": "Both changed since last sync",
        "queued_at": "2026-03-12T10:30:00Z"
      }
    ]
  }
  ```

**POST `/sync/resolve`** — resolve a conflict (pick winner)
- Body: `{"conflict_id": 1, "winner": "home"}`
- Response: `{"ok": true}`

**Wire routes to FastAPI app:**
Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` to include sync routes.

---

## Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py`

**Test coverage (~15 tests):**
1. Sync log CRUD operations
2. SyncEngine push (local → remote)
3. SyncEngine pull (remote → local)
4. SyncEngine conflict detection + last-write-wins
5. SyncEngine skip (hashes match)
6. Conflict file naming (`{filename}.conflict.{timestamp}.{ext}`)
7. Sync ignore patterns (glob, directory, negation)
8. POST `/sync/trigger` route
9. GET `/sync/status` route
10. GET `/sync/conflicts` route
11. POST `/sync/resolve` route
12. Ledger event logging (SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT)
13. Sync with empty volumes
14. Sync with SyncQueue flush (offline writes)
15. Idempotency (running sync twice with no changes = no-op)

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — all functions fully implemented
- Sync must be idempotent (running twice with no changes = no-op)
- Conflict resolution must preserve both versions (never lose data)
- Use ProvenanceStore for content hash lookup (not file reads)
- All ledger events must use universal entity IDs (e.g., `system:sync-engine`)

---

## Dependencies

**Python libraries:**
- `pathspec` — for gitignore syntax parsing (add to `pyproject.toml`)

---

## Deliverables

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\sync_log.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\ignore.py`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py`
6. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` to include sync routes
7. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` to add `pathspec` dependency

---

**End of TASK-035**
