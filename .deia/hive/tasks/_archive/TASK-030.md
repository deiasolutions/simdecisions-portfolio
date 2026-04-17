# TASK-030: Cloud Storage Adapter

**Assigned to:** BEE-SONNET
**Model:** Sonnet
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 5)
**Parent:** SPEC-HIVENODE-E2E-001 Wave 2

---

## Objective

Wire the `cloud://` volume adapter to call a remote hivenode's `/storage/*` routes over HTTPS. Currently all 8 methods in `hivenode/storage/adapters/cloud.py` raise `NotImplementedError`. Replace them with real HTTPS calls using `httpx`.

The cloud adapter on the LOCAL hivenode is an HTTP client that calls the CLOUD hivenode's `/storage/*` routes. It is NOT direct S3/volume access.

---

## Architecture (Section 5.1)

```
Browser → local hivenode (home://) → writes to local disk
Browser → cloud hivenode (cloud://) → writes to Railway volume
Local hivenode → cloud hivenode → sync (Wave 3)
```

The local hivenode's cloud adapter acts as an HTTP client to the cloud hivenode.

---

## Cloud Adapter Interface (Section 5.2)

All 8 methods to implement in `hivenode/storage/adapters/cloud.py`:

```python
class CloudStorageAdapter(BaseVolumeAdapter):
    def __init__(self, cloud_url: str, auth_token: str):
        self.cloud_url = cloud_url    # https://api.shiftcenter.com
        self.auth_token = auth_token  # ra96it JWT
        self.client = httpx.AsyncClient()

    async def read(self, path: str) -> bytes:
        # POST cloud_url/storage/read with { "path": path }
        # Include Authorization: Bearer <token> header
        # Return bytes content
        # If 404 → raise FileNotFoundError
        # If offline → raise VolumeOfflineError (new exception)

    async def write(self, path: str, content: bytes, actor: str, intent: str) -> dict:
        # POST cloud_url/storage/write with { "path": path, "content": base64(content), "actor": actor, "intent": intent }
        # Return response metadata
        # If offline → enqueue in sync_queue, return { "queued": true }

    async def list(self, path: str) -> list:
        # POST cloud_url/storage/list with { "path": path }
        # Return list of entries
        # If offline → raise VolumeOfflineError

    async def stat(self, path: str) -> dict:
        # POST cloud_url/storage/stat with { "path": path }
        # Return { "size": int, "modified": str, "content_hash": str }
        # If offline → raise VolumeOfflineError

    async def delete(self, path: str) -> dict:
        # POST cloud_url/storage/delete with { "path": path }
        # Return confirmation
        # If offline → raise VolumeOfflineError

    async def exists(self, path: str) -> bool:
        # Call stat(), return True if 200, False if 404
        # If offline → raise VolumeOfflineError

    async def move(self, src: str, dest: str) -> dict:
        # No native move over HTTP. Implement as: read(src) + write(dest) + delete(src)
        # If offline → raise VolumeOfflineError
```

Every operation includes the ra96it JWT in the `Authorization: Bearer <token>` header.

---

## Offline Behavior (Section 5.3)

If cloud:// is unreachable (network down, timeout, connection refused):

- **Reads** → raise `VolumeOfflineError` (new exception class)
- **Writes** → enqueue in `~/.shiftcenter/sync_queue/` (one file per queued write, JSON format with path + content_base64 + metadata)
- **Queue flushes** when cloud:// comes back online (checked on next operation or periodic sync)

### Sync Queue

Create new file: `hivenode/storage/adapters/sync_queue.py`

```python
class SyncQueue:
    def __init__(self, queue_dir: str = "~/.shiftcenter/sync_queue/"):
        self.queue_dir = Path(queue_dir).expanduser()
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, path: str, content: bytes, metadata: dict) -> str:
        # Generate unique queue file ID (timestamp + uuid)
        # Write JSON file to queue_dir:
        # {
        #   "path": path,
        #   "content_base64": base64.b64encode(content).decode(),
        #   "metadata": metadata,
        #   "queued_at": ISO timestamp
        # }
        # Return queue file ID

    def list_pending(self) -> list[str]:
        # Return list of queue file IDs (filenames in queue_dir)

    async def flush(self, cloud_adapter: CloudStorageAdapter) -> dict:
        # For each queued file:
        #   - Read JSON
        #   - Decode content_base64
        #   - Call cloud_adapter.write()
        #   - If success: delete queue file
        #   - If still offline: keep queue file
        # Return { "flushed": count_success, "pending": count_failed }
```

---

## Files to Read First

**Storage adapter files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\base.py` (BaseVolumeAdapter abstract interface — 8 methods)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` (current stub — all NotImplementedError)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\local.py` (reference implementation — LocalFilesystemAdapter)

**Storage registry:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (VolumeRegistry — how adapters are registered)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\transport.py` (FileTransport — how storage routes use adapters)

**Storage routes:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (storage route handlers — request/response format)

**Config and auth:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings — cloud_url, mode)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (how to get auth token)

---

## Architecture — Files to Modify

### 1. `hivenode/storage/adapters/cloud.py`

Replace all `NotImplementedError` with real `httpx` calls.

**Key details:**
- Use `httpx.AsyncClient()` for HTTP calls
- All storage routes are POST (not GET)
- Request body is JSON
- Include `Authorization: Bearer {self.auth_token}` header
- Handle exceptions:
  - `httpx.ConnectError`, `httpx.TimeoutException`, `httpx.NetworkError` → offline (queue or raise `VolumeOfflineError`)
  - 404 → `FileNotFoundError`
  - 403 → `PermissionError`
  - 500 → raise with server error message
- For `write()`: if offline, call `sync_queue.enqueue()` instead of raising

### 2. `hivenode/storage/adapters/exceptions.py` (new file)

```python
class VolumeOfflineError(Exception):
    """Raised when a volume is unreachable."""
    pass
```

### 3. `hivenode/storage/adapters/sync_queue.py` (new file)

Implement `SyncQueue` class as described above.

---

## Test Requirements (~15 tests)

Write tests in:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py` (file already exists, update with real tests)

### test_cloud_adapter.py (~15 tests)

Use `respx` or `httpx.mock` to mock HTTP responses.

1. **read()** — mock 200 response with content → returns bytes
2. **read()** — mock 404 response → raises FileNotFoundError
3. **read()** — mock network error → raises VolumeOfflineError
4. **write()** — mock 200 response → returns metadata
5. **write()** — mock network error → enqueues in sync_queue, returns { "queued": true }
6. **list()** — mock 200 response with file list → returns list
7. **list()** — mock network error → raises VolumeOfflineError
8. **stat()** — mock 200 response with metadata → returns dict
9. **stat()** — mock 404 response → raises FileNotFoundError
10. **delete()** — mock 200 response → returns confirmation
11. **exists()** — mock 200 response → returns True
12. **exists()** — mock 404 response → returns False
13. **move()** — mock read + write + delete sequence → succeeds
14. **sync_queue.enqueue()** — writes JSON file to queue dir
15. **sync_queue.flush()** — flushes queued writes when cloud comes back online

All tests use pytest. Run with: `python -m pytest tests/hivenode/storage/test_cloud_adapter.py -v`

---

## Constraints

- No file over 500 lines.
- TDD — write tests first, then implementation.
- No stubs. Every method fully implemented.
- Use `httpx.AsyncClient()` (already in dependencies).
- Handle all error cases gracefully.
- Sync queue must persist across hivenode restarts (files on disk, not in-memory).

---

## Definition of Done

- [x] `exceptions.py` written (VolumeOfflineError exception class)
- [x] `sync_queue.py` written (SyncQueue class with enqueue, list_pending, flush methods)
- [x] `cloud.py` modified (all 8 methods replaced with real httpx calls)
- [x] JWT header included in all requests
- [x] Offline detection working (network errors → queue or raise VolumeOfflineError)
- [x] Write queueing working (offline writes go to sync_queue)
- [x] Move implemented as read + write + delete
- [x] 15 tests written and passing (`python -m pytest tests/hivenode/storage/test_cloud_adapter.py -v`)
- [x] No existing tests broken by changes

---

## Response File

Write your response to:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-TASK-030-RESPONSE.md`

Use the standard 8-section format from BOOT.md Rule 10.

---

**End of TASK-030.**
