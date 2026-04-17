# TASK-CANVAS-002: Port Process Flow Nodes (Split, Join, Queue)

## Objective
Port 3 missing process flow node types from old platform to new shiftcenter flow-designer: `split` (ParallelSplitNode), `join` (ParallelJoinNode), and `queue` (QueueNode).

## Context
Old platform had 16 node types. New platform has 6. Missing: 3 process flow types + 7 annotation types.

Process flow nodes are critical for DES modeling:
- `split` (ParallelSplitNode) — fork flow into parallel paths (AND-split)
- `join` (ParallelJoinNode) — merge parallel paths (AND-join, wait for all)
- `queue` (QueueNode) — resource queue (explicit queue vs implicit via resource-node)

These node types existed in old platform and were used in production diagrams. Audit report (`.deia/hive/coordination/2026-03-23-CANVAS-COMPARISON-REPORT.md` lines 58-60) confirms they're missing.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\ParallelSplitNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\ParallelJoinNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\QueueNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx` (new node pattern to match)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\ResourceNode.tsx` (similar node, good reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (lines 36-44: NODE_TYPES registry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx` (PALETTE_ITEMS array, needs new entries)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (node data type definitions)

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/SplitNode.tsx` — ParallelSplitNode port (~150 lines, keep under 200)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/JoinNode.tsx` — ParallelJoinNode port (~150 lines, keep under 200)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/QueueNode.tsx` — QueueNode port (~150 lines, keep under 200)
- [ ] Register all 3 in `FlowCanvas.tsx` NODE_TYPES map (add `"split-node": SplitNode`, `"join-node": JoinNode`, `"queue-node": QueueNode`)
- [ ] Add all 3 to `NodePalette.tsx` PALETTE_ITEMS array (icon, label, nodeType, draggable)
- [ ] Add TypeScript types for node data: `SplitNodeData`, `JoinNodeData`, `QueueNodeData` in `types.ts`
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/nodes/__tests__/processFlowNodes.test.tsx` — verify render, props, handles
- [ ] Integration test: drag from palette → drop on canvas → node appears with correct type

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Split node with 0 outgoing edges — should render, not crash
  - Join node with 1 incoming edge — should render (even if semantically incomplete)
  - Queue node with no capacity set — use default (e.g., Infinity)
  - All 3 nodes: custom colors via CSS variables, not hardcoded
  - All 3 nodes: handle positions correct (split has multiple output handles, join has multiple input handles)

## Constraints
- No file over 500 lines (each node file under 200 lines preferred)
- CSS: var(--sd-*) only (no hex, no rgb, no named colors)
- No stubs — fully implement render, handles, data types
- Match existing node pattern: use ReactFlow Handle component, position handles correctly
- Icon/label for palette must match old platform icons or use sensible unicode (e.g., split: "⑂", join: "⑃", queue: "⊟")

## Acceptance Criteria (Mark [x] when done)
- [ ] SplitNode.tsx created, renders correctly, has multiple output handles
- [ ] JoinNode.tsx created, renders correctly, has multiple input handles
- [ ] QueueNode.tsx created, renders correctly, displays capacity if set
- [ ] All 3 registered in FlowCanvas.tsx NODE_TYPES map
- [ ] All 3 appear in NodePalette.tsx and are draggable
- [ ] TypeScript types added to types.ts (SplitNodeData, JoinNodeData, QueueNodeData)
- [ ] Test file exists: `processFlowNodes.test.tsx` with 10+ tests (3-4 per node type)
- [ ] Integration test: drag-drop from palette works for all 3 nodes
- [ ] No hardcoded colors (verified via grep)
- [ ] All existing canvas tests still pass (no regressions)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-002-RESPONSE.md`

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
