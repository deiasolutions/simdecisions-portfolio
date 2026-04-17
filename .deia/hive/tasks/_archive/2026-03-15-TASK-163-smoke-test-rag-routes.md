# TASK-163: Smoke Test RAG Routes

## Objective
Verify RAG HTTP routes are registered and respond correctly.

## Context
The RAG indexer has HTTP routes at `/api/rag/*`. These routes were ported from platform/efemera.

After TASK-161 (import fixes) and TASK-162 (indexer verification), we need to verify the routes work.

**Routes file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py`

**Expected endpoints:**
- `POST /api/rag/index` — index a file or directory
- `GET /api/rag/query` — query by similarity
- `GET /api/rag/status` — indexer status

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (route registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (example of E2E route testing)

## Deliverables
- [ ] Verify RAG routes are registered in `hivenode/routes/__init__.py`
- [ ] Write smoke test: `tests/hivenode/rag/test_routes.py`
- [ ] Test each endpoint with TestClient
- [ ] All smoke tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Run `cd hivenode && python -m pytest tests/hivenode/rag/test_routes.py -v`
- [ ] All tests pass
- [ ] Edge cases:
  - Invalid file path → 400 or 404
  - Empty query → 400
  - Valid request → 200

## Constraints
- No file over 500 lines
- No stubs
- Use FastAPI TestClient (see `tests/hivenode/test_e2e.py` for pattern)
- Use temporary directories for file indexing (pytest tmpdir fixture)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-163-RESPONSE.md`

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
