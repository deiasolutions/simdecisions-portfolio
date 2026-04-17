# TASK-142: SimDecisions Integration Tests (Phase 3)

## Objective
Write comprehensive integration tests for the full SimDecisions stack: adapter mount, EGG resolution, engine lifecycle, and existing sim component tests.

## Context
TASK-140 delivered simAdapter.tsx + sim.egg.md + APP_REGISTRY entry. TASK-141 delivered engine integration in sim.py. This task writes cross-cutting tests that verify the entire flow works end-to-end.

The frontend has 121 sim component files with existing tests in `browser/src/apps/sim/__tests__/`. The backend has sim route tests that were previously skipped. This task ensures all pieces work together.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\canvasAdapter.test.tsx` (pattern for adapter tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\resolveEgg.test.tsx` (pattern for EGG resolution tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (pattern for E2E tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_routes.py` (existing sim route tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\__tests__\` (directory listing — check what tests exist)

## Deliverables
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\simAdapter.integration.test.tsx`
  - Test: Full mount test — render simAdapter, verify FlowDesigner renders
  - Test: Verify canvas SVG element exists (FlowDesigner renders React Flow canvas)
  - Test: Verify toolbar renders (FlowDesigner has FlowToolbar component)
  - Test: Verify node palette renders (FlowDesigner has NodePalette component)
  - Mock ShellCtx with relay_bus
  - Mock ApiClientContext provider
  - Use `@testing-library/react` render + screen queries
  - Minimum 4 tests
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\resolveEgg.sim.integration.test.tsx`
  - Test: resolveCurrentEgg() with `?egg=sim` returns sim EGG
  - Test: resolveCurrentEgg() with path `/sim` returns sim EGG
  - Test: Resolved EGG has displayName "SimDecisions Flow Designer"
  - Test: Resolved EGG layout has appType "sim"
  - Test: APP_REGISTRY['sim'] is defined after registerApps()
  - Use existing resolveCurrentEgg function from shell
  - Mock window.location for query param tests
  - Minimum 5 tests
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_lifecycle.py`
  - Test: Full lifecycle — load → start → status=running → pause → status=paused → resume → status=running → tokens present
  - Test: Step mode — load → step → sim_time increases → step → sim_time increases
  - Test: Checkpoint/restore — load → start → checkpoint → advance → restore → sim_time reverts
  - Test: Fork — load → start → advance → fork → new run_id → both runs independent
  - Test: Sweep — load → sweep with 3 param sets → 3 results returned
  - Test: Events — load → start → get events → events list not empty
  - Use TestClient (sync)
  - Use demo PHASE-IR flow fixture (minimal flow with 2 tasks, 1 edge)
  - Minimum 6 tests
- [ ] Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_routes.py`
  - Remove all `@pytest.mark.skip` decorators
  - Fix any broken assertions caused by engine integration changes
  - Verify all tests pass
  - Do NOT rewrite tests unless assertions are broken
- [ ] Verify all existing sim frontend tests still pass
  - Run `cd browser && npx vitest run src/apps/sim/__tests__/`
  - If any fail, fix the failure (likely mock issues)
  - Do NOT skip or delete existing tests

## Test Requirements
- [ ] Tests written FIRST (TDD) — write integration tests before running TASK-140/141 code
- [ ] All new tests pass
- [ ] All existing browser tests pass (no regressions in sim component tests)
- [ ] All existing hivenode tests pass (unskipped sim route tests now run)
- [ ] Total new test count: minimum 15 tests across 3 new files
- [ ] Edge cases: missing run_id (404), invalid flow (400), adapter without bus (null check)

## Constraints
- No file over 500 lines (all test files under 200 lines)
- CSS: N/A (tests only)
- No stubs — every test fully implemented with real assertions
- Do NOT modify FlowDesigner.tsx or sim.py (those are TASK-140/141)
- Do NOT rewrite existing tests unless they are broken

## Acceptance Criteria
After this task:
- [ ] simAdapter integration test renders FlowDesigner with canvas, toolbar, palette
- [ ] EGG resolution tests confirm `?egg=sim` and `/sim` both resolve to sim EGG
- [ ] Lifecycle tests confirm load → start → pause → resume → status changes
- [ ] Step mode test confirms sim_time advances on each step
- [ ] Checkpoint/restore test confirms state reversion works
- [ ] Fork test confirms independent run_ids
- [ ] Sweep test confirms parameter sweep returns multiple results
- [ ] All unskipped sim route tests pass
- [ ] All existing sim frontend tests pass (no regressions)
- [ ] Total test count: minimum 15 new tests + all existing tests green

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-142-RESPONSE.md`

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
