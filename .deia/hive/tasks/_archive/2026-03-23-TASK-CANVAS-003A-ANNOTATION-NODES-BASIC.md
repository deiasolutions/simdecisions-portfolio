# TASK-CANVAS-003A: Port Basic Annotation Nodes (Text, Rectangle, Ellipse, StickyNote)

## Objective
Port 4 basic annotation node types from old platform canvas to new shiftcenter flow-designer.

## Context
The old platform had 7 annotation node types. The new flow-designer has zero. This task ports the 4 simpler ones: text labels, rectangles, ellipses, and sticky notes. A parallel bee (CANVAS-003B) ports the 3 richer ones.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationTextNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationRectNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationEllipseNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\StickyNoteNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx` (reference pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (nodeTypes map, lines 36-44)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx` (palette registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (type definitions)

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationTextNode.tsx` — text label node with inline editing
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationRectNode.tsx` — rectangle shape annotation
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationEllipseNode.tsx` — ellipse shape annotation
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/StickyNoteNode.tsx` — sticky note with editable text
- [ ] Register all 4 in `FlowCanvas.tsx` nodeTypes map
- [ ] Add "Annotations" category in `NodePalette.tsx` with all 4 types
- [ ] Add TypeScript types in `types.ts` for all 4 node data interfaces
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/annotation-nodes-basic.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 8+ tests (2 per node type)
- [ ] Edge cases: empty text, text wrapping, resize handles, CSS variable compliance, no hardcoded colors

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only. No hex, no rgb(), no named colors
- No stubs — every node fully functional
- Port from old platform — don't reinvent

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-003A-RESPONSE.md`

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
