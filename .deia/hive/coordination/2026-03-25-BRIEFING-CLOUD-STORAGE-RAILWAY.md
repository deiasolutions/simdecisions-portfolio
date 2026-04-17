# BRIEFING: Cloud Storage Backend on Railway

**Date:** 2026-03-25
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Priority:** P1
**Model Assignment:** Sonnet

---

## Objective

Implement server-side cloud storage on Railway hivenode backed by PostgreSQL. Enable signed-in users to get persistent 10 MB cloud storage with quota tracking and namespace isolation. Visitors (no auth) get export-only — no cloud writes without JWT.

---

## Context from Q88N

The current `CloudAdapter` (hivenode/storage/adapters/cloud.py) is an HTTP client that calls cloud hivenode's `/storage/*` routes. However, **those server-side routes don't exist yet**. They need to be implemented.

Currently, `storage_routes.py` uses `verify_jwt_or_local()` which bypasses auth for local development. For cloud deployment on Railway, we need:

1. **Server-side storage routes** (`/storage/write`, `/storage/read`, `/storage/list`, `/storage/stat`, `/storage/delete`) backed by PostgreSQL table storing file content
2. **Quota tracking table** in PostgreSQL — track bytes used per user, enforce 10 MB limit
3. **GET /storage/quota** endpoint — return current usage for authenticated user
4. **Namespace isolation** — users can only access `cloud://{user_id}/path/to/file` (their own namespace)
5. **JWT auth required** — cloud writes require JWT (visitors get 401), but visitor export (download) works without auth
6. **Documentation** — encryption at rest applies to Railway PostgreSQL only, user-added volumes are user's responsibility

---

## Storage Architecture

### Current State (Local Hivenode)

- `storage_routes.py`: `/storage/*` routes use `FileTransport` which calls `VolumeRegistry` → `LocalFilesystemAdapter`
- `CloudAdapter`: HTTP client that makes requests to cloud hivenode `/storage/*` routes
- `SyncQueue`: Queues writes when cloud is offline, flushes when reconnected

### Target State (Cloud Hivenode on Railway)

- Railway hivenode serves `/storage/*` routes backed by **PostgreSQL table** (not local filesystem)
- Table schema:
  ```sql
  CREATE TABLE cloud_files (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    path TEXT NOT NULL,
    content BYTEA NOT NULL,
    size INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, path)
  );

  CREATE INDEX idx_cloud_files_user ON cloud_files(user_id);
  ```

- Quota tracking table:
  ```sql
  CREATE TABLE cloud_quotas (
    user_id TEXT PRIMARY KEY,
    bytes_used BIGINT DEFAULT 0,
    quota_bytes BIGINT DEFAULT 10485760,  -- 10 MB
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

### Namespace Isolation

URIs are formatted as: `cloud://{user_id}/path/to/file.txt`

- Extract `user_id` from JWT claims (`claims['sub']`)
- Validate that `user_id` in URI matches `claims['sub']`
- Return 403 if user tries to access another user's namespace

### Quota Enforcement

Before write:
1. Check current `bytes_used` from `cloud_quotas` table
2. Add size of new file content
3. If `bytes_used + new_size > quota_bytes`, return 400 with error: `{"error": "quota_exceeded", "quota_bytes": 10485760, "bytes_used": 10000000}`
4. If quota OK, insert/update file in `cloud_files` table
5. Update `bytes_used` in `cloud_quotas` table

### Visitor Export (No Auth)

- Visitor can **download** (export) files they create locally
- Visitor **cannot write to cloud storage** (401 on cloud writes without JWT)
- The export flow happens client-side (browser download), not through cloud storage

---

## Files to Read First

- `hivenode/routes/storage_routes.py` — current storage routes (local filesystem)
- `hivenode/storage/adapters/cloud.py` — HTTP client for cloud storage
- `hivenode/storage/config.py` — volume configuration
- `hivenode/sync/engine.py` — sync engine (SyncQueue flushes to cloud)
- `hivenode/storage/adapters/base.py` — BaseVolumeAdapter interface
- `hivenode/dependencies.py` — `verify_jwt()`, `verify_jwt_or_local()`
- `hivenode/database.py` — SQLAlchemy setup (if exists)
- `hivenode/main.py` — FastAPI app registration
- `hivenode/routes/__init__.py` — route registration

---

## Files to Modify

### New Files to Create

1. **`hivenode/storage/cloud_store.py`** — PostgreSQL store for cloud files and quota tracking
   - `write_file(user_id, path, content) -> dict`
   - `read_file(user_id, path) -> bytes`
   - `list_files(user_id, path) -> List[str]`
   - `stat_file(user_id, path) -> dict`
   - `delete_file(user_id, path) -> dict`
   - `get_quota(user_id) -> dict`
   - `update_quota(user_id, delta_bytes) -> None`
   - Uses SQLAlchemy Core or raw SQL with `psycopg2`

2. **`hivenode/routes/cloud_storage_routes.py`** — Cloud-specific storage routes
   - `POST /storage/write` — requires JWT, enforces quota, namespace isolation
   - `GET /storage/read` — requires JWT, namespace isolation
   - `GET /storage/list` — requires JWT, namespace isolation
   - `GET /storage/stat` — requires JWT, namespace isolation
   - `DELETE /storage/delete` — requires JWT, namespace isolation
   - `GET /storage/quota` — requires JWT, returns usage for user

3. **`tests/hivenode/test_cloud_storage.py`** — TDD tests for cloud storage
   - Quota enforcement (reject write when quota exceeded)
   - Namespace isolation (user A cannot access user B's files)
   - JWT auth rejection (401 without JWT)
   - Write/read/list/stat/delete operations
   - Quota endpoint returns correct usage

### Files to Modify

1. **`hivenode/main.py`** — Register `cloud_storage_routes.router` (conditionally for cloud deployment)
2. **`hivenode/routes/__init__.py`** — Import and include cloud storage routes
3. **`hivenode/storage/config.py`** — Add `get_database_url()` helper for cloud PostgreSQL connection

---

## Deliverables (from Spec)

- [ ] Cloud storage routes: `/storage/write`, `/storage/read`, `/storage/list`, `/storage/stat`, `/storage/delete` on cloud hivenode
- [ ] Quota tracking table and enforcement (10 MB per user)
- [ ] `GET /storage/quota` endpoint for authenticated user
- [ ] Visitor export support (no cloud writes without JWT)
- [ ] Wire existing CloudAdapter to new server-side routes
- [ ] Tests for quota enforcement, namespace isolation, auth rejection

---

## Acceptance Criteria (from Spec)

- [ ] Cloud hivenode serves `/storage/*` routes backed by PostgreSQL
- [ ] Per-user namespace isolation (users cannot access other users' files)
- [ ] 10 MB quota enforced per user
- [ ] Quota check returns structured error on exceed: `{"error": "quota_exceeded", "quota_bytes": 10485760, "bytes_used": <current>}`
- [ ] `GET /storage/quota` returns usage for authenticated user: `{"bytes_used": 1234, "quota_bytes": 10485760}`
- [ ] Visitors get no cloud storage (401 on cloud writes without JWT)
- [ ] Visitor export (download) works without auth — **NOTE: This is client-side, not server-side. No changes needed.**
- [ ] Encryption at rest on server DB only — **documented in README or deployment docs**
- [ ] User-added endpoints security is user's responsibility — **documented**
- [ ] SyncQueue flushes to cloud storage — **already implemented in CloudAdapter + SyncQueue, no changes needed**
- [ ] Tests for quota enforcement, namespace isolation, auth rejection

---

## Test Requirements

### Unit Tests (TDD)

File: `tests/hivenode/test_cloud_storage.py`

Minimum 15 tests covering:

1. **Quota enforcement:**
   - Write file within quota → success
   - Write file exceeding quota → 400 error with structured response
   - Multiple writes accumulate quota correctly

2. **Namespace isolation:**
   - User A writes `cloud://userA/file.txt` → success
   - User B reads `cloud://userA/file.txt` → 403 (access denied)
   - User A reads `cloud://userA/file.txt` → success

3. **JWT auth rejection:**
   - Write without JWT → 401
   - Read without JWT → 401
   - List without JWT → 401
   - Stat without JWT → 401
   - Delete without JWT → 401
   - GET /quota without JWT → 401

4. **CRUD operations:**
   - Write → read → verify content matches
   - List → verify file appears
   - Stat → verify size/modified/created
   - Delete → verify file removed

5. **Quota endpoint:**
   - GET /quota returns correct `bytes_used` after writes
   - GET /quota returns `quota_bytes = 10485760`

### Integration Tests

File: `tests/hivenode/test_cloud_storage_integration.py`

Minimum 5 tests covering:

1. Full workflow: write multiple files → list → stat → read → delete
2. Quota updates across write/delete operations
3. Concurrent writes by different users (namespace isolation)
4. Error handling: 404 on read nonexistent file, 400 on invalid path
5. SyncQueue flush to cloud storage (mock cloud hivenode, verify CloudAdapter calls)

---

## Constraints (from Spec)

- **TDD** — tests first, then implementation
- **500-line limit per file** — modularize at 500, hard limit 1,000
- **Python 3.13**
- **JWT auth via ra96it/hodeia** — use `verify_jwt()` dependency
- **PostgreSQL on Railway** — connection string from env var `DATABASE_URL`
- **No encryption on user-declared custom volumes** — document this
- **Per-user namespace:** `cloud://{user_id}/path/to/file`
- **Storage backed by Railway PostgreSQL** — file content as `BYTEA` in `cloud_files` table

---

## Implementation Notes

### PostgreSQL Connection

Use `hivenode/database.py` if it exists, otherwise create SQLAlchemy engine:

```python
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
```

### URI Parsing for Namespace Extraction

```python
def parse_cloud_uri(uri: str) -> tuple[str, str]:
    """Parse cloud://user_id/path/to/file -> (user_id, path)"""
    if not uri.startswith("cloud://"):
        raise ValueError("Invalid cloud URI")

    rest = uri[8:]  # remove "cloud://"
    parts = rest.split("/", 1)

    if len(parts) < 2:
        raise ValueError("Cloud URI must include user_id and path")

    user_id = parts[0]
    path = parts[1]

    return user_id, path
```

### Quota Check Logic

```python
def check_quota(user_id: str, new_size: int) -> None:
    """Raise HTTPException(400) if quota would be exceeded."""
    quota_row = get_quota(user_id)

    if quota_row["bytes_used"] + new_size > quota_row["quota_bytes"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "quota_exceeded",
                "quota_bytes": quota_row["quota_bytes"],
                "bytes_used": quota_row["bytes_used"]
            }
        )
```

### Namespace Isolation Check

```python
def verify_namespace_access(uri: str, claims: dict) -> tuple[str, str]:
    """Verify user can access this namespace, return (user_id, path)."""
    user_id_from_uri, path = parse_cloud_uri(uri)
    user_id_from_jwt = claims["sub"]

    if user_id_from_uri != user_id_from_jwt:
        raise HTTPException(
            status_code=403,
            detail="Access denied: cannot access other users' namespaces"
        )

    return user_id_from_uri, path
```

---

## Deployment Environment Detection

Cloud routes should only be registered on Railway (cloud deployment), not local dev.

In `hivenode/main.py`:

```python
import os

# Register cloud storage routes only on Railway
if os.getenv("RAILWAY_ENVIRONMENT"):
    from hivenode.routes import cloud_storage_routes
    app.include_router(cloud_storage_routes.router, prefix="/storage")
else:
    # Local dev uses existing storage_routes.py
    from hivenode.routes import storage_routes
    app.include_router(storage_routes.router, prefix="/storage")
```

---

## Documentation Requirements

Create or update:

1. **`docs/CLOUD-STORAGE.md`** — Document:
   - Encryption at rest: Railway PostgreSQL only
   - User-added volumes: User's responsibility (no encryption, no security guarantees)
   - Quota limits: 10 MB per user (free tier)
   - Namespace isolation: Users cannot access other users' files
   - Visitor export: Client-side download, no cloud storage

2. **`docs/DEPLOYMENT.md`** — Add section:
   - Railway deployment requires `DATABASE_URL` env var
   - Cloud storage routes registered only when `RAILWAY_ENVIRONMENT` is set

---

## Smoke Test (from Spec)

```bash
cd hivenode && python -m pytest tests/hivenode/ -v -k storage
cd hivenode && python -m pytest tests/ -v  # no regressions
```

---

## What Q33N Should Do

1. **Read the files listed above** to understand current architecture
2. **Write task files** breaking down the work into bee-sized units:
   - **TASK-A:** Create `cloud_store.py` + tests (TDD)
   - **TASK-B:** Create `cloud_storage_routes.py` + tests (TDD)
   - **TASK-C:** Wire routes into `main.py` + conditional registration
   - **TASK-D:** Document cloud storage + deployment
   - **TASK-E:** Integration tests for full workflow

3. **Return task files to Q33NR for review** — do NOT dispatch bees yet
4. **After Q33NR approval:** Dispatch bees sequentially (TASK-A first, then TASK-B depends on TASK-A)

---

## Questions to Resolve Before Task Files

1. Does `hivenode/database.py` exist? If not, how should we connect to PostgreSQL?
2. Does Railway set `RAILWAY_ENVIRONMENT` env var? If not, what env var should we check?
3. Should quota table use `BIGINT` (bytes) or `INTEGER` (bytes)? 10 MB = 10,485,760 bytes fits in INTEGER.
4. Should `cloud_files` table include `content_hash` column for deduplication? (Optional, not in spec.)

---

## Expected Response from Q33N

After reading the codebase:

1. Confirmation of PostgreSQL connection method
2. List of task files created (TASK-A through TASK-E)
3. Summary of deliverables per task
4. Confirmation that all acceptance criteria are covered
5. Test count per task (minimum 15 unit + 5 integration = 20 total)

---

**Q33NR awaits Q33N's task files for review.**
