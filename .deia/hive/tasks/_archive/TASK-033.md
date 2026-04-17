# TASK-033: Repo Index Routes (Part 1) — Scan, Query, Read

**Status:** READY
**Assigned to:** BEE-SONNET
**Priority:** P1
**Depends on:** TASK-032
**Blocks:** (none — can run parallel with TASK-034)
**Estimate:** S
**Created:** 2026-03-12

---

## Objective

Create FastAPI routes for scanning, querying, and reading files from the repo index. This is Phase 2 of SPEC-REPO-INDEX-001, building on the core indexer from TASK-032.

## Context

TASK-032 built the RepoIndexer class and schemas. Now we expose three routes:
- `POST /repo/scan` — trigger full re-scan
- `GET /repo/index` — query the index with filters
- `GET /repo/read` — read file contents from disk

## Acceptance Criteria

### 1. Route File (`hivenode/repo/routes.py`)

Create a new FastAPI router with three endpoints.

### 2. POST /repo/scan

Full repo re-scan endpoint.

```python
@router.post("/scan", response_model=ScanResult)
async def scan_repo(
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Trigger full repository scan.

    Walks the file tree, computes hashes, applies gitignore rules,
    upserts entries to SQLite.

    Returns:
        ScanResult with file counts and duration
    """
```

**Requirements:**
- Auth: `verify_jwt_or_local` (local bypasses JWT)
- Call `await indexer.scan()`
- Return ScanResult model
- Handle errors gracefully (500 on unexpected errors)

### 3. GET /repo/index

Query the file index with filters.

```python
@router.get("/index", response_model=IndexResult)
async def query_index(
    path: str = Query("", description="Path prefix filter"),
    ext: str | None = Query(None, description="File extension filter (e.g., .py)"),
    gitignored: str = Query("exclude", description="exclude | include | only"),
    show_all: bool = Query(False, description="Show all files including hidden"),
    hidden_only: bool = Query(False, description="Show only hidden files"),
    search: str | None = Query(None, description="Substring search on path"),
    limit: int = Query(500, ge=1, le=1000, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Query file index with filters.

    Default behavior (no params): visible=1 AND gitignored=0 ("GitHub view")

    Query params:
        path: Prefix match (e.g., "hivenode/" shows all under hivenode/)
        ext: Extension filter (e.g., ".py", ".ts")
        gitignored: exclude (default), include, only
        show_all: Override visibility, show everything
        hidden_only: Only show hidden files
        search: Substring match on path (case-insensitive)
        limit: Max results (default 500, max 1000)
        offset: Pagination offset

    Returns:
        IndexResult with matching files and total count
    """
```

**Requirements:**
- Build `IndexQuery` from query params
- Call `await indexer.query(filters)`
- Return IndexResult model
- Validate limit (1-1000)
- Handle errors (400 for validation, 500 for DB errors)

### 4. GET /repo/read

Read a single file from disk.

```python
@router.get("/read", response_model=FileContent)
async def read_file(
    path: str = Query(..., description="Relative file path"),
    encoding: str = Query("auto", description="auto | utf-8 | base64"),
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Read file contents from disk (always fresh, not from DB).

    Security:
        - Rejects path traversal (..)
        - Rejects absolute paths
        - Blocks .git/ access (403)
        - Size limit: 10 MB

    Auto-detection (encoding="auto"):
        Text extensions: .py, .ts, .tsx, .js, .jsx, .md, .json, .yml, .yaml,
        .toml, .css, .html, .sql, .sh, .bat, .txt, .cfg, .ini, .env, .egg.md
        Binary: everything else (base64)

    Args:
        path: Relative path from repo root
        encoding: auto (default), utf-8, base64

    Returns:
        FileContent with content as UTF-8 or base64 string

    Raises:
        400: Path validation error
        403: Forbidden (.git/ access)
        404: File not found
        500: Unexpected error
    """
```

**Requirements:**
- Call `await indexer.read_file(path, encoding)`
- Map exceptions to HTTP status codes:
  - `ValueError` → 400 (path traversal, invalid path)
  - `PermissionError` → 403 (.git/ access)
  - `FileNotFoundError` → 404
  - Generic `Exception` → 500
- Return FileContent model

### 5. Dependency Injection (`hivenode/dependencies.py`)

Add a new dependency for getting the RepoIndexer instance:

```python
# Global instance (initialized in lifespan)
_repo_indexer: Optional[RepoIndexer] = None

def set_repo_indexer(indexer: RepoIndexer):
    """Set global repo indexer."""
    global _repo_indexer
    _repo_indexer = indexer

def get_repo_indexer() -> RepoIndexer:
    """Dependency: Get repo indexer."""
    if _repo_indexer is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repo indexer not initialized"
        )
    return _repo_indexer
```

**Note:** This is wired up in `main.py` during lifespan startup (TASK-034 handles that).

### 6. Route Tests (`tests/hivenode/repo/test_repo_routes.py`)

Write route-level tests using FastAPI TestClient:

#### Test Setup
```python
@pytest.fixture
def test_app(test_repo, tmp_path):
    """Create test FastAPI app with RepoIndexer."""
    from fastapi import FastAPI
    from hivenode.repo.routes import router
    from hivenode.repo.indexer import RepoIndexer
    from hivenode import dependencies

    app = FastAPI()
    app.include_router(router, prefix="/repo")

    # Initialize indexer
    db_path = tmp_path / "test-index.db"
    indexer = RepoIndexer(repo_root=test_repo, db_path=db_path)

    # Set in dependencies
    dependencies.set_repo_indexer(indexer)

    return app

@pytest.fixture
def client(test_app):
    """Create test client."""
    from fastapi.testclient import TestClient
    return TestClient(test_app)
```

#### POST /repo/scan Tests
- `test_scan_success` — POST /repo/scan returns 200 with counts
- `test_scan_returns_scan_result` — Response matches ScanResult schema
- `test_scan_without_auth_local_mode` — Works in local mode without JWT

#### GET /repo/index Tests
- `test_index_default_view` — No params returns visible + non-gitignored files
- `test_index_path_filter` — `?path=src/` returns only files under src/
- `test_index_extension_filter` — `?ext=.py` returns only .py files
- `test_index_gitignored_include` — `?gitignored=include` shows all visible files
- `test_index_gitignored_only` — `?gitignored=only` shows only gitignored files
- `test_index_show_all` — `?show_all=true` includes hidden files
- `test_index_hidden_only` — `?hidden_only=true` shows only hidden files
- `test_index_search` — `?search=main` returns paths containing "main"
- `test_index_pagination` — `?limit=5&offset=0` returns first 5, `offset=5` returns next 5
- `test_index_limit_validation` — `?limit=2000` returns 400 (max is 1000)

#### GET /repo/read Tests
- `test_read_text_file` — Read .py file returns UTF-8 content
- `test_read_binary_file` — Read .png file returns base64 content
- `test_read_explicit_utf8` — `?encoding=utf-8` forces UTF-8
- `test_read_explicit_base64` — `?encoding=base64` forces base64
- `test_read_not_found` — Missing file returns 404
- `test_read_path_traversal` — `?path=../../../etc/passwd` returns 400
- `test_read_absolute_path` — `?path=/etc/passwd` returns 400
- `test_read_git_forbidden` — `?path=.git/config` returns 403
- `test_read_missing_path_param` — No path param returns 422 (validation error)

#### Auth Tests (if not in local mode)
- `test_scan_requires_auth_cloud_mode` — In cloud mode, missing JWT returns 401
- `test_index_requires_auth_cloud_mode` — In cloud mode, missing JWT returns 401
- `test_read_requires_auth_cloud_mode` — In cloud mode, missing JWT returns 401

Minimum: 24 passing tests.

### 7. Error Handling

All routes should return JSON error responses:

```python
try:
    # ... operation ...
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except PermissionError:
    raise HTTPException(status_code=403, detail="Access forbidden")
except FileNotFoundError:
    raise HTTPException(status_code=404, detail="File not found")
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-REPO-INDEX-001.md` — full spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` — route pattern reference
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — dependency injection pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_storage_routes.py` — route test pattern
- Output from TASK-032 (schemas.py, indexer.py)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_repo_routes.py`

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — add `get_repo_indexer()` and `set_repo_indexer()`

## Constraints

- **NO STUBS.** Every route fully implemented.
- **TDD.** Write tests first, then routes.
- **No file over 500 lines.** If routes.py approaches 500, split into multiple files.
- Follow existing route patterns from `storage_routes.py`
- Use Pydantic models for request/response validation
- Auth via `verify_jwt_or_local` dependency
- All file paths relative to repo root
- JSON responses for all errors

## Success Criteria

- All tests pass: `pytest tests/hivenode/repo/test_repo_routes.py -v`
- Routes work correctly via TestClient
- Error handling covers all edge cases
- Auth works in both local and cloud modes
- Code follows hivenode conventions

---

**Model:** sonnet
**Estimate:** S (2-3 hours)

*Ready for dispatch after TASK-032 completes.*
