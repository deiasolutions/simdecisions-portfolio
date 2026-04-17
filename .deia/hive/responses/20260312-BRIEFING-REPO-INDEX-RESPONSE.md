# BRIEFING-REPO-INDEX: Repo File Index Task Breakdown -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\to_localhost\.gitkeep` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-032.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-033.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-034.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-BRIEFING-REPO-INDEX-RESPONSE.md` (created)

## What Was Done

- Created `.deia/to_localhost/` directory with `.gitkeep` file for commit
- Created TASK-032: Repo Index Core (schema, indexer, gitignore parser, unit tests) — S estimate, sonnet model
- Created TASK-033: Repo Index Routes Part 1 (scan, query, read endpoints + route tests) — S estimate, sonnet model
- Created TASK-034: Repo Index Routes Part 2 (tree, visibility, stats endpoints + main.py wiring + pathspec dependency) — S estimate, sonnet model
- All three tasks follow TDD, no-stubs, 500-line-limit, absolute-paths rules
- Task dependencies structured: TASK-032 blocks both TASK-033 and TASK-034; TASK-033 and TASK-034 can run parallel after TASK-032
- Each task includes comprehensive acceptance criteria, test requirements, file lists, and success criteria
- All tasks reference SPEC-REPO-INDEX-001 and follow existing hivenode patterns

## Task Summary

### TASK-032 (Core — Phase 1)
**Estimate:** S | **Model:** sonnet | **Depends:** none | **Blocks:** TASK-033, TASK-034

Creates the foundation:
- SQLite schema (files table + scan_meta table)
- `RepoIndexer` class with scan, query, tree, read_file, set_visibility, stats methods
- `GitignoreParser` using pathspec library
- Full Pydantic schemas (FileEntry, ScanResult, IndexQuery, IndexResult, TreeNode, FileContent, RepoStats)
- Comprehensive unit tests (28+ tests in test_indexer.py + test_gitignore.py)
- Security: path traversal blocking, .git/ exclusion, hardcoded exclusions
- Repo root auto-detection logic

### TASK-033 (Routes Part 1 — Phase 2)
**Estimate:** S | **Model:** sonnet | **Depends:** TASK-032 | **Blocks:** none

Adds three FastAPI routes:
- POST /repo/scan (trigger full re-scan)
- GET /repo/index (query with filters: path, ext, gitignored, show_all, hidden_only, search, pagination)
- GET /repo/read (read file contents, text as UTF-8, binary as base64)
- Dependency injection: `get_repo_indexer()` in dependencies.py
- Route tests (24+ tests in test_repo_routes.py)
- Error handling: 400/403/404/500 with JSON responses
- Auth via verify_jwt_or_local

### TASK-034 (Routes Part 2 + Wiring — Phase 3)
**Estimate:** S | **Model:** sonnet | **Depends:** TASK-032 | **Blocks:** none

Completes the service:
- GET /repo/tree (nested directory tree structure)
- PATCH /repo/visibility (toggle visible flag, recursive for dirs)
- GET /repo/stats (summary statistics, extension breakdown)
- Wire RepoIndexer into main.py lifespan startup
- Register repo router in routes/__init__.py
- Add pathspec>=0.12 to pyproject.toml dependencies
- Add hivenode.repo to setuptools packages
- Route tests for new endpoints (13+ additional tests)
- Full workflow E2E smoke test

## Test Coverage Estimates

- TASK-032: 28+ tests (gitignore, scan, query, tree, read, visibility, stats, security)
- TASK-033: 24+ tests (scan route, index route, read route, auth)
- TASK-034: 13+ tests (tree route, visibility route, stats route, E2E)
- **Total: 65+ tests minimum**

## Dependencies

- Existing: FastAPI, Pydantic, SQLite (stdlib), hashlib (stdlib), os.walk (stdlib)
- New: pathspec>=0.12 (added in TASK-034)

## Files Created (by tasks)

TASK-032 creates:
- hivenode/repo/__init__.py
- hivenode/repo/schemas.py
- hivenode/repo/gitignore.py
- hivenode/repo/indexer.py
- tests/hivenode/repo/__init__.py
- tests/hivenode/repo/test_gitignore.py
- tests/hivenode/repo/test_indexer.py

TASK-033 creates:
- hivenode/repo/routes.py
- tests/hivenode/repo/test_repo_routes.py

TASK-033 modifies:
- hivenode/dependencies.py (add get_repo_indexer, set_repo_indexer)

TASK-034 modifies:
- hivenode/repo/routes.py (add 3 more routes)
- hivenode/repo/schemas.py (add SetVisibilityRequest, SetVisibilityResponse)
- hivenode/repo/__init__.py (export router)
- hivenode/routes/__init__.py (include repo router)
- hivenode/main.py (initialize RepoIndexer in lifespan)
- pyproject.toml (add pathspec dependency, add hivenode.repo package)
- tests/hivenode/repo/test_repo_routes.py (add tests for new routes)

## Dispatch Strategy

1. **Immediate:** Dispatch TASK-032 (sonnet) — foundation must complete first
2. **After TASK-032:** Dispatch TASK-033 and TASK-034 in parallel (both sonnet) — they're independent once indexer exists

## Validation Checklist

- [x] All tasks are bee-sized (S estimates, 2-3 hours each)
- [x] TDD enforced (tests first, then implementation)
- [x] No stubs allowed (every method fully implemented)
- [x] 500-line limit documented
- [x] All file paths absolute in task docs
- [x] Model assignments specified (all sonnet)
- [x] Dependencies clear (TASK-032 blocks others)
- [x] Acceptance criteria unambiguous
- [x] Test counts estimated
- [x] Security requirements explicit (path traversal, .git/ blocking)
- [x] Error handling specified (HTTP status codes mapped)
- [x] Auth pattern documented (verify_jwt_or_local)
- [x] Database location follows existing pattern (~/.shiftcenter/)
- [x] Integration with existing hivenode clear (routes, dependencies, lifespan)

## Ready for Dispatch

All three task files are complete and ready for dispatch. TASK-032 should be dispatched immediately. TASK-033 and TASK-034 should wait for TASK-032 completion, then can dispatch in parallel.

---

**End of Response**
