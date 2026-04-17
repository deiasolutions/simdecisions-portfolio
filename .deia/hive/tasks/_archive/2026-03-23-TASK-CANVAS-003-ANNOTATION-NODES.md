# TASK-CANVAS-003: Port All 7 Annotation Node Types

## Objective
Port ALL 7 annotation node types from old platform to new shiftcenter flow-designer: AnnotationLine, AnnotationImage, Text, Rectangle, Ellipse, Callout, StickyNote.

## Context
Old platform had 7 annotation node types for flow documentation and visual markup. New platform has NONE. These are critical for:
- Documenting flows with text labels
- Drawing attention with callouts and sticky notes
- Visual grouping with shapes (rectangles, ellipses)
- Embedding images (logos, screenshots, diagrams)
- Freehand annotation with lines

Audit report (`.deia/hive/coordination/2026-03-23-CANVAS-COMPARISON-REPORT.md` lines 63-69) confirms all 7 are missing.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationLineNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationImageNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationTextNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationRectNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\AnnotationEllipseNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\CalloutNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\StickyNoteNode.tsx` (old implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx` (new node pattern to match)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (lines 36-44: NODE_TYPES registry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx` (PALETTE_ITEMS array)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (node data types)

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationLineNode.tsx` (~150 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationImageNode.tsx` (~150 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationTextNode.tsx` (~100 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationRectNode.tsx` (~100 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/AnnotationEllipseNode.tsx` (~100 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/CalloutNode.tsx` (~150 lines max)
- [ ] `browser/src/apps/sim/components/flow-designer/nodes/StickyNoteNode.tsx` (~150 lines max)
- [ ] Register all 7 in `FlowCanvas.tsx` NODE_TYPES map
- [ ] Add all 7 to `NodePalette.tsx` under a new "Annotations" category
- [ ] Add TypeScript types for node data: `AnnotationLineData`, `AnnotationImageData`, `AnnotationTextData`, etc. in `types.ts`
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/nodes/__tests__/annotationNodes.test.tsx` — verify render, props, editing
- [ ] Integration test: drag from palette → drop on canvas → annotation appears and is editable

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - AnnotationText with empty string — shows placeholder "Enter text..."
  - AnnotationImage with invalid URL — shows error icon or placeholder
  - CalloutNode with no text — shows empty bubble
  - StickyNote with long text — text wraps, scrolls, or truncates
  - All 7: CSS variables only, no hardcoded colors
  - All 7: resizable (if applicable — rect, ellipse, image, sticky should be resizable)
  - AnnotationLine: supports multiple points (polyline, not just straight line)

## Constraints
- No file over 500 lines (each node file under 150 lines)
- CSS: var(--sd-*) only (no hex, no rgb, no named colors)
- No stubs — fully implement render, editing (text nodes must be editable inline)
- Match existing node pattern: use ReactFlow NodeResizer if resizable
- Icons for palette: use unicode or SVG (e.g., line: "─", image: "🖼", text: "T", rect: "▭", ellipse: "○", callout: "💬", sticky: "📝")
- AnnotationLine: use SVG path or polyline, not canvas
- AnnotationImage: use `<img>` tag, handle load errors gracefully

## Acceptance Criteria (Mark [x] when done)
- [ ] All 7 annotation node files created
- [ ] All 7 render correctly on canvas
- [ ] All 7 registered in FlowCanvas.tsx NODE_TYPES map
- [ ] All 7 appear in NodePalette.tsx under "Annotations" category
- [ ] TypeScript types added to types.ts for all 7
- [ ] Test file exists: `annotationNodes.test.tsx` with 15+ tests (2-3 per node type)
- [ ] Integration test: drag-drop from palette works for all 7 nodes
- [ ] Text nodes are editable inline (AnnotationText, Callout, StickyNote)
- [ ] No hardcoded colors (verified via grep)
- [ ] Resizable nodes work correctly (Rect, Ellipse, Image, Sticky)
- [ ] All existing canvas tests still pass (no regressions)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-003-RESPONSE.md`

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
