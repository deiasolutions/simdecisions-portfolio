# Q33N Response: BUG-071 Canvas Node Resize Task File

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Regent)
**Date:** 2026-03-24
**Re:** BRIEFING-BUG-071-CANVAS-NODE-RESIZE

---

## Summary

I have read the briefing and reviewed all 7 annotation node files plus the canvasTypes.ts interface. I have written one task file for a Haiku bee to add NodeResizer components to all 7 annotation node types while keeping process flow nodes fixed-size.

**Task file created:**
- `.deia/hive/tasks/2026-03-24-TASK-BUG-071-CANVAS-NODE-RESIZE.md`

---

## Task File Details

### Scope
The task adds ReactFlow's `NodeResizer` component to exactly 7 annotation node types:
1. AnnotationRectNode
2. AnnotationEllipseNode
3. AnnotationImageNode
4. AnnotationLineNode
5. AnnotationTextNode
6. StickyNoteNode
7. CalloutNode

Process flow nodes (start, end, task, decision, checkpoint, split, join, queue, group) and BPMN nodes explicitly excluded — they remain fixed-size.

### Key Implementation Details

**1. NodeResizer integration:**
- Import `NodeResizer` from `@xyflow/react`
- Add as child component to root div in each annotation node
- Configure with `color="var(--sd-primary)"` (Rule 3)
- Set appropriate minimum dimensions per node type:
  - Rect/Ellipse: 60×40
  - Image: 80×60
  - Line: 40×2 (horizontal line special case)
  - Text: 60×20
  - Sticky: 100×80
  - Callout: 80×40

**2. Dimension persistence:**
- All annotation nodes already use `data.width` and `data.height` in inline styles
- NodeData interface already has `width?: number` and `height?: number` fields
- ReactFlow automatically updates dimensions when resize handles are dragged
- No additional state management required

**3. CSS styling:**
- Add styles to `browser/src/primitives/canvas/canvas.css`
- Style `.react-flow__resize-control` and `.react-flow__resize-control-line`
- All colors use `var(--sd-*)` variables (Rule 3)
- Include hover states for visual feedback

**4. Tests (TDD, minimum 5):**
- Test 1: NodeResizer renders for selected annotation nodes
- Test 2: NodeResizer does NOT render for process flow nodes
- Test 3: NodeResizer color uses CSS variable (no hardcoded colors)
- Test 4: All 7 annotation node types have NodeResizer
- Test 5: Minimum dimensions configured correctly per node type

Test file location: `browser/src/primitives/canvas/__tests__/canvas-node-resize.test.tsx`

### Files Modified (8 total)

1. `browser/src/primitives/canvas/nodes/AnnotationRectNode.tsx` — add NodeResizer
2. `browser/src/primitives/canvas/nodes/AnnotationEllipseNode.tsx` — add NodeResizer
3. `browser/src/primitives/canvas/nodes/AnnotationImageNode.tsx` — add NodeResizer
4. `browser/src/primitives/canvas/nodes/AnnotationLineNode.tsx` — add NodeResizer
5. `browser/src/primitives/canvas/nodes/AnnotationTextNode.tsx` — add NodeResizer
6. `browser/src/primitives/canvas/nodes/StickyNoteNode.tsx` — add NodeResizer
7. `browser/src/primitives/canvas/nodes/CalloutNode.tsx` — add NodeResizer
8. `browser/src/primitives/canvas/canvas.css` — add resize handle styles

Test file created: `browser/src/primitives/canvas/__tests__/canvas-node-resize.test.tsx`

### Constraints Verified

- **Rule 3:** All CSS uses `var(--sd-*)` variables only — CSS styles specified in task
- **Rule 4:** No file over 500 lines — all modified files under 100 lines
- **Rule 5:** TDD — 5 tests specified, must be written first
- **Rule 6:** No stubs — NodeResizer is a ReactFlow component, fully implemented by library

### Success Criteria

✅ All 7 annotation nodes get NodeResizer
✅ Process flow and BPMN nodes remain fixed-size
✅ Minimum dimensions set appropriately per node type
✅ CSS uses only `var(--sd-*)` variables
✅ At least 5 tests pass
✅ Build passes with no TypeScript errors

---

## Recommended Model

**Haiku** — This is a straightforward implementation task:
- Import one component from existing library
- Add to 7 files (simple JSX addition)
- Write 5 tests (standard ReactFlow component testing)
- Add CSS styles (3 rules, all using variables)
- No complex logic, no state management, no bus integration

Estimated effort: 30-40 minutes

---

## Dependencies

None. This is a self-contained frontend change:
- No backend changes
- No bus events
- No IR routing
- No schema changes (NodeData interface already has width/height fields)
- No dependency on other tasks

---

## Ready for Review

The task file is complete and ready for Q33NR review. Please check:

1. Are deliverables clear and specific?
2. Are test requirements adequate (5 tests minimum)?
3. Are constraints properly enforced (Rule 3: CSS variables)?
4. Are file paths absolute and correct?
5. Is the scope appropriate for a Haiku bee?
6. Are acceptance criteria measurable?

After review and approval, I will dispatch the Haiku bee via:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-BUG-071-CANVAS-NODE-RESIZE.md --model haiku --role bee --inject-boot
```

---

## Notes

- CalloutNode has a nested structure (callout-body div inside root div). Task specifies to add NodeResizer to root div, not nested div.
- StickyNoteNode has fixed width (140) in inline styles. NodeResizer will override this when user resizes, which is desired behavior.
- AnnotationLineNode is special (horizontal line, height: 2). Minimum dimensions adjusted accordingly (40×2).
- ReactFlow's NodeResizer automatically respects the `selected` prop — no manual show/hide logic needed.

**Awaiting Q33NR review and approval to dispatch.**
