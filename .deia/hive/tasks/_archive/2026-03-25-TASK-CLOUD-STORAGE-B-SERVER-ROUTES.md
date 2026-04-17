# TASK-CLOUD-STORAGE-B: Cloud Storage Server Routes (TDD)

## Objective

Create FastAPI routes for cloud storage (`cloud_storage_routes.py`) backed by PostgreSQL store. Routes enforce JWT auth, namespace isolation, and quota limits. Wire into main.py conditionally for cloud deployment only.

---

## Context

TASK-CLOUD-STORAGE-A created the PostgreSQL store (`cloud_store.py`). This task creates the HTTP routes that call the store. These routes serve as the server-side implementation that `CloudAdapter` (HTTP client) calls.

Routes:
- `POST /storage/write` — write file, enforce quota
- `GET /storage/read` — read file
- `GET /storage/list` — list directory
- `GET /storage/stat` — file metadata
- `DELETE /storage/delete` — delete file
- `GET /storage/quota` — current quota usage

All routes require JWT auth (no `verify_jwt_or_local` — cloud requires auth). Extract `user_id` from JWT `sub` claim for namespace isolation.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\cloud_store.py` — PostgreSQL store (TASK-A output)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` — existing local storage routes (pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — `verify_jwt()` dependency
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` — request/response schemas (if needed)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — route registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — router imports

---

## Deliverables

- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\cloud_storage_routes.py` (TDD)
- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_cloud_storage_routes.py` (tests first)
- [ ] 6 endpoints: `/storage/write`, `/storage/read`, `/storage/list`, `/storage/stat`, `/storage/delete`, `/storage/quota`
- [ ] All routes use `verify_jwt()` dependency (no bypass)
- [ ] Namespace validation: extract `user_id` from JWT, pass to store functions
- [ ] Error handling: 400 for quota exceeded, 403 for namespace violation, 404 for file not found, 401 for missing/invalid JWT
- [ ] Routes registered in `main.py` conditionally (cloud mode only)
- [ ] Routes registered in `__init__.py`
- [ ] Tests pass: minimum 20 tests

---

## Test Requirements (TDD — Write Tests First)

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_cloud_storage_routes.py`

Minimum 20 tests covering:

### JWT Auth Rejection (6 tests)
1. POST /storage/write without JWT → 401
2. GET /storage/read without JWT → 401
3. GET /storage/list without JWT → 401
4. GET /storage/stat without JWT → 401
5. DELETE /storage/delete without JWT → 401
6. GET /storage/quota without JWT → 401

### Quota Enforcement (3 tests)
7. Write file within quota → 200 OK
8. Write file exceeding quota → 400 with `{"error": "quota_exceeded", "bytes_used": X, "quota_bytes": 10485760}`
9. Multiple writes accumulate quota correctly

### Namespace Isolation (3 tests)
10. User A writes `cloud://userA/file.txt` → 200 OK
11. User B reads `cloud://userA/file.txt` → 403 (namespace violation)
12. User A lists `cloud://userA/` → only sees their files

### CRUD Operations (6 tests)
13. Write file → read file → content matches
14. Write file → stat file → size correct
15. Write file → list directory → file appears
16. Delete file → read file → 404
17. Read nonexistent file → 404
18. Delete nonexistent file → 404

### Quota Endpoint (2 tests)
19. GET /quota after write → returns correct `bytes_used` and `quota_bytes`
20. GET /quota for new user → returns `bytes_used=0`, `quota_bytes=10485760`

---

## Implementation Notes

### Route Signatures

Use FastAPI `Depends(verify_jwt)` on all routes. Extract `user_id = claims['sub']`.

**POST /storage/write**
```python
@router.post("/write", response_model=StorageWriteResponse)
async def write_file(
    request: StorageWriteRequest,
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    # Decode base64 content
    content = base64.b64decode(request.content_base64)
    # Write file via store
    try:
        result = cloud_store.write_file(request.uri, content, user_id)
        return StorageWriteResponse(ok=True, uri=request.uri)
    except cloud_store.QuotaExceededError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "quota_exceeded",
                "bytes_used": e.bytes_used,
                "quota_bytes": e.quota_bytes
            }
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Namespace access denied")
```

**GET /storage/read**
```python
@router.get("/read")
async def read_file(
    uri: str = Query(...),
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    try:
        content = cloud_store.read_file(uri, user_id)
        return Response(content=content, media_type="application/octet-stream")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Namespace access denied")
```

**GET /storage/list**
```python
@router.get("/list", response_model=StorageListResponse)
async def list_directory(
    uri: str = Query(...),
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    try:
        entries = cloud_store.list_files(uri, user_id)
        return StorageListResponse(entries=entries)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Namespace access denied")
```

**GET /storage/stat**
```python
@router.get("/stat", response_model=StorageStatResponse)
async def stat_file(
    uri: str = Query(...),
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    try:
        metadata = cloud_store.stat_file(uri, user_id)
        return StorageStatResponse(**metadata)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Namespace access denied")
```

**DELETE /storage/delete**
```python
@router.delete("/delete", response_model=StorageDeleteResponse)
async def delete_file(
    uri: str = Query(...),
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    try:
        cloud_store.delete_file(uri, user_id)
        return StorageDeleteResponse(ok=True)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Namespace access denied")
```

**GET /storage/quota**
```python
@router.get("/quota")
async def get_quota(
    claims: dict = Depends(verify_jwt)
):
    user_id = claims["sub"]
    quota = cloud_store.get_quota(user_id)
    return quota
```

### Wire Routes into main.py (Conditional Registration)

In `hivenode/main.py`, register cloud storage routes only in cloud mode:

```python
# Cloud storage routes (Railway deployment only)
if settings.mode == "cloud":
    from hivenode.routes import cloud_storage_routes
    # Replace local storage routes with cloud storage routes
    app.include_router(cloud_storage_routes.router, prefix="/storage", tags=["storage"])
else:
    # Local/remote: use existing local filesystem storage routes
    # (already registered in create_router())
    pass
```

**IMPORTANT:** Do NOT register both `storage_routes` and `cloud_storage_routes` at the same time. Cloud mode uses `cloud_storage_routes` (PostgreSQL). Local/remote modes use `storage_routes` (local filesystem).

### Update routes/__init__.py

Add import:
```python
from hivenode.routes import cloud_storage_routes
```

---

## Constraints

- **TDD:** Write tests first, then implementation
- **File size limit:** 500 lines for `cloud_storage_routes.py`
- **JWT auth required:** Use `Depends(verify_jwt)`, NOT `verify_jwt_or_local`
- **No stubs:** All routes fully implemented
- **Python 3.13**
- **Type hints:** All functions must have complete type annotations
- **Error responses:** Structured JSON for quota exceeded, namespace violations

---

## Acceptance Criteria

- [ ] `cloud_storage_routes.py` created with 6 endpoints
- [ ] All routes use `verify_jwt()` dependency
- [ ] Namespace isolation: `user_id` extracted from JWT, passed to store
- [ ] Quota exceeded error: 400 with structured JSON `{"error": "quota_exceeded", ...}`
- [ ] Namespace violation error: 403
- [ ] File not found error: 404
- [ ] Missing/invalid JWT error: 401
- [ ] Routes registered in `main.py` conditionally (cloud mode only)
- [ ] Routes imported in `routes/__init__.py`
- [ ] Tests written FIRST (TDD)
- [ ] All 20+ tests pass
- [ ] No file exceeds 500 lines
- [ ] No stubs
- [ ] Type hints on all functions

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-CLOUD-STORAGE-B-RESPONSE.md`

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

---

## Dependencies

- **TASK-CLOUD-STORAGE-A** must complete first (provides `cloud_store.py`)

---

## Test Command

```bash
cd hivenode && python -m pytest tests/hivenode/routes/test_cloud_storage_routes.py -v
```
