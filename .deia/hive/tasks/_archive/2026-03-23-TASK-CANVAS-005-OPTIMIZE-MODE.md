# TASK-CANVAS-005: Port Optimize Mode

## Objective
Port OptimizeView from old platform to new shiftcenter as OptimizeMode. This mode provides parameter sweep controls, Pareto frontier visualization, and optimization engine integration.

## Context
Optimize mode exists in old platform (`simdecisions-2/src/components/mode-views/OptimizeView.tsx`, 479 lines) but is completely missing in new platform. Audit report line 43 confirms regression.

OptimizeMode allows users to:
1. Define parameter ranges for sweep (e.g., arrival rate 1-10, service time 5-15)
2. Run multi-variate optimization (explore parameter space)
3. Visualize Pareto frontier (trade-off curves)
4. Select optimal configurations

This is an ADVANCED feature. May require backend API for optimization engine.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\OptimizeView.tsx` (old implementation, 479 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\SimulateMode.tsx` (similar backend integration pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (FlowMode type)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (mode switch)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (DES backend, may need new `/api/des/optimize` endpoint)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\` (check if old platform had optimization backend)

## CRITICAL ARCHITECTURE REQUIREMENT
All panels (parameter sweep, Pareto chart, results) MUST be shell panes defined in the EGG, NOT custom absolute-positioned divs. Use the pane adapter pattern established by TASK-CANVAS-000. Panels communicate via MessageBus events, not React props. If CANVAS-000 has not run yet, create the adapter yourself following the pattern in `browser/src/apps/textPaneAdapter.tsx`.

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/modes/OptimizeMode.tsx` (split into smaller files if > 500 lines)
- [ ] Parameter sweep pane adapter (`browser/src/apps/sim/adapters/optimizeParamsPaneAdapter.tsx`)
- [ ] Pareto frontier / results pane adapter (`browser/src/apps/sim/adapters/optimizeResultsPaneAdapter.tsx`)
- [ ] Update `canvas.egg.md` to define optimize mode pane layout (params pane left, results pane right)
- [ ] Backend API route: `hivenode/routes/des_routes.py` add `POST /api/des/optimize` (or verify if already exists)
- [ ] Add `'optimize'` to FlowMode type in `types.ts`
- [ ] Register OptimizeMode in `FlowDesigner.tsx` mode switch
- [ ] Add "Optimize" sidebar panel to `canvas.egg.md`
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/modes/__tests__/OptimizeMode.test.tsx`
- [ ] Backend test: `tests/hivenode/test_des_optimize.py` (if new API route added)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Parameter ranges with min > max — validation error
  - Optimization with 0 parameters — error message "No parameters defined"
  - Optimization run fails (backend timeout) — show error in UI
  - Pareto frontier with single objective — degenerates to sorted list (handle gracefully)
  - Large parameter space (100+ combinations) — show progress bar

## Constraints
- No file over 500 lines (split OptimizeMode into subcomponents if needed)
- CSS: var(--sd-*) only
- No stubs — fully implement parameter sweep UI, Pareto chart, results table
- Backend API required — if old platform had `/api/optimize`, port it. If not, implement minimal version (parameter sweep via multiple `/api/des/run` calls client-side)
- Use chart library for Pareto viz (Recharts or similar, already in deps?)

## Acceptance Criteria
- [ ] OptimizeMode.tsx created (or split into optimize/ subdirectory)
- [ ] Parameter sweep panel allows defining parameter ranges
- [ ] Pareto frontier chart visualizes trade-offs
- [ ] Optimization results table shows all runs
- [ ] Backend API exists (`/api/des/optimize` or client-side multi-run logic)
- [ ] FlowMode type includes 'optimize'
- [ ] OptimizeMode registered in FlowDesigner mode switch
- [ ] Canvas.egg.md includes Optimize sidebar panel entry
- [ ] Frontend test file exists with 10+ tests
- [ ] Backend test exists (if new API route added)
- [ ] All existing tests pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-005-RESPONSE.md` with all 8 sections.
