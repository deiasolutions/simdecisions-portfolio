# TASK-181: Write integration test for tree-to-canvas drag-drop flow

## Objective
Write end-to-end integration test proving that dragging from tree-browser palette to FlowCanvas creates a node at the drop position.

## Context
All infrastructure exists:
- simPaletteAdapter provides TreeNodeData with dragMimeType + dragData
- TreeNodeRow (after TASK-180) sets dataTransfer
- FlowDesigner.onDrop creates nodes from dataTransfer

This task writes the integration test proving the full flow works.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPaletteAdapter.ts` (full file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (302-358: onDrop)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\Canvas.drop.test.tsx` (existing tests)

## Deliverables
- [ ] New test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\palette-to-canvas.test.tsx`
- [ ] Test scenarios:
  - Drag 'start' node from palette → drop on canvas → start node created at position
  - Drag 'node' (activity) → drop → phase-node created with duration
  - Drag 'checkpoint' → drop → checkpoint-node created with trueLabel/falseLabel
  - Drag 'resource' → drop → resource-node created with capacity
  - Drag 'group' → drop over existing nodes → group created with enclosed children
  - Drag 'end' → drop → end-node created
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD approach)
- [ ] Use simPaletteAdapter to get real palette items
- [ ] Mock screenToFlowPosition to return predictable coordinates
- [ ] Verify node.id, node.type, node.position, node.data match expectations
- [ ] All tests pass
- [ ] Edge cases:
  - Drop event with no dataTransfer → no node created
  - Drop event with wrong MIME type → no node created
  - Drop with malformed JSON → no crash

## Constraints
- No file over 500 lines (new test file should be ~150 lines)
- CSS: var(--sd-*) only (no CSS in test files)
- No stubs (fully implement all test scenarios)
- TDD: tests first

## Acceptance Criteria
- [ ] Integration test file created with 6+ scenarios
- [ ] All scenarios pass
- [ ] Test verifies node creation (id, type, position, data) for all node kinds
- [ ] Group drop-over-nodes scenario covered
- [ ] Smoke test: `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/palette-to-canvas.test.tsx`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-181-RESPONSE.md`

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
