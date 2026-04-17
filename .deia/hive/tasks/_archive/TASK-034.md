# TASK-034: Repo Index Routes (Part 2) — Tree, Visibility, Stats, Wiring

**Status:** READY
**Assigned to:** BEE-SONNET
**Priority:** P1
**Depends on:** TASK-032
**Blocks:** (none — can run parallel with TASK-033)
**Estimate:** S
**Created:** 2026-03-12

---

## Objective

Complete the Repo Index Service by adding remaining routes (tree, visibility, stats), wiring the RepoIndexer into hivenode startup, adding the route to the main router, and adding the `pathspec` dependency to pyproject.toml.

## Context

TASK-032 built the core indexer, TASK-033 added scan/query/read routes. This task completes the API surface and integrates everything into the running hivenode.

## Acceptance Criteria

### 1. Additional Routes (`hivenode/repo/routes.py`)

Add three more endpoints to the existing router:

#### GET /repo/tree

```python
@router.get("/tree", response_model=TreeNode)
async def get_tree(
    path: str = Query("", description="Path prefix filter"),
    ext: str | None = Query(None, description="File extension filter"),
    gitignored: str = Query("exclude", description="exclude | include | only"),
    show_all: bool = Query(False, description="Show all files including hidden"),
    hidden_only: bool = Query(False, description="Show only hidden files"),
    search: str | None = Query(None, description="Substring search on path"),
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Get directory tree structure.

    Returns nested JSON representing the folder hierarchy.
    Same filter params as /repo/index.

    Returns:
        TreeNode representing root with nested children
    """
```

**Requirements:**
- Build `IndexQuery` from query params
- Call `await indexer.tree(filters)`
- Return TreeNode model
- Handle errors (400 for validation, 500 for DB errors)

#### PATCH /repo/visibility

```python
@router.patch("/visibility")
async def set_visibility(
    request: SetVisibilityRequest,
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Toggle visibility for a file or directory.

    If path is a directory, recursively updates all descendants.

    Request body:
        {
            "path": ".deia/hive/responses/",
            "visible": false
        }

    Returns:
        {
            "ok": true,
            "affected": 47
        }
    """
```

**Requirements:**
- Define `SetVisibilityRequest` schema in `schemas.py`:
  ```python
  class SetVisibilityRequest(BaseModel):
      path: str
      visible: bool

  class SetVisibilityResponse(BaseModel):
      ok: bool
      affected: int
  ```
- Call `await indexer.set_visibility(request.path, request.visible)`
- Return `SetVisibilityResponse` with affected row count
- Handle errors (400 for invalid path, 500 for DB errors)

#### GET /repo/stats

```python
@router.get("/stats", response_model=RepoStats)
async def get_stats(
    claims: dict = Depends(verify_jwt_or_local),
    indexer: RepoIndexer = Depends(get_repo_indexer)
):
    """
    Get repository statistics.

    Returns summary counts, extension breakdown, and last scan time.

    Returns:
        RepoStats model
    """
```

**Requirements:**
- Call `await indexer.stats()`
- Return RepoStats model
- Handle errors (500 for DB errors)

### 2. Route Registration (`hivenode/routes/__init__.py`)

Add repo router to the main router:

```python
from hivenode.routes import health, auth, ledger_routes, storage_routes, node, llm_routes, shell, repo

def create_router() -> APIRouter:
    """Create and configure all routes."""
    router = APIRouter()

    # Mount all route modules
    router.include_router(health.router, tags=['health'])
    router.include_router(auth.router, prefix='/auth', tags=['auth'])
    router.include_router(ledger_routes.router, prefix='/ledger', tags=['ledger'])
    router.include_router(storage_routes.router, prefix='/storage', tags=['storage'])
    router.include_router(node.router, prefix='/node', tags=['node'])
    router.include_router(llm_routes.router, prefix='/llm', tags=['llm'])
    router.include_router(shell.router, prefix='/shell', tags=['shell'])
    router.include_router(repo.router, prefix='/repo', tags=['repo'])  # NEW

    return router
```

### 3. Repo Module Export (`hivenode/repo/__init__.py`)

Export the router:

```python
"""Repo file index module."""
from hivenode.repo.routes import router

__all__ = ['router']
```

### 4. Lifespan Initialization (`hivenode/main.py`)

Initialize RepoIndexer during app startup and set in dependencies:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize services on startup."""
    # ... existing ledger/storage/node setup ...

    # Initialize repo indexer
    from hivenode.repo.indexer import RepoIndexer
    from pathlib import Path

    repo_index_db = Path(settings.ledger_db_path).parent / "repo-index.db"
    repo_root = _find_repo_root()
    repo_indexer = RepoIndexer(repo_root=repo_root, db_path=repo_index_db)

    dependencies.set_repo_indexer(repo_indexer)

    yield

    # Cleanup
    # ... existing cleanup ...
    repo_indexer.close()  # Add close() method to RepoIndexer if needed


def _find_repo_root() -> Path:
    """Find git repository root by walking up from hivenode directory."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise ValueError("Could not find git repository root (.git/ directory)")
```

**Note:** Add `close()` method to `RepoIndexer` class if it needs cleanup (e.g., closing DB connections). If using `sqlite3` directly, this may be a no-op.

### 5. Add Dependency (`pyproject.toml`)

Add `pathspec` to `[project.dependencies]`:

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "sqlalchemy>=2.0",
    "pydantic>=2.0",
    "pyjwt[crypto]>=2.8",
    "passlib[bcrypt]>=1.7",
    "cryptography>=42.0",
    "pydantic-settings>=2.0",
    "twilio>=9.0",
    "aiosqlite>=0.20",
    "pyyaml>=6.0",
    "click>=8.0",
    "psutil>=5.0",
    "pathspec>=0.12",  # NEW
]
```

### 6. Update Setuptools Packages (`pyproject.toml`)

Add `hivenode.repo` to the packages list:

```toml
[tool.setuptools]
packages = [
    "ra96it",
    "ra96it.services",
    "ra96it.routes",
    "hivenode",
    "hivenode.routes",
    "hivenode.ledger",
    "hivenode.storage",
    "hivenode.storage.adapters",
    "hivenode.adapters",
    "hivenode.privacy",
    "hivenode.llm",
    "hivenode.governance",
    "hivenode.governance.gate_enforcer",
    "hivenode.shell",
    "hivenode.repo",  # NEW
    "engine"
]
```

### 7. Route Tests (continued in `test_repo_routes.py`)

Add tests for the three new routes:

#### GET /repo/tree Tests
- `test_tree_structure` — Root tree has nested children
- `test_tree_path_filter` — `?path=src/` returns subtree under src/
- `test_tree_extension_filter` — `?ext=.py` only includes .py files in tree
- `test_tree_respects_visibility` — Hidden files excluded from tree by default
- `test_tree_show_all` — `?show_all=true` includes hidden files in tree

#### PATCH /repo/visibility Tests
- `test_set_visibility_single_file` — Toggle single file, affected=1
- `test_set_visibility_directory_recursive` — Toggle directory, all descendants updated
- `test_set_visibility_returns_affected_count` — Response has correct count
- `test_set_visibility_makes_file_hidden` — File no longer appears in default index query
- `test_set_visibility_makes_file_visible_again` — Re-toggle shows file again

#### GET /repo/stats Tests
- `test_stats_counts_correct` — Total files, dirs, visible, gitignored, hidden are accurate
- `test_stats_extensions` — Extension breakdown matches actual files
- `test_stats_total_size` — Total size computed correctly
- `test_stats_last_scan_time` — Timestamp from scan_meta

Minimum: 13 additional tests (total ~37 across both route test files).

### 8. Integration Smoke Test

Add one final E2E-style test that verifies the full flow:

```python
def test_full_workflow(client, test_repo):
    """Smoke test: scan → query → read → hide → query again → stats."""
    # 1. Scan repo
    scan_resp = client.post("/repo/scan")
    assert scan_resp.status_code == 200
    assert scan_resp.json()["ok"] is True

    # 2. Query default view
    index_resp = client.get("/repo/index")
    assert index_resp.status_code == 200
    files_before = index_resp.json()["files"]

    # 3. Read a file
    read_resp = client.get("/repo/read?path=README.md")
    assert read_resp.status_code == 200
    assert "Test Repo" in read_resp.json()["content"]

    # 4. Hide a file
    visibility_resp = client.patch("/repo/visibility", json={
        "path": "README.md",
        "visible": False
    })
    assert visibility_resp.status_code == 200
    assert visibility_resp.json()["affected"] == 1

    # 5. Query again (README.md should be gone)
    index_resp2 = client.get("/repo/index")
    paths_after = [f["path"] for f in index_resp2.json()["files"]]
    assert "README.md" not in paths_after

    # 6. Get stats
    stats_resp = client.get("/repo/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total_files"] > 0
    assert stats["hidden_files"] >= 1
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-REPO-INDEX-001.md` — full spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — lifespan pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — router registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` — dependencies and packages
- Output from TASK-032 (indexer.py, schemas.py)
- Output from TASK-033 (routes.py initial version)

## Files to Create

- (None — all additions to existing files)

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\routes.py` — add tree, visibility, stats routes
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\schemas.py` — add SetVisibilityRequest, SetVisibilityResponse
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\__init__.py` — export router
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — include repo router
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — initialize RepoIndexer in lifespan
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` — add pathspec dependency and hivenode.repo package
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_repo_routes.py` — add tests for new routes

## Constraints

- **NO STUBS.** Every route fully implemented.
- **TDD.** Write tests first, then routes.
- **No file over 500 lines.** If routes.py exceeds 500, consider splitting.
- Follow existing patterns from main.py and routes/__init__.py
- Use Pydantic models for request/response validation
- Auth via `verify_jwt_or_local` dependency
- Ensure `_find_repo_root()` is robust (handles missing .git gracefully)

## Success Criteria

- All tests pass: `pytest tests/hivenode/repo/ -v`
- Routes accessible via hivenode: `http://localhost:8420/repo/*`
- Full workflow test passes (scan → query → read → hide → stats)
- `pathspec` installed: `pip install -e .` succeeds
- RepoIndexer initializes on hivenode startup without errors
- Code follows hivenode conventions

---

**Model:** sonnet
**Estimate:** S (2-3 hours)

*Ready for dispatch after TASK-032 completes. Can run parallel with TASK-033 once indexer is built.*
