# TASK-CANVAS-004: Port Configure Mode

## Objective
Port ConfigureView from old platform to new shiftcenter as ConfigureMode. This mode provides validation panel + sim config panel + read-only canvas for pre-simulation setup.

## Context
Configure mode exists in old platform (`simdecisions-2/src/components/mode-views/ConfigureView.tsx`, 158 lines) but is completely missing in new platform. Audit report line 42 confirms regression.

ConfigureMode is a pre-simulation step where users:
1. Review validation errors/warnings on the flow
2. Configure simulation parameters (runs, seed, duration)
3. View flow in read-only mode (can't edit during config)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\ConfigureView.tsx` (old implementation, 158 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\SimulateMode.tsx` (similar mode, good pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (lines 155-160: FlowMode type, needs 'configure' added)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (mode switch logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\SimConfigPanel.tsx` (can reuse for config panel)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (lines 50-51: sidebar panel config, needs configure entry)

## CRITICAL ARCHITECTURE REQUIREMENT
All panels (validation, sim config) MUST be shell panes defined in the EGG, NOT custom absolute-positioned divs. Use the pane adapter pattern established by TASK-CANVAS-000. Panels communicate via MessageBus events, not React props. Read the adapters created by CANVAS-000 in `browser/src/apps/sim/adapters/` and follow that pattern. If CANVAS-000 has not run yet, create the adapter yourself following the pattern in `browser/src/apps/textPaneAdapter.tsx`.

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/modes/ConfigureMode.tsx` (~200 lines max)
- [ ] Validation panel as a shell pane adapter (reuse existing validation UI, wrap in adapter)
- [ ] Sim config panel integration via existing `sim-config-panel` pane adapter
- [ ] Read-only canvas rendering (disable drag, disable connect, disable node edits)
- [ ] Update `canvas.egg.md` to define configure mode pane layout (validation pane left, sim config pane right)
- [ ] Add `'configure'` to FlowMode type in `types.ts`
- [ ] Register ConfigureMode in `FlowDesigner.tsx` mode switch (lines 550+)
- [ ] Add "Configure" sidebar panel to `canvas.egg.md` (icon: "⚙️", action: `sim:mode-change`, payload: `{ mode: "configure" }`)
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/modes/__tests__/ConfigureMode.test.tsx`
- [ ] Integration test: switch to configure mode → canvas becomes read-only → validation panel appears

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Flow with validation errors — errors display in validation panel
  - Flow with no errors — validation panel shows "✓ No issues"
  - Switch from design → configure → design — mode changes correctly
  - Configure mode: drag nodes disabled, connect edges disabled
  - Sim config changes in panel → update state (don't run sim yet, just config)

## Constraints
- No file over 500 lines (ConfigureMode.tsx under 200 lines)
- CSS: var(--sd-*) only
- No stubs — fully implement validation panel, config panel, read-only canvas
- Reuse existing components where possible (SimConfigPanel, validation logic from useSimulation)
- Read-only canvas: set `nodesDraggable={false}`, `edgesUpdatable={false}`, `nodesConnectable={false}` on ReactFlow

## Acceptance Criteria
- [ ] ConfigureMode.tsx created
- [ ] Validation panel displays flow validation results
- [ ] Sim config panel displays and edits SimConfig
- [ ] Canvas is read-only in configure mode (no drag, no connect)
- [ ] FlowMode type includes 'configure'
- [ ] ConfigureMode registered in FlowDesigner mode switch
- [ ] Canvas.egg.md includes Configure sidebar panel entry
- [ ] Test file exists with 8+ tests
- [ ] Integration test verifies read-only behavior
- [ ] All existing tests pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-004-RESPONSE.md` with all 8 sections.
