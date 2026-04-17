# SPEC: Rebuild route registration in hivenode/routes/__init__.py

## Priority
P0.05

## Model Assignment
haiku

## Objective
Re-add route imports and registrations that were lost in a git reset. Four routes need to be registered in `hivenode/routes/__init__.py`:

1. **DES routes** — `hivenode/routes/des_routes.py` exists (untracked, survived). Import and register its router.
2. **RAG routes** — `hivenode/routes/rag_routes.py` exists (untracked, survived). Import and register its router.
3. **Canvas chat routes** — `hivenode/routes/canvas_chat.py` exists (untracked, survived). Import and register its router.
4. **Phase NL routes** — `hivenode/routes/phase_nl_routes.py` exists (untracked, survived). Import and register its router if it has a router.

## Recovery Sources
Read these response files for exact import patterns:
- `.deia/hive/responses/20260315-TASK-146-RESPONSE.md` (DES routes registration)
- `.deia/hive/responses/20260315-TASK-157-RESPONSE.md` (RAG routes registration)
- `.deia/hive/responses/20260315-TASK-165-RESPONSE.md` (canvas chat registration)
- `.deia/hive/responses/20260315-TASK-166-RESPONSE.md` (phase NL registration)

Also read the current `hivenode/routes/__init__.py` to understand the existing pattern for how routers are imported and included.

**CRITICAL: Read the surviving test files — they contain the exact imports and endpoint paths:**
- `tests/hivenode/test_des_routes.py` — shows DES router prefix, endpoint paths, schema imports
- `tests/hivenode/test_rag_routes.py` — shows RAG router prefix, endpoint paths
- `tests/hivenode/test_canvas_chat.py` — shows canvas chat router prefix, endpoint paths
- `tests/hivenode/test_phase_nl_routes.py` — shows phase NL router prefix, endpoint paths

**Also read the route source files themselves (they survived):**
- `hivenode/routes/des_routes.py` — has the router object name and prefix
- `hivenode/routes/rag_routes.py` — has the router object name and prefix
- `hivenode/routes/canvas_chat.py` — has the router object name and prefix
- `hivenode/routes/phase_nl_routes.py` — has the router object name and prefix

## Acceptance Criteria
- [ ] All 4 route modules imported in __init__.py
- [ ] All 4 routers registered with app.include_router()
- [ ] Existing routes NOT disrupted
- [ ] `python -m pytest tests/hivenode/test_des_routes.py tests/hivenode/test_rag_routes.py tests/hivenode/test_canvas_chat.py -v` all pass
- [ ] No import errors when starting hivenode

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-01-route-registration", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-01-route-registration", "files": ["hivenode/routes/__init__.py"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
