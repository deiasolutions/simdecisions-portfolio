# TASK-033: Repo Index Routes (Part 1) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`

## Files Created

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_repo_routes.py`

## What Was Done

- Added `set_repo_indexer()` and `get_repo_indexer()` to hivenode/dependencies.py for dependency injection
- Created hivenode/repo/routes.py with three FastAPI endpoints:
  - POST /repo/scan - trigger full repository re-scan
  - GET /repo/index - query file index with comprehensive filters (path, ext, gitignored, show_all, hidden_only, search, limit, offset)
  - GET /repo/read - read file contents from disk with security checks
- Mounted repo router to main app in hivenode/routes/__init__.py with /repo prefix
- Created comprehensive test suite (tests/hivenode/repo/test_repo_routes.py) with 25 passing tests:
  - 3 scan endpoint tests (success, schema validation, local auth bypass)
  - 10 index endpoint tests (default view, path filter, extension filter, gitignored modes, show_all, hidden_only, search, pagination, limit validation)
  - 9 read endpoint tests (text files, binary files, encoding modes, not found, path traversal, absolute paths, .git/ forbidden, missing param)
  - 3 auth tests for cloud mode (scan, index, read)
- All routes use verify_jwt_or_local for auth (local mode bypasses JWT, cloud requires it)
- All routes properly map exceptions to HTTP status codes (400, 403, 404, 500)
- Query parameter validation via FastAPI/Pydantic (limit constrained to 1-1000)
- Security: path traversal blocked, absolute paths blocked, .git/ access forbidden
- Auto-detection for file encoding (text vs base64) based on extension

## Test Results

- **New tests:** 25/25 passing in tests/hivenode/repo/test_repo_routes.py
- **Full repo module:** 64/64 passing (39 from TASK-032 + 25 from TASK-033)
- **Hivenode suite:** 654 passing (17 pre-existing LLM router failures unrelated to this task)
- All routes successfully registered and accessible via FastAPI app

## Notes

- Followed TDD: wrote tests first, then implementation
- Used storage_routes.py as pattern reference for route structure
- Error handling covers all specified cases (ValueError→400, PermissionError→403, FileNotFoundError→404, Exception→500)
- Routes are read-only (except scan operation) per security requirements
- No file over 500 lines constraint met (routes.py: 155 lines, test file: 489 lines)
- All acceptance criteria from TASK-033 met

## Next Steps

TASK-034 will initialize the RepoIndexer in main.py lifespan and wire up the dependency injection. This task is ready for archival.
