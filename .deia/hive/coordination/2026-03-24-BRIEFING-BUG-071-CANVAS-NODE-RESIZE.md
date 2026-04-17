# BRIEFING: BUG-071 Canvas Node Selection and Resize

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-24-SPEC-BUG)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-24
**Model:** Sonnet
**Priority:** P1

---

## Objective

Add pointer/select tool functionality to the canvas2 primitive and enable resize handles on all 7 annotation node types. Currently users can drag-drop nodes from the palette onto the canvas and move them, but cannot select individual nodes for editing or resize them after placement.

---

## Context

The canvas primitive uses ReactFlow and has 22 node types:
- 9 core PHASE-IR types (start, end, task, decision, checkpoint, split, join, queue, group)
- 6 BPMN types (bpmn-start, bpmn-end, bpmn-task, bpmn-gateway, bpmn-subprocess, bpmn-event)
- 7 annotation types (annotation-ellipse, annotation-image, annotation-line, annotation-rect, annotation-text, sticky-note, callout)

**Current state:**
- Nodes can be placed on canvas via drag-drop from palette
- Node selection already exists (ReactFlow built-in) and publishes `canvas:node-selected` bus events
- Visual selection feedback exists (the `selected` prop is passed to all node components)
- Resize handles are NOT present on any annotation nodes
- Annotation nodes use fixed dimensions (width/height from data or hardcoded defaults)

**What needs to happen:**
1. Add `NodeResizer` from `@xyflow/react` to all 7 annotation node types
2. Store resized dimensions in node data (width/height fields)
3. Ensure process flow nodes (start, end, task, etc.) remain fixed-size
4. Add CSS for resize handle styling using `var(--sd-*)` variables only

**Files to understand:**
- `browser/src/primitives/canvas/CanvasApp.tsx` — main canvas component (592 lines)
- `browser/src/primitives/canvas/canvasTypes.ts` — NodeData interface (already has width/height fields)
- `browser/src/primitives/canvas/nodes/AnnotationRectNode.tsx` — rect annotation (47 lines)
- `browser/src/primitives/canvas/nodes/AnnotationEllipseNode.tsx` — ellipse annotation (46 lines)
- `browser/src/primitives/canvas/nodes/AnnotationImageNode.tsx` — image annotation (63 lines)
- `browser/src/primitives/canvas/nodes/CalloutNode.tsx` — callout speech bubble (50 lines)
- `browser/src/primitives/canvas/nodes/StickyNoteNode.tsx` — sticky note (50 lines)
- `browser/src/primitives/canvas/nodes/AnnotationLineNode.tsx` — line annotation (not read yet)
- `browser/src/primitives/canvas/nodes/AnnotationTextNode.tsx` — text annotation (not read yet)

**ReactFlow NodeResizer API:**
- Import: `import { NodeResizer } from '@xyflow/react';`
- Usage: Add `<NodeResizer />` as a child in the node component
- Props: `minWidth`, `minHeight`, `color`, `handleStyle`, `lineStyle`
- Automatically updates node dimensions in ReactFlow state
- Requires node to have `selected` prop to show handles

---

## Deliverables

Q33N should write a single task file that delivers:

1. **Add NodeResizer to 7 annotation node types**
   - Import `NodeResizer` from `@xyflow/react`
   - Add `<NodeResizer />` component to each annotation node
   - Set min dimensions (minWidth: 60, minHeight: 40 or similar)
   - Style handles using `var(--sd-*)` variables

2. **Update node dimensions on resize**
   - ReactFlow automatically updates node dimensions
   - Ensure node inline styles use `data.width` and `data.height` from NodeData
   - All annotation nodes already read width/height from data — verify this persists after resize

3. **Ensure process flow nodes remain fixed-size**
   - Do NOT add NodeResizer to: start, end, task, decision, checkpoint, split, join, queue, group, bpmn-*
   - These nodes should not be resizable

4. **CSS styling for resize handles**
   - Add styles to `browser/src/primitives/canvas/canvas.css`
   - Use `var(--sd-*)` variables only (Rule 3)
   - Style classes: `.react-flow__resize-control`, `.react-flow__resize-control-handle`
   - Colors: border, background, hover states

5. **Tests (minimum 5)**
   - Test: Clicking an annotation node shows resize handles
   - Test: Dragging resize handle changes node dimensions
   - Test: Resized dimensions persist in node data (width/height fields)
   - Test: Process flow nodes do NOT show resize handles when selected
   - Test: Resize handles styled with CSS variables (no hardcoded colors)

---

## Constraints

- **Rule 3:** All CSS uses `var(--sd-*)` variables only. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. Modularize at 500.
- **Rule 5:** TDD. Tests first, then implementation.
- **Rule 6:** No stubs. Every function fully implemented.

---

## File Paths (absolute)

All paths must be absolute (Windows format):

- **Canvas app:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- **Types:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvasTypes.ts`
- **CSS:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css`
- **Annotation nodes:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\Annotation*.tsx`
- **Sticky note:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\StickyNoteNode.tsx`
- **Callout:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\CalloutNode.tsx`

---

## Test Requirements

- **Minimum 5 tests** covering:
  - Node selection shows resize handles (annotation nodes only)
  - Resize handle interaction changes dimensions
  - Dimension persistence in node data
  - Process flow nodes NOT resizable
  - CSS variable usage (no hardcoded colors)

- **Test file location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-node-resize.test.tsx`

---

## Response File

When complete, bee writes:
`.deia/hive/responses/20260324-TASK-BUG-071-RESPONSE.md`

Must include all 8 sections (see BOOT.md).

---

## Success Criteria

- [ ] All 7 annotation node types show resize handles when selected
- [ ] Dragging resize handles changes node dimensions
- [ ] Resized dimensions persist in node data (width/height fields)
- [ ] Process flow nodes (start, end, task, decision, etc.) remain fixed-size
- [ ] All CSS uses `var(--sd-*)` variables only
- [ ] At least 5 tests pass
- [ ] Build passes (no TypeScript errors)

---

## Notes

- NodeData interface already has `width?: number` and `height?: number` fields — no schema changes needed
- All annotation nodes already use `data.width` and `data.height` in their inline styles — just need to ensure ReactFlow updates persist to data
- Selection visual feedback already exists (CSS class `selected` applied when node selected)
- This is a pure frontend change — no backend, no bus events, no IR changes

---

**Q33N: Read the 7 annotation node files, write a task file for a bee (Haiku), return for Q33NR review before dispatch.**
