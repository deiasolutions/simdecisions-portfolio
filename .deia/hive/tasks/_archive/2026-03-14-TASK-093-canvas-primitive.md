# TASK-093: Build Canvas Primitive

## Objective
Create the core canvas primitive using ReactFlow v12, rendering PHASE-IR graphs with custom nodes, edges, and bus integration.

## Context
This is the main canvas component for ShiftCenter. It renders PHASE-IR graphs (from TASK-092 types) using ReactFlow. The old repo had a 633-line `Canvas.tsx` — we must modularize to stay under 500 lines per file.

The `to_ir` bus handler already exists in `terminalResponseRouter.ts:184-194` — it publishes `terminal:ir-deposit`. The canvas listens for that event.

## Dependencies
- **TASK-092 must be complete** (provides `browser/src/types/ir.ts`)
- ReactFlow must be installed: `@xyflow/react ^12.10.1`, `dagre ^0.8.5`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\types\ir.ts` (from TASK-092)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts` (to_ir handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` (pattern reference for primitive structure)

## Deliverables

### Step 0: Install dependencies
- [ ] Run: `cd browser && npm install @xyflow/react@^12 dagre@^0.8.5`

### Step 1: Create canvas files
- [ ] `browser/src/primitives/canvas/CanvasApp.tsx` (~250 lines) — Main ReactFlow wrapper, bus listeners, dagre layout
- [ ] `browser/src/primitives/canvas/CanvasNodeTypes.ts` (~100 lines) — Node type registry mapping NodeType enum to React components
- [ ] `browser/src/primitives/canvas/CanvasEdgeTypes.ts` (~50 lines) — Edge type registry
- [ ] `browser/src/primitives/canvas/CanvasControls.tsx` (~100 lines) — Zoom, minimap, grid controls
- [ ] `browser/src/primitives/canvas/canvas.css` — Canvas styles using `var(--sd-*)` only

### Step 2: Create custom node components (4 core types)
- [ ] `browser/src/primitives/canvas/nodes/StartNode.tsx` (~80 lines) — Green circle, single output handle
- [ ] `browser/src/primitives/canvas/nodes/EndNode.tsx` (~80 lines) — Red circle, single input handle
- [ ] `browser/src/primitives/canvas/nodes/TaskNode.tsx` (~100 lines) — Rounded rect with label, timing badge, input+output handles
- [ ] `browser/src/primitives/canvas/nodes/DecisionNode.tsx` (~100 lines) — Diamond shape, label, multiple output handles with probability labels

### Step 3: Create custom edge
- [ ] `browser/src/primitives/canvas/edges/CustomEdge.tsx` (~100 lines) — Smart edge with label, guard badge

### Step 4: Bus integration
- [ ] Listen for `terminal:ir-deposit` — receives IRGraph, calls setNodes/setEdges
- [ ] Publish `canvas:node-selected` when user clicks a node (payload: IRNode)
- [ ] Publish `canvas:edge-selected` when user clicks an edge (payload: IREdge)

### Step 5: Tests
- [ ] `browser/src/primitives/canvas/__tests__/CanvasApp.test.tsx` — 20+ tests:
  - Renders with zero nodes (empty state)
  - Renders with sample IR data (5 nodes, 4 edges)
  - Publishes `canvas:node-selected` on node click
  - Receives `terminal:ir-deposit` and updates graph
  - Each node type renders correct shape
  - Edge renders with label
  - Dagre layout positions nodes
  - Minimap renders
  - Grid renders
  - Zoom controls work

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs — every component must render real visuals
- All node shapes must be CSS (no SVG images)
- Do NOT port annotation nodes, lasso, or context menus — just the core 4 node types + edges

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-093-RESPONSE.md`

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
sonnet
