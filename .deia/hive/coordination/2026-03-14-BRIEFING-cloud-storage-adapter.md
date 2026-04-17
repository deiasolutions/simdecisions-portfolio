# BRIEFING: Cloud Storage Adapter Completion

**Date:** 2026-03-14
**From:** Q33N
**To:** Q88NR (Regent)
**Spec:** `.deia/hive/queue/2026-03-14-0400-SPEC-cloud-storage-adapter.md`
**Priority:** P1

---

## Current State Assessment

After reading the codebase, I found that **CloudAdapter already exists** and is substantially complete:

### What Already Exists

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py`

The CloudAdapter class already implements:
- ✅ HTTP client calling cloud hivenode's `/storage/*` routes
- ✅ JWT authentication via `Authorization: Bearer` header
- ✅ Offline detection (ConnectError, TimeoutException, NetworkError)
- ✅ VolumeOfflineError raised for offline reads
- ✅ Write queue via SyncQueue when offline
- ✅ All CRUD methods: read(), write(), list(), stat(), delete(), exists(), move()

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py`

The SyncQueue class already implements:
- ✅ Queue directory at `~/.shiftcenter/sync_queue/`
- ✅ Enqueue writes when offline (JSON files with base64 content)
- ✅ Flush method to retry queued writes when cloud comes back online
- ✅ Proper cleanup (delete queue files on success, keep on failure)

---

## The Problem: Registry Instantiation Mismatch

**Critical issue:** VolumeRegistry.get_adapter() instantiates CloudAdapter with wrong parameters.

```python
# Registry line 160 — passes endpoint and bucket
adapter = CloudAdapter(endpoint, bucket)

# CloudAdapter __init__ signature — expects cloud_url and auth_token
def __init__(self, cloud_url: str, auth_token: str, queue_dir: str = ...):
```

**Additional issue:** BaseVolumeAdapter defines **sync** methods, but CloudAdapter implements **async** methods.

```python
# BaseVolumeAdapter (base.py) — SYNC interface
def read(self, path: str) -> bytes:
    pass

# CloudAdapter (cloud.py) — ASYNC implementation
async def read(self, path: str) -> bytes:
    pass
```

This mismatch means:
1. Registry can't instantiate CloudAdapter (parameter mismatch on line 160)
2. CloudAdapter methods are async but BaseVolumeAdapter expects sync
3. Any code calling adapter methods must await, breaking the interface contract

---

## Two Possible Solutions

### Option A: Make CloudAdapter Synchronous (Recommended)

Change CloudAdapter to use **synchronous httpx.Client** instead of async. This matches the BaseVolumeAdapter interface and works with the existing VolumeRegistry.

**Pros:**
- No changes to BaseVolumeAdapter or VolumeRegistry
- Works with existing route handlers (if they're sync)
- Simple, consistent interface

**Cons:**
- httpx sync client still works, just blocks
- Less concurrent throughput (not a problem for single-file ops)

### Option B: Make BaseVolumeAdapter Asynchronous

Change BaseVolumeAdapter to async methods, update LocalFilesystemAdapter, update VolumeRegistry to async, update all route handlers to async.

**Pros:**
- More idiomatic for I/O-bound operations
- Better concurrency for cloud ops

**Cons:**
- Breaking change across the entire storage system
- Requires updating many files (local adapter, registry, routes)
- Higher risk, more test changes

---

## Recommendation

**Go with Option A: Make CloudAdapter synchronous.**

This is the minimal change that completes the spec's acceptance criteria without breaking existing code. The cloud adapter is called infrequently (single file reads/writes), so blocking I/O is acceptable.

---

## What Needs to Be Done

### Task 1: Convert CloudAdapter to Synchronous (TASK-077)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py`

**Changes:**
- Replace `httpx.AsyncClient` with `httpx.Client`
- Remove `async` from all methods (read, write, list, stat, delete, exists, move)
- Remove `await` from client calls
- Update close() method to sync (client.close() instead of await client.aclose())
- Update SyncQueue.flush() calls (if any)

**Estimated lines:** ~150 (existing file, minor edits throughout)

### Task 2: Fix Registry Instantiation for CloudAdapter (TASK-078)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`

**Current problem:** Line 160 calls `CloudAdapter(endpoint, bucket)` but CloudAdapter expects `(cloud_url, auth_token, queue_dir)`.

**Changes:**
- Read `cloud_url` from config (or fall back to `endpoint_url`)
- Read `auth_token` from config or environment variable `HIVENODE_RA96IT_TOKEN`
- Pass correct parameters to CloudAdapter constructor
- Optionally pass `queue_dir` from config if specified

**Estimated lines:** ~15 (edits to get_adapter() method)

### Task 3: Update Volume Config Schema (TASK-079)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\config.py`

**Changes:**
- Update default cloud volume config (line 123-130) to include `cloud_url` and `auth_token` keys
- Document that `cloud_url` defaults to `HIVENODE_CLOUD_URL` env var or Railway URL
- Document that `auth_token` defaults to `HIVENODE_RA96IT_TOKEN` env var
- Keep backward compatibility with `endpoint_url` if present

**Estimated lines:** ~20 (config additions + docstring updates)

### Task 4: Update Tests to Match Sync Interface (TASK-080)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py`

**Current status:** 15 tests, all pass, all use `@pytest.mark.asyncio` and `await`

**Changes:**
- Remove `@pytest.mark.asyncio` decorators
- Remove `async` from test functions
- Remove `await` from adapter method calls
- Update respx mocks if needed for sync httpx.Client

**Estimated lines:** ~100 (existing file, remove async throughout)

---

## Files to Read (For Bees)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\base.py` (interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` (current async impl)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py` (queue impl)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (config schema)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 5)

---

## Acceptance Criteria (From Spec)

- [ ] CloudStorageAdapter class implements BaseStorageAdapter interface (currently async, needs sync fix)
- [ ] read(), write(), list(), stat(), delete() methods call cloud hivenode over HTTPS (already done)
- [ ] Authentication: ra96it JWT included in all requests (already done)
- [ ] Offline behavior: VOLUME_OFFLINE error when cloud is unreachable (already done)
- [ ] Write queue: writes queued in `~/.shiftcenter/sync_queue/` when offline (already done)
- [ ] Queue flushes when cloud comes back online (already done)
- [ ] Adapter registered in volume registry for `cloud://` scheme (needs work)
- [ ] 10+ tests (mock cloud endpoint) (missing)
- [ ] No file over 500 lines (cloud.py is 292 lines, sync_queue.py is 130 lines — both OK)

---

## Summary

Most of the work is already done. The spec was written before the CloudAdapter was implemented (or the implementation happened in parallel). What remains:

1. **Fix sync/async mismatch** (convert CloudAdapter to sync)
2. **Wire registry** (config for cloud_url + auth_token)
3. **Write tests** (13+ test cases with mocked endpoint)

Estimated effort: **Small to Medium** (1 bee for conversion, 1 bee for tests, total 2 tasks).

---

**Awaiting Q88NR approval to create task files.**
