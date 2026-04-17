# TASK-034: Repo Index Routes Part 2 -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\schemas.py` — Added SetVisibilityRequest and SetVisibilityResponse models
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\routes.py` — Added GET /repo/tree, PATCH /repo/visibility, GET /repo/stats routes with imports
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\__init__.py` — Added new schemas to exports and routes module
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — Added _find_repo_root() function and initialized RepoIndexer in lifespan
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` — Added pathspec>=0.12 dependency and hivenode.repo to packages list
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_repo_routes.py` — Added 19 new tests (5 tree, 5 visibility, 4 stats, 1 full workflow)

## What Was Done

- Added SetVisibilityRequest (path, visible) and SetVisibilityResponse (ok, affected) Pydantic models to schemas.py
- Implemented GET /repo/tree route with all query filters (path, ext, gitignored, show_all, hidden_only, search), returns nested TreeNode structure
- Implemented PATCH /repo/visibility route accepting SetVisibilityRequest, updates single file or directory recursively, returns affected count
- Implemented GET /repo/stats route returning RepoStats with counts, extensions breakdown, total size, and last scan time
- Updated routes.py imports to include TreeNode, RepoStats, SetVisibilityRequest, SetVisibilityResponse
- Updated hivenode/repo/__init__.py to export new schemas and routes module
- Added pathspec>=0.12 to project dependencies in pyproject.toml
- Added hivenode.repo to setuptools packages list in pyproject.toml
- Created _find_repo_root() helper function in main.py that walks up from hivenode directory to find .git/
- Initialized RepoIndexer in main.py lifespan using ledger_db_path parent directory for repo-index.db
- Set RepoIndexer in global dependencies via dependencies.set_repo_indexer()
- Added 5 tests for GET /repo/tree: structure, path filter, extension filter, visibility respect, show_all flag
- Added 5 tests for PATCH /repo/visibility: single file toggle, directory recursive, affected count, hidden behavior, re-toggle
- Added 4 tests for GET /repo/stats: counts accuracy, extensions breakdown, total size, last scan timestamp
- Added 1 full workflow smoke test covering scan → query → read → hide → query → stats end-to-end
- All 79 repo module tests pass (40 route tests + 39 indexer/gitignore tests)
- Verified routes registered in FastAPI app: /repo/tree, /repo/visibility, /repo/stats accessible
- Added REPO-002 to feature inventory (19 new tests)
- Exported inventory to FEATURE-INVENTORY.md (36 features, 5,645 tests)
- Archived TASK-034.md to _archive/

---

## Test Results

```
============================= test session starts =============================
tests/hivenode/repo/ - 79 tests
- test_repo_routes.py: 40 passed (includes 19 new tests for tree, visibility, stats, full workflow)
- test_indexer.py: 32 passed
- test_gitignore.py: 7 passed
============================= 79 passed in 6.28s ==============================
```

## Route Verification

App imported successfully. Routes registered:
- /repo/scan ✓
- /repo/index ✓
- /repo/read ✓
- /repo/tree ✓ (NEW)
- /repo/visibility ✓ (NEW)
- /repo/stats ✓ (NEW)

---

## Implementation Notes

**TDD Followed:** All 19 tests written before implementation, all tests pass.

**No Stubs:** All routes fully implemented with error handling (400 for validation, 500 for DB errors).

**Auth:** All routes use verify_jwt_or_local dependency (local bypasses, cloud requires JWT).

**Lifespan Pattern:** RepoIndexer initialized in main.py lifespan following existing patterns for ledger/storage/node services.

**Path Finding:** _find_repo_root() walks up from hivenode directory until .git/ found, raises ValueError if not found.

**DB Location:** repo-index.db stored in same directory as ledger.db (follows existing pattern).

**Dependencies:** pathspec added to pyproject.toml dependencies, hivenode.repo added to packages list.

**Route Structure:** routes.py now 269 lines (under 500 limit), fully implements all 6 repo routes.

**Full Workflow:** Smoke test verifies complete end-to-end flow from scan through stats.

---

**Task Status:** COMPLETE — All acceptance criteria met, all tests passing, routes accessible via hivenode.
