# TASK-BUG-022-B: Click to Place on Canvas

## Objective
Clicking a palette node places it on the canvas at viewport center. Implements the spec requirement: "Clicking a component places it on canvas or starts drag."

## Context

**Current state:** Palette nodes are draggable (`draggable: true`). Drag handlers work (TreeNodeRow lines 46-61). User must manually drag to canvas.

**Spec requirement:** "Clicking a component places it on canvas or starts drag."

**Chosen interpretation:** Click-to-place at canvas viewport center. This is the simplest interpretation of the spec. If Q88N wants click-to-drag mode instead (cursor changes to "placing" mode), he will say so after reviewing this implementation.

**Architecture:** Palette nodes live in TreeBrowser (left sidebar). Canvas lives in CanvasApp (center pane). They communicate via MessageBus. When a palette node is clicked, publish a bus message with the nodeType. CanvasApp subscribes and creates the node.

**Bus event design:**
- Event type: `palette:node-click`
- Payload: `{ nodeType: string, paneId?: string }`
- Publisher: TreeNodeRow (when palette node clicked) OR TreeBrowser (via onSelect handler)
- Subscriber: CanvasApp

**Node placement:** Place at canvas viewport center. ReactFlow provides `project()` to convert screen coords to canvas coords. Use viewport center for initial placement.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (114 lines — add click handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (161 lines — review onSelect flow)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (527 lines — add bus subscriber)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (bus message types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (lines 244-250 — check bus permissions)

## Deliverables
- [ ] Bus message type defined: `palette:node-click` in `messages.ts`
- [ ] TreeNodeRow publishes `palette:node-click` when palette node clicked (check `node.meta.nodeType` exists)
- [ ] CanvasApp subscribes to `palette:node-click` and creates node at viewport center
- [ ] Node creation uses ReactFlow `project()` to convert viewport center to canvas coords
- [ ] Node ID generation: `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
- [ ] Node type mapping: `palette:node-click` payload `nodeType` → CanvasApp ReactFlow node type (lowercase)
- [ ] Edge case: no canvas active → message ignored (no crash)

## Test Requirements
- [ ] **TDD:** Tests written FIRST before modifying TreeNodeRow and CanvasApp
- [ ] **Unit test 1:** TreeNodeRow with palette node publishes `palette:node-click` on click (mock bus)
- [ ] **Unit test 2:** TreeNodeRow with non-palette node does NOT publish `palette:node-click`
- [ ] **Unit test 3:** CanvasApp receives `palette:node-click` → creates node at viewport center
- [ ] **Integration test:** Full flow — palette node clicked → bus message → canvas node created (verify node in canvas state)
- [ ] **Edge case test:** `palette:node-click` published when canvas not mounted → no crash, message ignored
- [ ] All tests pass

## Constraints
- No file over 500 lines (CanvasApp is 527 lines — already over limit, do NOT make it worse; add minimal lines)
- CSS: `var(--sd-*)` only (no CSS changes required)
- No stubs — full implementation of click-to-place logic
- Bus message must be added to `canvas.egg.md` permissions if not already present

## Implementation Guidance

### Bus Message Type (messages.ts)
```typescript
export interface PaletteNodeClickMessage {
  type: 'palette:node-click';
  nodeType: string;
  paneId?: string;
}
```

### TreeNodeRow Click Handler
```typescript
const handleClick = (e: React.MouseEvent) => {
  if (node.disabled) return;
  // Don't trigger select if clicking chevron
  if ((e.target as HTMLElement).closest('.tree-node-chevron')) return;

  // Publish palette click if this is a palette node
  if (node.meta?.nodeType && bus) {
    bus.publish({
      type: 'palette:node-click',
      nodeType: node.meta.nodeType as string,
    });
  }

  onSelect(node.id, node);
};
```

**Note:** TreeNodeRow does NOT have access to bus directly. Options:
1. Pass bus via TreeBrowser → TreeNodeRow props (requires prop drilling)
2. Call onSelect, then TreeBrowser publishes the message (cleaner)
3. Add bus to TreeBrowserProps, pass down to TreeNodeRow

**Recommended:** Option 2 — TreeBrowser handles the publish in its onSelect wrapper.

### CanvasApp Subscriber
```typescript
useEffect(() => {
  if (!bus) return;

  const unsub = bus.subscribe('palette:node-click', (msg) => {
    const nodeType = msg.nodeType?.toLowerCase(); // Map "Task" → "task"
    const id = `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    // Get viewport center
    const { x: vx, y: vy } = getViewport();
    const center = project({ x: window.innerWidth / 2, y: window.innerHeight / 2 });

    const newNode: Node = {
      id,
      type: nodeType,
      position: center,
      data: { label: msg.nodeType },
    };

    setNodes((nds) => [...nds, newNode]);
  });

  return unsub;
}, [bus, setNodes, project, getViewport]);
```

## Acceptance Criteria
- [ ] Clicking a palette component places it on canvas at viewport center
- [ ] Bus event `palette:node-click` defined in `messages.ts`
- [ ] TreeBrowser or TreeNodeRow publishes `palette:node-click` when palette node clicked
- [ ] CanvasApp subscribes to `palette:node-click` and creates node
- [ ] Node placement uses ReactFlow `project()` for correct canvas coords
- [ ] Tests pass: minimum 5 tests (2 unit TreeNodeRow + 1 unit CanvasApp + 1 integration + 1 edge case)
- [ ] No hardcoded colors introduced
- [ ] No stubs shipped
- [ ] CanvasApp does NOT exceed 600 lines (current: 527, add minimal lines only)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-BUG-022-B-RESPONSE.md`

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
