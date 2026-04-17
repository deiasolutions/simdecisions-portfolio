# BRIEFING: Repo File Index Service

**Date:** 2026-03-12
**From:** Q33NR
**To:** Q33N
**Spec:** `docs/specs/SPEC-REPO-INDEX-001.md`

## Objective

Create task files to implement the Repo File Index Service described in SPEC-REPO-INDEX-001. This adds `/repo/*` routes to the existing hivenode that let the browser query a SQLite index of every file in the repository and fetch file contents on demand.

## What to Build

A new `hivenode/repo/` module with:

1. **SQLite file index** (`~/.shiftcenter/repo-index.db`) — indexes every file in the repo with path, size, modified time, SHA-256 hash, extension, gitignore status, and user-controlled visibility flag
2. **Gitignore parser** — uses `pathspec` library to parse `.gitignore` rules and mark files accordingly
3. **6 FastAPI routes** mounted at `/repo` prefix on existing hivenode:
   - `POST /repo/scan` — full re-scan of repo tree
   - `GET /repo/index` — query index with filters (path prefix, extension, visibility, gitignore, search, pagination)
   - `GET /repo/tree` — directory tree structure as nested JSON
   - `GET /repo/read?path=...` — read file contents from disk (text as UTF-8, binary as base64)
   - `PATCH /repo/visibility` — toggle visible/hidden on files or folders (recursive for dirs)
   - `GET /repo/stats` — summary statistics
4. **Pydantic schemas** for all request/response models
5. **Tests** — TDD, unit tests for indexer + gitignore + routes

## Key Design Decisions (already approved by Q88N)

- Routes go on existing hivenode (port 8420), NOT a separate service
- On-demand scan only (no watchdog/timer)
- Whole repo indexed, with `.gitignore` awareness for filtering
- Auth: `verify_jwt_or_local` (local bypasses JWT)
- Hard-skip: `.git/`, `node_modules/`, `__pycache__/`, `.venv/`, `venv/`
- Read-only — no write/delete through `/repo/*` routes
- DB location: `~/.shiftcenter/repo-index.db` (follows ledger.db pattern)
- New dependency: `pathspec>=0.12` added to pyproject.toml

## Files to Read First

- `docs/specs/SPEC-REPO-INDEX-001.md` — the full spec (READ THIS ENTIRELY)
- `hivenode/routes/__init__.py` — route registration pattern
- `hivenode/routes/storage_routes.py` — existing route pattern to follow
- `hivenode/storage/adapters/base.py` — adapter pattern reference
- `hivenode/dependencies.py` — auth dependency (`verify_jwt_or_local`)
- `hivenode/main.py` — lifespan startup pattern for initializing RepoIndexer
- `hivenode/config.py` — settings pattern (DB paths)
- `pyproject.toml` — where to add `pathspec` dependency

## Task Breakdown Guidance

The spec defines 4 phases. Suggested task split:

- **TASK-032:** Schema + RepoIndexer core (scan, DB operations, gitignore parsing) + unit tests
- **TASK-033:** Routes (scan, index, read) + route tests
- **TASK-034:** Routes (tree, visibility, stats) + route tests + wire into main.py + add pathspec to pyproject.toml

Phase 1 (TASK-032) must complete before Phases 2-3. TASK-033 and TASK-034 can run in parallel once TASK-032 is done.

Adjust the split if you see a better breakdown after reading the spec and codebase. The key constraint is bee-sized tasks (each completable by a single bee).

## Constraints

- No file over 500 lines — modularize if needed
- TDD — tests first
- No stubs
- CSS rule N/A (backend only)
- All file paths absolute in task docs
- Follow existing hivenode patterns (Pydantic models, dependency injection, error handling)

## Model Assignment

- TASK-032: **sonnet** (core logic, gitignore parsing, schema design)
- TASK-033: **sonnet** (route patterns, query filtering)
- TASK-034: **sonnet** (tree building, wiring)

## Deliverable

Write task files to `.deia/hive/tasks/`. Return to Q33NR for review before dispatching bees.

## Directory to Create

Ensure `.deia/to_localhost/` exists in the repo with a `.gitkeep` file so it's committed.
