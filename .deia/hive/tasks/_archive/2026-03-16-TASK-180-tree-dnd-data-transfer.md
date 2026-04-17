# TASK-180: Wire TreeNodeRow drag data transfer

## Objective
Enable TreeNodeRow to set dataTransfer data on drag start, reading from node.meta.dragMimeType and node.meta.dragData, so draggable tree nodes can transfer payload to drop targets.

## Context
TreeNodeRow already has `draggable` and `onDragStart` support, but it doesn't populate e.dataTransfer. The simPaletteAdapter provides nodes with `meta.dragMimeType` ('application/phase-node') and `meta.dragData` (the PaletteItem object). FlowDesigner.onDrop already reads this data. We just need to wire the middle layer.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (46-49: current handleDragStart)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPaletteAdapter.ts` (26-38: meta shape)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (304-308: drop handler expecting this data)

## Deliverables
- [ ] Update TreeNodeRow.handleDragStart to:
  - Read `node.meta.dragMimeType` and `node.meta.dragData`
  - If both present, call `e.dataTransfer.setData(mimeType, JSON.stringify(dragData))`
  - Set `e.dataTransfer.effectAllowed = 'copy'`
- [ ] No change required to TreeNodeRow props (meta is already in TreeNodeData.meta)
- [ ] Test written FIRST covering:
  - Drag start with dragMimeType + dragData → setData called
  - Drag start with missing meta → no setData call
  - Drag disabled node → no setData call

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.drag.test.tsx`
- [ ] All tests pass
- [ ] Edge cases:
  - node.draggable = false → no data transfer
  - node.disabled = true → no data transfer
  - node.meta missing → no data transfer
  - node.meta.dragMimeType missing → no data transfer
  - node.meta.dragData present → JSON.stringify called

## Constraints
- No file over 500 lines (TreeNodeRow.tsx currently 102 lines, safe)
- CSS: var(--sd-*) only (no CSS changes)
- No stubs (fully implement all functions)
- TDD: tests first

## Acceptance Criteria
- [ ] TreeNodeRow sets dataTransfer on drag start when meta.dragMimeType + meta.dragData present
- [ ] Tests pass (5+ test cases)
- [ ] No regression on existing TreeNodeRow.test.tsx tests
- [ ] Smoke test: `cd browser && npx vitest run src/primitives/tree-browser/`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-180-RESPONSE.md`

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
