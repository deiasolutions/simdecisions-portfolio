# TASK-140: SimDecisions Shell Integration (Phase 1)

## Objective
Create simAdapter.tsx, sim.egg.md, and APP_REGISTRY entry to wire the existing FlowDesigner component into the ShiftCenter shell, enabling `?egg=sim` to load the flow designer.

## Context
The SimDecisions FlowDesigner component (818 lines) exists at `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`. It has 5 modes (Design, Simulate, Playback, Tabletop, Compare), full toolbar, property panels, and file ops. The component uses ApiClientContext for API calls and has a LocalDESEngine fallback for client-side simulation.

This task connects the FlowDesigner to the shell's app registry using the same pattern as canvasAdapter.tsx (32 lines). The adapter wraps FlowDesigner, passes the bus from ShellCtx, and makes it launchable via EGG.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\canvasAdapter.tsx` (32 lines, pattern to follow)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` (APP_REGISTRY, add sim entry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md` (schema_version 3 EGG pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (first 50 lines for props interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts` (AppRendererProps interface)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\simAdapter.tsx`
  - Import FlowDesigner from `../apps/sim/components/flow-designer/FlowDesigner`
  - Import ShellCtx from `../infrastructure/relay_bus`
  - Import AppRendererProps from `../shell/components/appRegistry`
  - Export SimAdapter function component accepting AppRendererProps
  - Extract bus from ShellCtx context
  - Wrap FlowDesigner with ApiClientProvider (needed by FlowDesigner)
  - Pass paneId as nodeId, pass bus, pass empty initialNodes/initialEdges (demo flow will load inside)
  - Follow canvasAdapter.tsx pattern exactly (approx 40 lines)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md`
  - YAML frontmatter: `egg: sim`, `version: 1.0.0`, `schema_version: 3`, `displayName: "SimDecisions Flow Designer"`, `description: "Visual BPMN flow designer with DES simulation engine. Design, simulate, playback, tabletop, compare."`, `defaultRoute: /sim`, `_stub: false`
  - Single pane layout block (JSON): `{"type": "pane", "appType": "sim", "nodeId": "sim-designer", "label": "SimDecisions", "chrome": false}`
  - Empty `modes`, `ui`, `tabs`, `commands`, `prompt`, `settings`, `away`, `startup` blocks (keep structure, minimal content)
  - Total approx 100 lines
- [ ] Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`
  - Import SimAdapter from `./simAdapter`
  - Add `registerApp('sim', SimAdapter)` call in `registerApps()` function
  - Place after BuildMonitorAdapter registration (alphabetical)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\simAdapter.test.tsx`
  - Test: renders FlowDesigner component when mounted
  - Test: passes paneId to FlowDesigner as nodeId prop
  - Test: wraps FlowDesigner with ApiClientProvider
  - Test: extracts bus from ShellCtx and passes to FlowDesigner
  - Mock ShellCtx with vi.mock
  - Mock FlowDesigner with vi.mock (return div with test-id)
  - Verify FlowDesigner receives correct props (toHaveBeenCalledWith)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\resolveEgg.sim.test.tsx`
  - Test: resolveCurrentEgg() returns sim EGG for `?egg=sim` query param
  - Test: resolveCurrentEgg() returns sim EGG for `/sim` path
  - Test: APP_REGISTRY has 'sim' entry after registerApps()
  - Use existing resolveCurrentEgg function (do not rewrite)
- [ ] All tests pass
- [ ] No existing tests break (run full browser suite)
- [ ] Edge cases: missing bus (null check), missing config (default to empty object)

## Constraints
- No file over 500 lines (all deliverables under 100 lines each)
- CSS: `var(--sd-*)` only (no CSS in this task, but note for future)
- No stubs — every function fully implemented
- Do NOT modify FlowDesigner.tsx or any existing sim component
- Do NOT add backend routes or engine integration (Phase 2 task)
- SimAdapter must work even if backend is unreachable (LocalDESEngine fallback is built into FlowDesigner)

## Acceptance Criteria
After this task:
- [ ] `localhost:5174/?egg=sim` renders FlowDesigner with toolbar, canvas, node palette visible
- [ ] Can drag a TASK node onto the canvas (existing FlowDesigner functionality)
- [ ] APP_REGISTRY contains 'sim' entry
- [ ] resolveCurrentEgg() returns sim EGG for `?egg=sim` and `/sim`
- [ ] All new tests pass (minimum 6 tests total)
- [ ] All existing browser tests still pass (no regressions)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-140-RESPONSE.md`

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
