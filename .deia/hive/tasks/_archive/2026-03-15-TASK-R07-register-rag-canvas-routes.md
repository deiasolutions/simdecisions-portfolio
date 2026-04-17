# TASK-R07: Register RAG routes + canvas chat routes in __init__.py

**Priority:** P0.35
**Original:** TASK-157 (RAG routes) + TASK-165 (canvas chatbot dialect)
**Rebuild Batch:** 02
**Date:** 2026-03-15

---

## Objective

Restore route registrations for two surviving route modules (`hivenode/routes/rag_routes.py` and `hivenode/routes/canvas_chat.py`) that were lost in the git reset.

---

## Context

After `git reset --hard HEAD`, two route modules survived (they were already tracked in git):
- `hivenode/routes/rag_routes.py` — 4 endpoints: /api/rag/index, /api/rag/query, /api/rag/chunks, /api/rag/stats
- `hivenode/routes/canvas_chat.py` — POST /api/canvas/chat endpoint

However, their registrations in `hivenode/routes/__init__.py` were lost. The routes exist but are not mounted to the FastAPI router.

**Dependencies:**
- This task depends on TASK-R01 from Batch 01 completing first (DES routes must be registered before this)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current state — missing registrations)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py` (surviving file — check router export name)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\canvas_chat.py` (surviving file — check router export name)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-157-RESPONSE.md` (RAG routes completion report)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-165-COMPLETION-REPORT.md` (canvas chat completion report)

---

## Deliverables

### 1. Add RAG Routes Registration

- [ ] In `hivenode/routes/__init__.py`, add import for `hivenode.routes.rag_routes`
- [ ] **IMPORTANT:** Rename the import to `new_rag_routes` to avoid collision with existing `rag_routes` import (from `hivenode.rag`)
- [ ] Add route registration: `router.include_router(new_rag_routes.router, prefix='/api/rag', tags=['rag-indexer'])`
- [ ] Verify router object name is `router` in `rag_routes.py` (check file before assuming)

### 2. Add Canvas Chat Routes Registration

- [ ] In `hivenode/routes/__init__.py`, add import for `hivenode.routes.canvas_chat`
- [ ] Add route registration: `router.include_router(canvas_chat.router, tags=['canvas-chat'])`
- [ ] Verify router object name is `router` in `canvas_chat.py` (check file before assuming)
- [ ] **NOTE:** Canvas chat routes already have `/api/canvas` prefix in their route file — do NOT add prefix again in registration

### 3. Verify Import Order

- [ ] Place new imports AFTER existing route imports but BEFORE `create_router()` function
- [ ] Maintain alphabetical or logical grouping (group by module origin)

---

## Test Requirements

### Tests Written FIRST (TDD)
- [ ] No new tests needed — tests already exist
- [ ] Verify existing tests still pass after registration

### All Tests Pass
- [ ] Run: `python -m pytest tests/hivenode/test_rag_routes.py -v`
- [ ] Expected: **16 tests PASSING** (from TASK-157)
- [ ] Run: `python -m pytest tests/hivenode/test_canvas_chat.py -v` (if file exists)
- [ ] Expected: **8 tests PASSING** (from TASK-165)

### Smoke Test (Route Registration Verification)
- [ ] Start hivenode server: `cd hivenode && uvicorn main:app --reload` (background)
- [ ] Check OpenAPI docs at `http://localhost:8000/docs`
- [ ] Verify `/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, `/api/rag/stats` appear in docs
- [ ] Verify `/api/canvas/chat` appears in docs
- [ ] Stop server after verification

---

## Constraints

- No file over 500 lines (`__init__.py` is currently 44 lines — well within limits)
- No stubs (just adding two lines of registration code)
- Do NOT modify `rag_routes.py` or `canvas_chat.py` — they already exist and work
- Handle import name collision (`rag_routes` already imported from `hivenode.rag`)

---

## Acceptance Criteria

- [x] Import added: `from hivenode.routes import rag_routes as new_rag_routes`
- [x] Import added: `from hivenode.routes import canvas_chat`
- [x] Registration added: `router.include_router(new_rag_routes.router, prefix='/api/rag', tags=['rag-indexer'])`
- [x] Registration added: `router.include_router(canvas_chat.router, tags=['canvas-chat'])`
- [x] All 16 RAG route tests pass
- [x] All 8 canvas chat tests pass (if test file exists)
- [x] No import errors when hivenode starts
- [x] Routes visible in OpenAPI docs

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R07-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Haiku (simple registration task)
**Estimated Duration:** 5-10 minutes
**Depends On:** TASK-R01 (Batch 01)
