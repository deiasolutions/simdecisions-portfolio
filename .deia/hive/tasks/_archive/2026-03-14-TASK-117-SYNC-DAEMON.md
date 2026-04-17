# TASK-117: Sync Daemon

**Wave:** 3
**Model:** haiku
**Role:** bee
**Depends on:** TASK-116

---

## Objective

Build background daemon that orchestrates markdown export and cloud sync based on policy (IMMEDIATE, BATCHED, MANUAL).

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\markdown_exporter.py` (MarkdownExporter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\cloud_sync.py` (CloudSyncService)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (IndexStorage)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\sync_daemon.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_sync_daemon.py`

## Files to Modify

None

## Deliverables

### sync_daemon.py (267 lines)

**Enum:** `SyncPolicy`

```python
class SyncPolicy(str, Enum):
    IMMEDIATE = "immediate"  # Sync every indexed file immediately
    BATCHED = "batched"      # Sync in batches at interval
    MANUAL = "manual"        # Sync only on explicit force_sync_all() call
```

**Class:** `SyncDaemon`

**Attributes:**
- `storage: IndexStorage`
- `exporter: MarkdownExporter`
- `cloud_sync: CloudSyncService`
- `policy: SyncPolicy`
- `batch_interval_seconds: int` — default 300 (5 minutes)
- `enable_markdown: bool` — default True
- `enable_cloud: bool` — default False (requires HIVE_CLOUD_DB_URL)
- `running: bool` — daemon state
- `pending_queue: set[str]` — artifact_ids pending batch sync
- `last_sync_time: Optional[datetime]` — timestamp of last batch sync
- `daemon_thread: Optional[threading.Thread]` — background thread

**Methods:**

1. **`__init__(storage: IndexStorage, exporter: MarkdownExporter, cloud_sync: CloudSyncService, policy: SyncPolicy = SyncPolicy.MANUAL, batch_interval_seconds: int = 300, enable_markdown: bool = True, enable_cloud: bool = False)`**
   - Store all parameters
   - running = False
   - pending_queue = set()
   - last_sync_time = None
   - daemon_thread = None

2. **`start() -> None`**
   - Set running = True
   - Spawn daemon thread: `daemon_thread = threading.Thread(target=_daemon_loop, daemon=True)`
   - Start thread

3. **`stop() -> None`**
   - Set running = False
   - Wait for daemon_thread to finish (join with timeout=10s)

4. **`on_context_indexed(artifact_id: str) -> None`**
   - Called by IndexerService after indexing a file
   - Route by policy:
     - IMMEDIATE: call `_sync_now(artifact_id)`
     - BATCHED: add artifact_id to pending_queue
     - MANUAL: do nothing

5. **`force_sync_all() -> dict`**
   - Override policy, sync everything now
   - Clear pending_queue
   - Call `_sync_all_records()`
   - Return stats: `{"synced": count, "failed": count}`

6. **`get_status() -> dict`**
   - Return:
     ```python
     {
       "running": self.running,
       "policy": self.policy,
       "pending_count": len(self.pending_queue),
       "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None,
       "enable_markdown": self.enable_markdown,
       "enable_cloud": self.enable_cloud
     }
     ```

7. **`_daemon_loop() -> None`**
   - While running:
     - If policy == BATCHED and time since last_sync >= batch_interval:
       - Call `_sync_batch()`
     - Sleep 10 seconds
     - Repeat

8. **`_sync_now(artifact_id: str) -> None`**
   - If enable_markdown: call `exporter.write_markdown_file(artifact_id, storage)`
   - If enable_cloud: call `cloud_sync.sync_to_cloud(artifact_id)`

9. **`_sync_batch() -> None`**
   - For each artifact_id in pending_queue:
     - Call `_sync_now(artifact_id)`
   - Clear pending_queue
   - Update last_sync_time = now

10. **`_sync_all_records() -> dict`**
    - Get all records: `storage.list_all()`
    - For each record: call `_sync_now(artifact_id)`
    - Return stats: `{"synced": count, "failed": count}`

**Factory function:**

11. **`create_daemon_from_env(storage: IndexStorage, exporter: MarkdownExporter, cloud_sync: CloudSyncService) -> SyncDaemon`**
    - Read environment variables:
      - `SYNC_POLICY` — default "manual" (parse to SyncPolicy enum)
      - `SYNC_BATCH_INTERVAL` — default 300 (int)
      - `SYNC_ENABLE_CLOUD` — default "false" (parse to bool)
      - `SYNC_ENABLE_MARKDOWN` — default "true" (parse to bool)
    - Create and return SyncDaemon instance

### test_sync_daemon.py (6+ tests)

**Test cases:**
- Test IMMEDIATE policy: `on_context_indexed()` syncs immediately
- Test BATCHED policy: `on_context_indexed()` adds to queue, daemon syncs at interval
- Test MANUAL policy: `on_context_indexed()` does nothing
- Test `force_sync_all()` syncs all records regardless of policy
- Test `get_status()` returns correct daemon state
- Test `create_daemon_from_env()` reads environment variables correctly
- Test daemon thread starts and stops gracefully

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/test_sync_daemon.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same 3 policies, same batch interval logic as platform/efemera
- [ ] TDD: tests written first
- [ ] 6+ tests covering all policies, batch timer, force sync, status, env factory
- [ ] Environment variables: `SYNC_POLICY`, `SYNC_BATCH_INTERVAL`, `SYNC_ENABLE_CLOUD`, `SYNC_ENABLE_MARKDOWN`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-117-RESPONSE.md`

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
