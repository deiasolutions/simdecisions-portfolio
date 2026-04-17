# TASK-242: Full Smoke Test Suite Against Production -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-17
**Role:** Q33N (Coordinator)

## Files Modified

Created:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-242-A-playwright-smoke-expansion.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-242-B-backend-api-smoke.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-242-RESPONSE.md`

## What Was Done

- Read BOOT.md and HIVE.md to understand Q33N role and workflow
- Read briefing TASK-242 from Q33NR
- Analyzed existing smoke test patterns in `browser/e2e/deploy-smoke.spec.ts`
- Analyzed E2E test patterns in `tests/hivenode/test_e2e.py`
- Reviewed auth dependency patterns in `hivenode/routes/auth.py` and `hivenode/routes/shell.py`
- Created TASK-242-A for Playwright smoke test expansion (5 new tests)
- Created TASK-242-B for backend API smoke tests (3 new tests)
- Task breakdown follows bee-sized units: frontend tests (Haiku), backend tests (Haiku)

## Task Breakdown Summary

### TASK-242-A: Expand Playwright Smoke Tests (Haiku)
**Deliverables:**
- Add 5 new tests to `browser/e2e/deploy-smoke.spec.ts`
- Tests cover: landing branding, efemera EGG, protected API rejection, FAB menu, theme toggle
- Tests 4 & 5 gracefully skip if features not exposed in production
- Total test count: 9 → 14 tests
- File size: 166 → ~226 lines (under 500 limit)

**Tests:**
1. Landing page branding (verify "ShiftCenter" text)
2. Efemera EGG 4-pane layout (verify pane count ≥ 4)
3. Protected API rejection (POST /api/shell/exec returns 401/403)
4. FAB menu interaction (conditional skip if not exposed)
5. Theme toggle (conditional skip if not exposed)

### TASK-242-B: Create Backend API Smoke Tests (Haiku)
**Deliverables:**
- Create `tests/smoke/test_production_api.py` with 3 tests
- Tests verify: /health endpoint, /api/shell/exec rejection, /efemera/channels behavior
- Tests gracefully skip if production URL unreachable
- Fast execution (< 5 seconds total)
- File size: < 150 lines

**Tests:**
1. `/health` returns 200 with "ok" or "healthy" status
2. `/api/shell/exec` rejects without auth (401 or 403)
3. `/efemera/channels` behavior verified (logs INFO if no auth check yet)

## Test Count Projection

**Before:**
- Playwright: 9 tests
- Backend smoke: 0 tests
- Total: 9 tests

**After:**
- Playwright: 14 tests (+5)
- Backend smoke: 3 tests (+3)
- Total: 17 tests (+8)

## Acceptance Criteria

From briefing:
- [x] `browser/e2e/deploy-smoke.spec.ts` will have 13-15 tests total (targeting 14)
- [x] New tests will cover: landing branding, efemera EGG, auth rejection, FAB menu, theme toggle
- [x] `tests/smoke/test_production_api.py` will exist with 3 tests (health, shell reject, efemera behavior)
- [x] All tests will use existing patterns (no new frameworks)
- [x] Tests gracefully skip if production unreachable or features not exposed
- [x] Run instructions documented in file headers
- [x] Task breakdown follows bee-sized units (2 tasks, both Haiku model)

## Clock / Cost / Carbon

- **Clock:** 18 minutes (reading context, writing task files, response)
- **Cost:** ~$0.15 USD (Sonnet API calls for reading + task writing)
- **Carbon:** ~15g CO2e (estimate based on Sonnet inference)

## Issues / Follow-ups

### Observations
1. **Efemera routes have NO auth checks** currently (per `hivenode/efemera/routes.py`). TASK-242-B test logs this but doesn't fail.
2. **FAB menu and theme toggle may not be exposed** in production yet. Tests gracefully skip with console.log.
3. **Shell exec endpoint uses verify_jwt_or_local** which bypasses auth in local mode, but enforces in cloud mode.
4. **Protected API test (TASK-242-A, test 3)** uses Playwright `page.request.post()` to test `/api/shell/exec` without auth.

### Recommendations
1. **Run TASK-242-A and TASK-242-B in parallel** — they are independent (frontend vs backend)
2. **Deploy TASK-241 first** (Production URL verification) to ensure target URL is reachable
3. **Add auth checks to efemera routes** if not already planned (currently open endpoints)
4. **Document theme toggle location** if it exists (TASK-242-A test 5 selector is TBD)

### Next Steps for Q33NR
1. Review task files for completeness
2. Approve dispatch if satisfied
3. Q33N will dispatch both bees in parallel (independent work)
4. Q33N will monitor and review bee responses
5. Q33N will report results to Q33NR when complete

## Questions for Q33NR

1. **Efemera auth:** Should efemera routes require authentication? Currently they don't check auth. TASK-242-B handles both cases (logs INFO if no auth).
2. **Theme toggle location:** Where is the theme switcher exposed in production UI? TASK-242-A test 5 uses `[aria-label="Toggle theme"]` but may need adjustment.
3. **Dispatch priority:** Should TASK-242 wait for TASK-241 completion, or run in parallel?

## Ready for Review

Task files are complete and ready for Q33NR review. Awaiting approval to dispatch bees.
