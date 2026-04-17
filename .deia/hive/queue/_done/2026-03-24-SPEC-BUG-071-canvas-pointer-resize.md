# SPEC-BUG-071: Canvas Pointer/Select Tool and Node Resize

## Priority
P1

## Objective
Add a pointer/select tool to the canvas2 primitive and enable resize handles on annotation nodes (shapes, images, callouts, sticky notes). Currently users can drag-drop nodes onto the canvas and move/connect them, but cannot select individual nodes for editing or resize them after placement.

## Files to Read First
- browser/src/primitives/canvas/CanvasApp.tsx
- browser/src/primitives/canvas/canvasTypes.ts
- browser/src/primitives/canvas/nodes/AnnotationRectNode.tsx
- browser/src/primitives/canvas/nodes/AnnotationImageNode.tsx
- browser/src/primitives/canvas/nodes/AnnotationEllipseNode.tsx
- browser/src/primitives/canvas/nodes/CalloutNode.tsx
- browser/src/primitives/canvas/nodes/StickyNoteNode.tsx

## Deliverables
1. Add `NodeResizer` from `@xyflow/react` to all annotation node types (rect, ellipse, image, line, text, sticky-note, callout) so they can be resized when selected
2. Ensure node selection visual feedback (border highlight or handles visible) on click
3. Store updated width/height in node data after resize so dimensions persist
4. Add resize CSS styles to canvas.css using only `var(--sd-*)` tokens
5. Tests: at least 5 tests covering node selection, resize handle visibility, and dimension persistence

## Acceptance Criteria
- [ ] Clicking a node selects it with visible selection indicator
- [ ] Selected annotation nodes show resize handles on corners/edges
- [ ] Dragging resize handles changes node dimensions
- [ ] Resized dimensions persist in node data (width/height fields in NodeData)
- [ ] Process flow nodes (start, end, task, decision, etc.) remain fixed-size
- [ ] All new CSS uses var(--sd-*) variables only
- [ ] Tests pass: node selection, resize handles, dimension update

## Response File
20260324-TASK-BUG-071-RESPONSE.md
