# BRIEFING: Re-register DES Routes

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0.05
**Model:** haiku

---

## Objective

Re-register the DES routes module in `hivenode/routes/__init__.py`. The module (`des_routes.py`) survived the git reset but its registration was lost.

---

## Context

**What happened:**
- A git reset occurred on 2026-03-15 that lost some route registrations
- The `hivenode/routes/des_routes.py` file still exists (276 lines, 4 endpoints, 9 schemas)
- The tests still exist (`tests/hivenode/test_des_routes.py`, 22 tests, 471 lines)
- But the route registration in `hivenode/routes/__init__.py` was removed
- All 22 tests are currently failing because the routes are not mounted

**What exists:**
- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- Router defined: `router = APIRouter(prefix="/api/des", tags=["des-engine"])`
- Endpoints: `/api/des/run`, `/api/des/validate`, `/api/des/replicate`, `/api/des/status`
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py`

**Current state of __init__.py:**
- Line 3: Import statement does NOT include `des_routes`
- Lines 15-43: `create_router()` function does NOT register `des_routes.router`
- Other routes (ledger, shell, rag, efemera, phase_ir, etc.) are registered correctly

---

## What Needs to Happen

Create a single task file for a bee to:

1. **Import `des_routes`** in line 3 of `hivenode/routes/__init__.py`
2. **Register the router** in the `create_router()` function with:
   - Prefix: `/api/des` (already in the router definition, so it's redundant but explicit)
   - Tags: `['des']` or `['des-engine']` (match the router definition)
3. **Run the 22 tests** in `tests/hivenode/test_des_routes.py` to verify all pass
4. **Run other route tests** to verify no regressions

---

## Constraints

- **Model:** haiku (simple import + registration task)
- **TDD:** Tests already exist (22 tests), bee must verify they all pass
- **No new code:** Just registration — do NOT modify `des_routes.py` itself
- **File size:** `__init__.py` is 44 lines, will grow to ~46 lines (well under 500)
- **No stubs:** N/A (just registration)
- **Response file:** Bee must write full 8-section response to `.deia/hive/responses/`

---

## Files the Bee Should Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current state)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (to see router definition)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py` (to understand what will be tested)

---

## Acceptance Criteria

- [ ] `des_routes` imported in `hivenode/routes/__init__.py` (line 3 area)
- [ ] Router registered in `create_router()` function with appropriate prefix and tags
- [ ] All 22 tests in `tests/hivenode/test_des_routes.py` pass
- [ ] No regressions in other route tests (run full backend test suite to verify)

---

## Expected Deliverables

1. Modified file: `hivenode/routes/__init__.py`
2. Test results: 22/22 DES route tests passing
3. Build verification: No regressions in other route tests
4. Response file: `.deia/hive/responses/20260316-TASK-R01-RESPONSE.md` (8 sections)

---

## Q33N Instructions

1. **Read this briefing completely**
2. **Read the three files** listed above to understand current state
3. **Write a single task file** to `.deia/hive/tasks/2026-03-16-TASK-R01-re-register-des-routes.md`
4. **Include all required sections** (objective, context, files to read, deliverables, test requirements, constraints, response requirements)
5. **Return to Q33NR for review** — do NOT dispatch the bee yet
6. **Wait for Q33NR approval** before dispatching

---

## Reference: Spec Location

Original spec: `.deia/hive/queue/2026-03-15-2300-SPEC-rebuild-R01-des-routes.md`

Task file location (Q33N will create): `.deia/hive/tasks/2026-03-15-TASK-R01-re-register-des-routes.md`

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-2300-SPE
**Event:** QUEUE_BRIEFING_WRITTEN
**Timestamp:** 2026-03-16T[current-time]
