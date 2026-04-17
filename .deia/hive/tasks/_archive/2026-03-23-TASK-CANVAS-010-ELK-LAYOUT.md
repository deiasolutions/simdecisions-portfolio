# TASK-CANVAS-010: Implement ELK Auto-Layout (Replacing Dagre)

## Objective
Implement ELK.js auto-layout for the flow-designer, replacing the old platform's dagre layout. Support all 4 directions, distribute functions, toolbar trigger, and LLM tool call integration.

## Context
Old platform used dagre for auto-layout (461 lines, 23 tests). New shiftcenter has NO auto-layout at all. We're upgrading to ELK (Eclipse Layout Kernel) which handles hierarchical layouts better — important for future group drill-down. Must support all layout features the old dagre system had.

**Old dagre features to replicate:**
- 4 directions: LR, RL, TB, BT
- Configurable spacing: nodeSep (80px), rankSep (120px), node dimensions
- Toolbar trigger: click=TB, shift+click=LR
- LLM tool call: `layout_actions` with auto_layout_lr/tb/rl/bt + distribute_horizontal/vertical
- Manual distribute horizontal (80px gap) and distribute vertical (100px gap)
- Handle position auto-set based on direction (LR→right/left, TB→bottom/top)
- Coordinate transform: center→top-left for ReactFlow compatibility

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\layout\dagre.ts` (68 lines — layout algorithm)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\layout\index.ts` (exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\hooks\useLayout.ts` (16 lines — React hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\layout\__tests__\dagre.test.ts` (78 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\layout\__tests__\dagre.direction.test.ts` (62 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\tools\canvas-tools.ts` (lines 104-131, layout_actions tool)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\controls\ZoomControls.tsx` (lines 54-68, toolbar button)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowToolbar.tsx`

## Deliverables
- [ ] Install `elkjs` package: `cd browser && npm install elkjs`
- [ ] `browser/src/apps/sim/services/layout/elk.ts` — ELK layout engine wrapper
  - `layoutWithElk(nodes, edges, options): Promise<LayoutedNode[]>`
  - Support directions: LR, RL, TB, BT (mapped to ELK's `elk.direction`)
  - Options: nodeSep, rankSep, nodeWidth, nodeHeight
  - Handle position auto-set based on direction
  - Center→top-left coordinate transform for ReactFlow
- [ ] `browser/src/apps/sim/services/layout/distribute.ts` — manual distribute functions
  - `distributeHorizontal(nodes, minGap=80)` — sort by X, equalize spacing
  - `distributeVertical(nodes, minGap=100)` — sort by Y, equalize spacing
- [ ] `browser/src/apps/sim/services/layout/index.ts` — barrel exports
- [ ] `browser/src/apps/sim/hooks/useLayout.ts` — React hook: `const { applyLayout, distributeH, distributeV } = useLayout()`
- [ ] Toolbar integration: add auto-layout button to ZoomControls or FlowToolbar (click=TB, shift+click=LR)
- [ ] Test file: `browser/src/apps/sim/services/layout/__tests__/elk.test.ts` — 13+ tests matching old dagre test coverage
- [ ] Test file: `browser/src/apps/sim/services/layout/__tests__/distribute.test.ts` — 10+ tests matching old distribute tests

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 13+ ELK tests: LR ordering, TB ordering, no overlaps, handle positions for all 4 directions, edge labels, node preservation
- [ ] 10+ distribute tests: horizontal/vertical, overlapping nodes, single node, normalization

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — layout must actually reposition nodes
- ELK is async (returns Promise) — handle this in the hook and toolbar
- Port the test patterns from old dagre tests — same assertions, different engine

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-010-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — anything that didn't work, edge cases, recommended next tasks

DO NOT skip any section.
