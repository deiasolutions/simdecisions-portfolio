# TASK-R01: Re-register DES Routes

## Objective

Re-register the `hivenode/routes/des_routes.py` module in `hivenode/routes/__init__.py` to mount the 4 DES engine endpoints that were lost during the git reset.

---

## Context

**Background:**
- A git reset occurred on 2026-03-15 that removed the route registration for DES routes
- The module itself (`hivenode/routes/des_routes.py`) survived intact (276 lines, 4 endpoints)
- All 22 tests survived (`tests/hivenode/test_des_routes.py`, 471 lines)
- Only the registration in `hivenode/routes/__init__.py` was lost
- All 22 tests are currently failing because the routes are not mounted

**DES Routes Module Details:**
- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- Router: `router = APIRouter(prefix="/api/des", tags=["des-engine"])`
- 4 Endpoints:
  - `POST /api/des/run` — run a DES flow to completion
  - `POST /api/des/validate` — validate a flow before running
  - `POST /api/des/replicate` — run multiple replications with stats
  - `GET /api/des/status` — engine health check
- 9 Pydantic schemas: `NodeSchema`, `EdgeSchema`, `ResourceSchema`, `VariableSchema`, `FlowSchema`, `SimConfigSchema`, `RunRequest`, `RunResponse`, `ValidateResponse`, `ReplicateRequest`, `ReplicateResponse`, `StatusResponse`

**Current State of __init__.py:**
- Line 3: Import statement does NOT include `des_routes`
- Lines 15-43: `create_router()` function does NOT register `des_routes.router`
- Other routes (ledger, shell, rag, efemera, phase_ir, etc.) are correctly registered

**What You Need to Do:**
1. Import `des_routes` module at line 3 (add to existing import statement)
2. Register the router in the `create_router()` function
3. Verify all 22 DES route tests pass

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — current state, see what's missing
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` — to see router definition (prefix, tags)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py` — to understand what will be tested

---

## Deliverables

- [ ] Import `des_routes` in `hivenode/routes/__init__.py` (line 3 area)
- [ ] Register `des_routes.router` in the `create_router()` function with appropriate prefix and tags
- [ ] All 22 tests in `tests/hivenode/test_des_routes.py` pass (verify with pytest)
- [ ] No regressions in other route tests (run full backend test suite)
- [ ] Response file: `.deia/hive/responses/20260316-TASK-R01-RESPONSE.md` (8 sections)

---

## Test Requirements

- [ ] Run `cd hivenode && python -m pytest tests/hivenode/test_des_routes.py -v` — all 22 tests must pass
- [ ] Run full backend test suite to verify no regressions in other routes
- [ ] Edge cases already covered by existing tests:
  - Empty flows (should fail validation)
  - Bad edge references (should fail validation)
  - Flows with no source nodes (should fail validation)
  - Valid flows with resources and variables (should run successfully)
  - Replication endpoint with custom configs

---

## Constraints

- **No file over 500 lines** — `__init__.py` is currently 44 lines, will grow to ~46 lines
- **TDD** — Tests already exist (22 tests), you must verify they all pass
- **No stubs** — N/A (just registration, no new code)
- **No hardcoded colors** — N/A (backend route registration)
- **Absolute paths** — All paths in this task file are absolute
- **No new code** — Just import + registration. Do NOT modify `des_routes.py` itself.

---

## Registration Pattern

Look at how other routes are registered in `create_router()` and follow the same pattern. For example:

```python
# Import at top (line 3 area)
from hivenode.routes import health, auth, ledger_routes, ..., des_routes

# In create_router() function
router.include_router(des_routes.router, tags=['des'])
# OR
router.include_router(des_routes.router, prefix='/api/des', tags=['des-engine'])
```

**Note:** The `des_routes.router` already has `prefix="/api/des"` and `tags=["des-engine"]` defined in the router creation, so you can either:
- Use `router.include_router(des_routes.router)` (relies on router's own prefix/tags)
- Use `router.include_router(des_routes.router, tags=['des'])` (override tags)
- Use `router.include_router(des_routes.router, prefix='/api/des', tags=['des-engine'])` (explicit, but redundant)

**Recommendation:** Follow the pattern used by other routes in the file. Most routes use explicit tags in `include_router()`.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-R01-RESPONSE.md`

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

---

## Acceptance Criteria

- [ ] `des_routes` imported in `hivenode/routes/__init__.py` (line 3 area)
- [ ] Router registered in `create_router()` function with appropriate prefix and tags
- [ ] All 22 tests in `tests/hivenode/test_des_routes.py` pass
- [ ] No regressions in other route tests (run full backend test suite to verify)
- [ ] Response file written with all 8 sections

---

## Reference

- Original spec: `.deia/hive/queue/2026-03-15-2300-SPEC-rebuild-R01-des-routes.md`
- Briefing: `.deia/hive/coordination/2026-03-16-BRIEFING-des-routes-registration.md`
- Original implementation: TASK-146 (2026-03-15, completed with 22/22 tests passing)
