# TASK-BUG-019-A: Palette and TreeNode Canvas Internal Marker

## Objective
Add `canvasInternal: true` marker to paletteAdapter nodes and propagate it as `canvas/internal` dataTransfer type in TreeNodeRow to isolate canvas drags from shell drag-drop system.

## Context
Canvas palette drags are currently intercepted by the Shell's drag-drop system instead of being isolated to the canvas pane. This is because:
1. Palette nodes don't set the `canvasInternal: true` marker in their metadata
2. TreeNodeRow doesn't check for this marker and set the `canvas/internal` dataTransfer type
3. The shell can't distinguish between canvas-internal drags and shell pane rearrangement drags

The fix requires two changes:
- paletteAdapter: Add `canvasInternal: true` to the meta object in `itemToNode()`
- TreeNodeRow: Check for `canvasInternal` in `handleDragStart()` and set `canvas/internal` dataTransfer type

**IMPORTANT:** The drag MIME type is `application/phase-node` (NOT `application/sd-node-type`). Keep existing MIME type.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts

## Deliverables
- [ ] paletteAdapter.ts: Add `canvasInternal: true` to meta object in `itemToNode()` function (line 64-68)
- [ ] TreeNodeRow.tsx: Update `handleDragStart()` to check `node.meta.canvasInternal` (after line 56)
- [ ] TreeNodeRow.tsx: If `canvasInternal` is true, set `e.dataTransfer.setData('canvas/internal', 'true')`
- [ ] TreeNodeRow.tsx: Call `e.stopPropagation()` for canvas-internal drags
- [ ] Test file created: `browser/src/primitives/tree-browser/__tests__/paletteAdapter.test.ts` (minimum 3 tests)
- [ ] Test file created: `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.canvasInternal.test.tsx` (minimum 4 tests)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Palette node has canvasInternal marker
  - TreeNodeRow sets canvas/internal dataTransfer type for palette nodes
  - TreeNodeRow calls stopPropagation for canvas-internal drags
  - Non-canvas adapters (explorer, files, properties) do NOT get canvasInternal marker
  - Shell pane rearrangement drags (hhs/node-id) are NOT affected

### Test Coverage Requirements

**paletteAdapter.test.ts** (minimum 3 tests):
1. Verify `itemToNode()` returns node with `canvasInternal: true` in meta
2. Verify drag MIME type is `application/phase-node` (not `application/sd-node-type`)
3. Verify all palette categories (Flow Control, Process, Layout) get canvasInternal marker

**TreeNodeRow.canvasInternal.test.tsx** (minimum 4 tests):
1. Verify `handleDragStart()` sets `canvas/internal` dataTransfer type when `node.meta.canvasInternal` is true
2. Verify `handleDragStart()` calls `stopPropagation()` for canvas-internal drags
3. Verify `handleDragStart()` does NOT set `canvas/internal` when `canvasInternal` is false/undefined
4. Verify drag event contains both `application/phase-node` and `canvas/internal` types

## Implementation Details

### paletteAdapter.ts changes

In `itemToNode()` function (starting at line 58), update the meta object:

```typescript
function itemToNode(item: PhaseNodeDragData & { icon: string }): TreeNodeData {
  return {
    id: `palette-node-${item.kind}`,
    label: item.label,
    icon: item.icon,
    draggable: true,
    meta: {
      description: item.description,
      dragMimeType: 'application/phase-node',
      dragData: { kind: item.kind, label: item.label, description: item.description, defaultData: item.defaultData },
      canvasInternal: true,  // ADD THIS LINE
    },
  }
}
```

### TreeNodeRow.tsx changes

In `handleDragStart()` function (starting at line 56), after setting dragMimeType data (line 65):

```typescript
const handleDragStart = (e: React.DragEvent) => {
  if (node.disabled || !node.draggable) return;

  // Set dataTransfer if node has drag metadata
  if (node.meta) {
    const dragMimeType = node.meta.dragMimeType as string | undefined;
    const dragData = node.meta.dragData;

    if (dragMimeType && dragData) {
      e.dataTransfer.setData(dragMimeType, JSON.stringify(dragData));
      e.dataTransfer.effectAllowed = 'copy';
    }

    // ADD THIS BLOCK:
    // If this is a canvas-internal drag, mark it to prevent shell interception
    const canvasInternal = node.meta.canvasInternal as boolean | undefined;
    if (canvasInternal) {
      e.dataTransfer.setData('canvas/internal', 'true');
      e.stopPropagation();
    }
  }

  onDragStart?.(node.id, node);
};
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs — fully implement all functions
- TDD: write tests FIRST, then implementation
- Do NOT change the drag MIME type from `application/phase-node`
- Do NOT break existing drag-drop for non-canvas adapters

## Acceptance Criteria
- [ ] paletteAdapter.ts sets `canvasInternal: true` in node metadata
- [ ] TreeNodeRow.tsx checks `node.meta.canvasInternal` in `handleDragStart()`
- [ ] TreeNodeRow.tsx sets `dataTransfer.setData('canvas/internal', 'true')` when canvasInternal is true
- [ ] TreeNodeRow.tsx calls `e.stopPropagation()` for canvas-internal drags
- [ ] Drag MIME type remains `application/phase-node` (unchanged)
- [ ] paletteAdapter.test.ts: 3+ tests passing
- [ ] TreeNodeRow.canvasInternal.test.tsx: 4+ tests passing
- [ ] All existing tree-browser tests still pass
- [ ] Non-canvas adapters (explorer, files, properties) do NOT get canvasInternal marker

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-BUG-019-A-RESPONSE.md`

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
