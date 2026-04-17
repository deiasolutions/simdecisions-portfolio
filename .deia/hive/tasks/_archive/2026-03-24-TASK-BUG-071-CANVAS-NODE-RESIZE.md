# TASK-BUG-071: Add Node Resize Capability to Canvas Annotation Nodes

## Objective

Add ReactFlow `NodeResizer` component to all 7 annotation node types (annotation-rect, annotation-ellipse, annotation-image, annotation-line, annotation-text, sticky-note, callout) to enable visual resize handles when nodes are selected. Process flow nodes remain fixed-size.

## Context

The canvas primitive uses ReactFlow and currently supports 22 node types:
- 9 core PHASE-IR types (start, end, task, decision, checkpoint, split, join, queue, group)
- 6 BPMN types (bpmn-start, bpmn-end, bpmn-task, bpmn-gateway, bpmn-subprocess, bpmn-event)
- 7 annotation types (annotation-ellipse, annotation-image, annotation-line, annotation-rect, annotation-text, sticky-note, callout)

**Current behavior:**
- Nodes can be placed via drag-drop from palette
- Node selection already works (ReactFlow built-in)
- Selection publishes `canvas:node-selected` bus events
- Visual selection feedback exists (CSS class `selected` applied)
- Resize handles DO NOT exist on any nodes

**What changes:**
- Add `NodeResizer` from `@xyflow/react` to 7 annotation node types ONLY
- ReactFlow automatically updates node dimensions when resize handles are dragged
- All annotation nodes already read `data.width` and `data.height` from NodeData interface
- Style resize handles using `var(--sd-*)` variables (Rule 3)

**ReactFlow NodeResizer API:**
```tsx
import { NodeResizer } from '@xyflow/react';

<NodeResizer
  minWidth={60}
  minHeight={40}
  color="var(--sd-primary)"
  handleStyle={{ borderRadius: 2 }}
  lineStyle={{ borderWidth: 1 }}
/>
```

The `NodeResizer` component:
- Automatically shows when parent node is selected
- Updates ReactFlow node dimensions on drag
- ReactFlow stores updated dimensions in node state
- Node component receives updated dimensions via props

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\AnnotationRectNode.tsx` (47 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\AnnotationEllipseNode.tsx` (46 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\AnnotationImageNode.tsx` (63 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\CalloutNode.tsx` (50 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\StickyNoteNode.tsx` (50 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\AnnotationLineNode.tsx` (53 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\AnnotationTextNode.tsx` (38 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvasTypes.ts` (86 lines, NodeData interface)

## Deliverables

### 1. Add NodeResizer to 7 Annotation Node Types

For each of the 7 annotation node types:
- [ ] Import `NodeResizer` from `@xyflow/react`
- [ ] Add `<NodeResizer />` component as a child of the root div
- [ ] Set minimum dimensions: `minWidth={60}` and `minHeight={40}` (or appropriate for node type)
- [ ] Configure color: `color="var(--sd-primary)"`
- [ ] Style handles using props (no inline hex/rgb colors)

**Specific node requirements:**
- **AnnotationRectNode**: minWidth={60}, minHeight={40}
- **AnnotationEllipseNode**: minWidth={60}, minHeight={40}
- **AnnotationImageNode**: minWidth={80}, minHeight={60}
- **AnnotationLineNode**: minWidth={40}, minHeight={2} (horizontal line)
- **AnnotationTextNode**: minWidth={60}, minHeight={20}
- **StickyNoteNode**: minWidth={100}, minHeight={80}
- **CalloutNode**: minWidth={80}, minHeight={40}

### 2. Verify Dimension Persistence

Each annotation node already uses `data.width` and `data.height` in inline styles:
- [ ] Verify AnnotationRectNode uses `width: d.width || 120`
- [ ] Verify AnnotationEllipseNode uses `width: d.width || 100`
- [ ] Verify AnnotationImageNode uses `width` and `height` from data
- [ ] Verify AnnotationLineNode uses `width: data?.width || 100`
- [ ] Verify AnnotationTextNode uses minWidth (no fixed width)
- [ ] Verify StickyNoteNode uses fixed width (140) but can be overridden
- [ ] Verify CalloutNode uses minWidth/maxWidth

**Note:** ReactFlow automatically updates node dimensions. These existing data fields ensure dimensions persist in node data.

### 3. CSS Styling for Resize Handles

Add styles to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css`:

```css
/* NodeResizer handles — all colors via CSS variables (Rule 3) */
.react-flow__resize-control {
  border: 1px solid var(--sd-primary);
  background: var(--sd-surface);
}

.react-flow__resize-control:hover {
  background: var(--sd-primary-dim);
  border-color: var(--sd-primary-bright);
}

.react-flow__resize-control-line {
  border-color: var(--sd-primary);
}
```

**Requirements:**
- [ ] All colors use `var(--sd-*)` variables (Rule 3)
- [ ] No hex, rgb(), or named colors
- [ ] Style both handle and line elements
- [ ] Include hover states

### 4. Do NOT Add Resize to Process Flow Nodes

Process flow nodes (start, end, task, decision, checkpoint, split, join, queue, group) and BPMN nodes must remain fixed-size:
- [ ] Do NOT modify StartNode.tsx
- [ ] Do NOT modify EndNode.tsx
- [ ] Do NOT modify TaskNode.tsx
- [ ] Do NOT modify DecisionNode.tsx
- [ ] Do NOT modify CheckpointNode.tsx
- [ ] Do NOT modify SplitNode.tsx
- [ ] Do NOT modify JoinNode.tsx
- [ ] Do NOT modify QueueNode.tsx
- [ ] Do NOT modify GroupNode.tsx
- [ ] Do NOT modify any BPMN node files

## Test Requirements

Write tests FIRST (TDD, Rule 5). Create test file:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-node-resize.test.tsx`

Minimum 5 tests:

### Test 1: Annotation Nodes Show NodeResizer When Selected
```typescript
it('renders NodeResizer for selected annotation-rect node', () => {
  const node = {
    id: 'test-1',
    type: 'annotation-rect',
    position: { x: 100, y: 100 },
    data: { label: 'Test', width: 120, height: 80 }
  };
  // Render AnnotationRectNode with selected=true
  // Assert NodeResizer is present in DOM
});
```

### Test 2: Process Flow Nodes Do NOT Show NodeResizer
```typescript
it('does not render NodeResizer for process flow nodes', () => {
  const node = {
    id: 'test-2',
    type: 'task',
    position: { x: 100, y: 100 },
    data: { label: 'Task' }
  };
  // Render TaskNode with selected=true
  // Assert NodeResizer is NOT present in DOM
});
```

### Test 3: NodeResizer Uses CSS Variables (No Hardcoded Colors)
```typescript
it('NodeResizer color prop uses CSS variable', () => {
  const node = {
    id: 'test-3',
    type: 'annotation-ellipse',
    position: { x: 100, y: 100 },
    data: { width: 100, height: 80 }
  };
  // Render AnnotationEllipseNode with selected=true
  // Assert NodeResizer color prop is 'var(--sd-primary)'
});
```

### Test 4: All 7 Annotation Node Types Have NodeResizer
```typescript
it('renders NodeResizer for all 7 annotation node types', () => {
  const types: CanvasNodeType[] = [
    'annotation-rect', 'annotation-ellipse', 'annotation-image',
    'annotation-line', 'annotation-text', 'sticky-note', 'callout'
  ];
  types.forEach(type => {
    // Render each node type with selected=true
    // Assert NodeResizer is present
  });
});
```

### Test 5: Minimum Dimensions Configured Correctly
```typescript
it('sets correct minimum dimensions for each node type', () => {
  // annotation-rect: minWidth=60, minHeight=40
  // annotation-ellipse: minWidth=60, minHeight=40
  // annotation-image: minWidth=80, minHeight=60
  // annotation-line: minWidth=40, minHeight=2
  // annotation-text: minWidth=60, minHeight=20
  // sticky-note: minWidth=100, minHeight=80
  // callout: minWidth=80, minHeight=40
  // Render each node, assert NodeResizer props
});
```

**Additional test coverage:**
- Test that NodeResizer is NOT rendered when node is NOT selected
- Test that existing node dimensions (data.width, data.height) are preserved

## Constraints

- **Rule 3:** All CSS uses `var(--sd-*)` variables only. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. All modified files are under 100 lines — this is satisfied.
- **Rule 5:** TDD. Write tests first, then implementation.
- **Rule 6:** No stubs. Every function fully implemented.

## Acceptance Criteria

- [ ] All 7 annotation node types render `<NodeResizer />` component
- [ ] NodeResizer only appears when node is selected
- [ ] NodeResizer configured with minimum dimensions for each node type
- [ ] Process flow nodes (start, end, task, etc.) do NOT have NodeResizer
- [ ] BPMN nodes do NOT have NodeResizer
- [ ] CSS styles use `var(--sd-*)` variables only (Rule 3)
- [ ] At least 5 tests pass
- [ ] All tests pass (frontend test suite)
- [ ] Build passes (no TypeScript errors)
- [ ] No file exceeds 500 lines (Rule 4)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-071-RESPONSE.md`

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

## Build Verification Commands

After implementation, run these commands:

```bash
# Frontend tests (from repo root)
cd browser && npx vitest run src/primitives/canvas/__tests__/canvas-node-resize.test.tsx

# Full frontend test suite
cd browser && npx vitest run

# Type check
cd browser && npx tsc --noEmit
```

Expected output:
- At least 5 tests pass in `canvas-node-resize.test.tsx`
- No new test failures in existing canvas tests
- No TypeScript errors

## Notes

- NodeData interface already has `width?: number` and `height?: number` fields (line 69-70 of canvasTypes.ts) — no type changes needed
- All annotation nodes already read dimensions from data — no inline style changes needed
- ReactFlow handles resize state automatically — no manual event handlers required
- This is a pure frontend change — no backend, no bus events, no IR routing
- CalloutNode has a nested structure (callout-body div) — add NodeResizer to root div, not callout-body
- StickyNoteNode has fixed width (140) but should still support resize — NodeResizer will override inline styles

## Success Criteria

✅ User can select an annotation node and see resize handles
✅ User can drag resize handles to change node dimensions
✅ Resized dimensions persist in node data
✅ Process flow nodes remain fixed-size (no resize handles)
✅ All colors use CSS variables (Rule 3)
✅ Tests pass
✅ Build passes
