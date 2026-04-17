# TASK-189: Wire FlowDesigner to Listen for node:property-changed and Update Canvas

## Objective
Subscribe to `node:property-changed` bus event in FlowDesigner and update the canvas node in real-time when properties are edited in PropertyPanel.

## Context
FlowDesigner needs to listen for property change events from PropertyPanel and update the node data in the React Flow state. The conversion logic already exists in `useNodeEditing.ts` `onPropertySave` function — reuse that logic.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

## Deliverables
- [ ] In FlowDesigner or useNodeEditing, subscribe to `node:property-changed` event
- [ ] When event received:
  - Find the node by nodeId
  - Convert NodeProperties to PhaseNodeData (reuse existing logic from onPropertySave)
  - Update nodes state with pushHistory()
  - Emit ledger event (already done in onPropertySave)
- [ ] Unsubscribe on unmount
- [ ] Tests written FIRST (TDD):
  - Test subscribes to node:property-changed
  - Test updates node when event received
  - Test converts properties correctly
  - Test pushes history
  - Test emits ledger event
  - Test unsubscribes on unmount

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Bus is null
  - Event for non-existent nodeId (should ignore)
  - Multiple rapid property changes
  - Property change in non-design mode

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-189-RESPONSE.md`

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
