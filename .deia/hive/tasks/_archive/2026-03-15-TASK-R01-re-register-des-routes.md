# TASK-R01: Re-register DES routes in __init__.py

**Priority:** P0.05
**Model:** Haiku
**Original:** TASK-146 (DES engine routes port)

---

## Objective

Re-register the DES routes module (`hivenode/routes/des_routes.py`) in the main routes `__init__.py` file. The DES routes module was created and survived the git reset, but its registration in `__init__.py` was lost.

---

## Context

A `git reset --hard HEAD` wiped all uncommitted tracked-file modifications. The DES routes module file (`des_routes.py`) survived because it was a new untracked file. However, the edits to the existing `__init__.py` file to register these routes were lost and must be reconstructed.

The DES routes module provides 4 endpoints under `/api/des/`:
- POST `/api/des/run` — run a DES flow to completion
- POST `/api/des/validate` — validate a flow before running
- POST `/api/des/replicate` — run multiple replications
- GET `/api/des/status` — engine health check

These routes were already built and tested (22 passing tests) but are not currently accessible because they are not registered in the FastAPI router.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current state — missing DES registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (surviving module with router definition)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-146-RESPONSE.md` (original work record for context)

---

## Deliverables

- [ ] Import `des_routes` in `hivenode/routes/__init__.py` (add to existing import line at top)
- [ ] Register the DES router in `create_router()` function with prefix `/api/des` and tag `des`
- [ ] Run `python -m pytest tests/hivenode/test_des_routes.py -v` to verify all 22 tests pass
- [ ] No other routes or functionality should be affected

---

## Test Requirements

- [ ] All 22 existing tests in `tests/hivenode/test_des_routes.py` must pass
- [ ] No regressions in other route tests (run `python -m pytest tests/hivenode/ -v` to verify)
- [ ] Manual verification: the router includes the des_routes.router with correct prefix and tags

---

## Constraints

- No file over 500 lines (routes/__init__.py is currently 44 lines, will grow minimally)
- No stubs
- Follow the exact pattern used for other route registrations in the same file (see `sim.router`, `inventory_routes.router`, etc.)

---

## Implementation Guidance

1. **Import statement:** Add `des_routes` to the existing import line at line 3:
   ```python
   from hivenode.routes import health, auth, ledger_routes, storage_routes, node, llm_routes, shell, sync_routes, kanban_routes, progress_routes, build_monitor, sim, inventory_routes, des_routes
   ```

2. **Router registration:** Add this line inside `create_router()` function (after line 37, before entity_routes):
   ```python
   router.include_router(des_routes.router, prefix='/api/des', tags=['des'])
   ```

3. **Verification:** Run the test suite to confirm all 22 DES route tests pass.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R01-RESPONSE.md`

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
