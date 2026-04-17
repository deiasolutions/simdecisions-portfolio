# TASK-CANVAS-001: Wire Terminal → IR → Canvas Pipeline

## Objective
Wire the end-to-end LLM → IR → Canvas pipeline so that when a user talks to the terminal with `routeTarget: 'ir'`, the LLM generates PHASE-IR, and the IR appears as nodes on the canvas.

## Context
The infrastructure exists but is not connected:
- Terminal sends `terminal:ir-deposit` bus event when LLM generates IR (verified in `terminalResponseRouter.ts` line 187)
- Canvas EGG declares `terminal:ir-deposit` in `bus_receive` permissions (`eggs/canvas.egg.md` line 292)
- FlowDesigner has no bus subscription to receive `terminal:ir-deposit`
- Old platform had this working (TabletopView, AIAssistantPanel created nodes from LLM output)

The terminal `routeTarget: 'ir'` mode splits LLM responses into chat text (routes to text-pane) and IR JSON (routes to canvas). Currently the text routing works but the IR routing does not.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts` (lines 184-194: IR routing)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (main component, needs bus subscription)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\useFlowState.ts` (addNode function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (lines 118-127: terminal config with `links.to_ir`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (message envelope types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 45-46: routeTarget option)

## Deliverables
- [ ] Add bus subscription in `FlowDesigner.tsx` or `useFlowState.ts` that listens for `terminal:ir-deposit` events
- [ ] Parse incoming IR data and convert to ReactFlow nodes/edges
- [ ] Add nodes to canvas via `addNode()` or `setNodes()`
- [ ] Position new nodes intelligently (spread layout, not all at 0,0)
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/ir-deposit.test.tsx` — verify bus event → nodes appear
- [ ] Integration test: terminal with `routeTarget: 'ir'` → mock LLM response with IR → canvas receives nodes
- [ ] Document IR format expected (likely PHASE-IR JSON: `{ nodes: [...], edges: [...] }` or similar)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - IR with no nodes (empty object) — should not crash
  - IR with nodes but no edges — nodes appear, no edges
  - IR with invalid node IDs — handle gracefully (log warning, skip invalid)
  - Multiple `terminal:ir-deposit` events in sequence — additive (append nodes, don't replace)
  - IR includes existing node IDs — dedupe or increment IDs

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs — full implementation
- IR must route ONLY to the target pane specified in terminal config `links.to_ir` (currently `"canvas-editor"` in canvas.egg.md line 125)
- Do NOT break existing canvas functionality (drag-drop from palette, manual node creation)

## Acceptance Criteria (Mark [x] when done)
- [ ] Bus subscription added to FlowDesigner or useFlowState that listens for `terminal:ir-deposit`
- [ ] IR parser converts PHASE-IR JSON to ReactFlow node/edge format
- [ ] Nodes appear on canvas when `terminal:ir-deposit` event is sent
- [ ] New nodes are positioned intelligently (spread layout or center + offset)
- [ ] Test file exists: `ir-deposit.test.tsx` with 5+ tests
- [ ] Integration test verifies end-to-end terminal → IR → canvas flow
- [ ] All existing canvas tests still pass (no regressions)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-001-RESPONSE.md`

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
