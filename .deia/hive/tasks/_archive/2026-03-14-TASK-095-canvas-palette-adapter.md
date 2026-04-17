# TASK-095: Build Canvas Palette Adapter

## Objective
Create a tree-browser adapter that displays the canvas node palette — the list of node types users can drag onto the canvas.

## Context
ShiftCenter uses tree-browser adapters to populate the left sidebar. See `channelsAdapter.ts` for the pattern. The palette adapter shows node types grouped by category (Process, Flow Control, Resources, Events).

Note: The old repo did NOT have a drag-from-palette — users added nodes via chat or context menu. This palette is NEW behavior, built fresh using the existing tree-browser adapter pattern.

## Dependencies
- **TASK-092 must be complete** (provides `browser/src/types/ir.ts` with NodeType enum)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\types\ir.ts` (from TASK-092)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`

## Deliverables
- [ ] Create `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts` (~120 lines)
  - Export `createPaletteAdapter()` following the channelsAdapter pattern
  - Return TreeNodeData[] grouped by category:
    - **Process**: Task, Queue
    - **Flow Control**: Start, End, Decision, Checkpoint
    - **Parallel**: Parallel Split, Parallel Join
    - **Resources**: Group
  - Each leaf node has `draggable: true` and `data.nodeType` matching the NodeType enum
  - Publish `palette:node-drag-start` on drag start (payload: { nodeType: NodeType })
- [ ] Create `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts` — 5+ tests:
  - Loads node types as TreeNodeData array
  - Groups by category (4 groups)
  - Each leaf item has draggable: true
  - Each leaf has data.nodeType matching NodeType enum
  - Publishes palette:node-drag-start on drag

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- Follow the exact channelsAdapter pattern
- Node type data is hardcoded (not fetched from API) — it's a static palette

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-095-RESPONSE.md`

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

## Model Assignment
haiku
