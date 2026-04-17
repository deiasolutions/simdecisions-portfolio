# TASK-CANVAS-003B: Port Rich Annotation Nodes (Line, Image, Callout)

## Objective
Port 3 rich annotation node types from old platform canvas to new shiftcenter flow-designer.

## Context
The old platform had 7 annotation node types. This task ports the 3 more complex ones: freehand lines (SVG polyline), embedded images, and callout bubbles. A parallel bee (CANVAS-003A) ports the 4 simpler ones.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationLineNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationImageNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\CalloutNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx` (reference pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (nodeTypes map)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts`

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationLineNode.tsx` — freehand line via SVG polyline
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationImageNode.tsx` — embedded image with error handling
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/CalloutNode.tsx` — callout bubble with pointer and editable text
- [ ] Register all 3 in `FlowCanvas.tsx` nodeTypes map
- [ ] Add to "Annotations" category in `NodePalette.tsx` (category may already exist from CANVAS-003A — add to it if so, create if not)
- [ ] Add TypeScript types in `types.ts` for all 3 node data interfaces
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/annotation-nodes-rich.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 8+ tests (2-3 per node type)
- [ ] Edge cases: invalid image URL, empty polyline points, callout pointer direction, SVG rendering, CSS variable compliance

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only. No hex, no rgb(), no named colors
- No stubs — every node fully functional
- Port from old platform — don't reinvent

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-003B-RESPONSE.md`

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
