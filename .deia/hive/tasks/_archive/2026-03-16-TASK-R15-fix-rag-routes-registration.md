# TASK-R15: Fix RAG routes returning 404

## Objective
Debug and fix why all RAG API endpoints (`/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, `/api/rag/stats`) return 404.

## Context
R13 verification found 13 test failures in `tests/hivenode/test_rag_routes.py`. All requests return 404. The R07 task was supposed to register `rag_routes.py` in `__init__.py` but something went wrong — either import collision, wrong prefix, or missing registration.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (check registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py` (check router name + prefixes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rag_routes.py` (check expected paths)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R13-RESPONSE.md`

## Deliverables
- [ ] Identify why routes return 404 (read __init__.py and rag_routes.py first)
- [ ] Fix the registration — ensure routes are mounted at correct prefix
- [ ] Handle any import name collision with existing `rag` module
- [ ] Run: `python -m pytest tests/hivenode/test_rag_routes.py -v`
- [ ] All 13+ RAG route tests must pass

## Constraints
- Do NOT modify test files — they define the contract
- Do NOT modify rag_routes.py unless absolutely necessary (prefer fixing registration)

## Acceptance Criteria
- [ ] All RAG route tests pass (13+ tests)
- [ ] Routes accessible at correct API paths
- [ ] No import errors on hivenode startup
- [ ] No regressions in other route tests

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R15-RESPONSE.md`
All 8 sections required.
