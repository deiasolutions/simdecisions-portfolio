# Q33N Survey: Cloud Storage Adapter (SPEC-0400)

**Date:** 2026-03-14
**Q33N Bot ID:** QUEEN-QUEUE-TEMP-2026-03-14-0400-SPE
**Spec:** `.deia/hive/queue/2026-03-14-0400-SPEC-cloud-storage-adapter.md`
**Briefing:** `.deia/hive/coordination/2026-03-14-BRIEFING-cloud-storage-adapter.md`

---

## Current State

After surveying the codebase, I found that **CloudAdapter is substantially complete** but has **two blocking issues** preventing it from working with VolumeRegistry.

### What Already Exists ✅

1. **CloudAdapter class** (`hivenode/storage/adapters/cloud.py`, 292 lines)
   - ✅ Full HTTP client implementation calling cloud hivenode routes
   - ✅ JWT authentication via Authorization header
   - ✅ All CRUD methods: read(), write(), list(), stat(), delete(), exists(), move()
   - ✅ Offline detection (VolumeOfflineError)
   - ✅ Write queueing when offline

2. **SyncQueue class** (`hivenode/storage/adapters/sync_queue.py`, 130 lines)
   - ✅ Queues writes to `~/.shiftcenter/sync_queue/`
   - ✅ Flush method to retry when cloud comes back online
   - ✅ JSON format with base64-encoded content

3. **Tests** (`tests/hivenode/storage/test_cloud_adapter.py`)
   - ✅ 15 tests covering all methods + sync queue
   - ✅ All 15 tests pass (verified)
   - ✅ Uses respx to mock HTTP endpoints

4. **Registry awareness** (`hivenode/storage/registry.py`)
   - ✅ CloudAdapter import exists (line 5)
   - ✅ Instantiation logic exists (line 160)
   - ❌ **Wrong parameters passed to constructor**

---

## Blocking Issues

### Issue 1: Registry Instantiation Mismatch

**Location:** `hivenode/storage/registry.py:160`

```python
# Registry passes endpoint and bucket
adapter = CloudAdapter(endpoint, bucket)

# CloudAdapter expects cloud_url and auth_token
def __init__(self, cloud_url: str, auth_token: str, queue_dir: str = "~/.shiftcenter/sync_queue/"):
```

**Impact:** VolumeRegistry.get_adapter("cloud") will crash with TypeError (wrong number of args).

**Fix required:** Update registry line 160 to pass `cloud_url` and `auth_token` from config.

### Issue 2: Async/Sync Interface Mismatch

**Location:** `hivenode/storage/adapters/cloud.py` (all methods)

```python
# BaseVolumeAdapter interface (base.py) — SYNC
def read(self, path: str) -> bytes:
    pass

# CloudAdapter implementation — ASYNC
async def read(self, path: str) -> bytes:
    pass
```

**Impact:**
- Code calling `adapter.read(path)` expects bytes, gets coroutine
- Must await or use asyncio.run(), breaking the uniform interface
- Registry assumes sync interface

**Fix required:** Convert CloudAdapter to synchronous (httpx.Client instead of AsyncClient).

---

## Task Breakdown

I've identified **4 tasks** to complete the spec:

### TASK-077: Convert CloudAdapter to Synchronous
- File: `hivenode/storage/adapters/cloud.py`
- Change httpx.AsyncClient → httpx.Client
- Remove async/await throughout
- Estimated: Small (1-2 hours)

### TASK-078: Fix Registry Instantiation
- File: `hivenode/storage/registry.py`
- Update line 160 to pass correct parameters
- Read cloud_url + auth_token from config or environment
- Estimated: Small (< 1 hour)

### TASK-079: Update Volume Config Schema
- File: `hivenode/storage/config.py`
- Add cloud_url and auth_token to default config
- Document environment variable fallbacks
- Estimated: Small (< 1 hour)

### TASK-080: Update Tests to Sync Interface
- File: `tests/hivenode/storage/test_cloud_adapter.py`
- Remove @pytest.mark.asyncio and async/await
- All tests already pass, just need async removal
- Estimated: Small (< 1 hour)

**Total effort:** Small to Medium (4-6 hours wall time, can parallelize)

---

## Acceptance Criteria Status

From SPEC-0400:

- [x] CloudStorageAdapter class implements BaseStorageAdapter interface (exists, but async — needs sync fix)
- [x] read(), write(), list(), stat(), delete() methods call cloud hivenode over HTTPS (done)
- [x] Authentication: ra96it JWT included in all requests (done, line 34-37)
- [x] Offline behavior: VOLUME_OFFLINE error when cloud is unreachable (done, VolumeOfflineError)
- [x] Write queue: writes queued in `~/.shiftcenter/sync_queue/` when offline (done, SyncQueue)
- [x] Queue flushes when cloud comes back online (done, SyncQueue.flush())
- [ ] Adapter registered in volume registry for `cloud://` scheme (registry exists but wrong params)
- [x] 10+ tests (mock cloud endpoint) (15 tests, all pass)
- [x] No file over 500 lines (cloud.py: 292, sync_queue.py: 130)

**Summary:** 7 of 9 criteria met. 2 require fixes (registry instantiation + async/sync).

---

## Recommendation

**Proceed with 4-task plan.** The work is well-scoped, low risk, and completes the spec.

All tasks can run **sequentially** (each depends on previous):
1. TASK-077 (sync adapter) → TASK-080 (sync tests) must wait for TASK-077
2. TASK-078 (registry) depends on TASK-077 completing
3. TASK-079 (config) can run in parallel with TASK-077

**Suggested dispatch order:**
1. TASK-077 + TASK-079 in parallel (both are independent)
2. TASK-078 after TASK-077 completes (depends on sync adapter)
3. TASK-080 after TASK-077 completes (depends on sync adapter)

**Model assignment:** Haiku for all 4 (straightforward mechanical changes).

---

**Awaiting Q88NR approval to write task files.**
