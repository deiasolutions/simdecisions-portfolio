# SPEC: Wire Properties Panel to Canvas Node Selection

## Priority
P1

## Objective
Wire node:selected bus event to open PropertyPanel with selected node data. Wire node:property-changed from PropertyPanel back to canvas to update the node in real-time. Both components exist and are ported — they need bus event wiring.

## Context
Files to read first:
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (canvas, onDrop handler at lines 302-358)
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx`
- `browser/src/apps/sim/components/flow-designer/useNodeEditing.ts` (line 159: emits node_properties_saved)
- `browser/src/apps/sim/components/flow-designer/properties/GeneralTab.tsx`
- `browser/src/apps/sim/components/flow-designer/properties/TimingTab.tsx`
- `browser/src/infrastructure/relay_bus/` (bus event system)

## Acceptance Criteria
- [ ] Clicking a node on canvas emits node:selected bus event with node data
- [ ] PropertyPanel listens for node:selected and opens with the selected node's properties
- [ ] Editing a property in PropertyPanel emits node:property-changed bus event
- [ ] FlowDesigner listens for node:property-changed and updates the canvas node in real-time
- [ ] Clicking canvas background (deselect) closes PropertyPanel
- [ ] PropertyPanel shows correct tab content for different node types (source, activity, gateway, etc.)
- [ ] CSS uses var(--sd-*) only
- [ ] 5+ tests for selection → edit → update flow
- [ ] No file over 500 lines

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-16-1501-SPEC-w2-03-properties-canvas-wire", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-16-1501-SPEC-w2-03-properties-canvas-wire", "files": ["path/to/file1.ts"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done, release early: POST http://localhost:8420/build/release

## Smoke Test
- [ ] Click node → PropertyPanel opens with node data
- [ ] Edit property → canvas node updates immediately
- [ ] Click background → PropertyPanel closes
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/
- [ ] No new test failures

## Model Assignment
haiku
