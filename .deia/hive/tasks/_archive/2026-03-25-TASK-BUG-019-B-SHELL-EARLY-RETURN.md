# TASK-BUG-019-B: Shell Early Return for Canvas Internal Drags

## Objective
Add early return logic to ShellNodeRenderer's `onDragOver` and `onDrop` handlers to ignore drags with `canvas/internal` dataTransfer type, preventing Shell from intercepting canvas-internal drags.

## Context
The Shell's drag-drop system currently intercepts ALL drags, including canvas-internal drags from the palette. After TASK-BUG-019-A, palette nodes will set a `canvas/internal` dataTransfer marker. This task makes ShellNodeRenderer check for that marker and return early, allowing canvas-internal drags to pass through to the canvas without Shell interception.

The shell must still accept `hhs/node-id` drags for pane rearrangement. This task ONLY adds a filter for `canvas/internal` drags.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts

## Deliverables
- [ ] ShellNodeRenderer.tsx: Add early return in `onDragOver` handler (after line 160) to check for `canvas/internal` marker
- [ ] ShellNodeRenderer.tsx: Add early return in `onDrop` handler (after line 176) to check for `canvas/internal` marker
- [ ] Test file created: `browser/src/shell/components/__tests__/ShellNodeRenderer.canvasDrag.test.tsx` (minimum 5 tests)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - onDragOver returns early when `canvas/internal` is in dataTransfer.types
  - onDrop returns early when `canvas/internal` is in dataTransfer.types
  - onDragOver still processes `hhs/node-id` drags (shell pane rearrangement)
  - onDrop still processes `hhs/node-id` drags (shell pane rearrangement)
  - Multiple dataTransfer types: both `hhs/node-id` and `canvas/internal` present → canvas wins

### Test Coverage Requirements

**ShellNodeRenderer.canvasDrag.test.tsx** (minimum 5 tests):
1. Verify `onDragOver` returns early when `canvas/internal` is present in dataTransfer.types
2. Verify `onDrop` returns early when `canvas/internal` is present in dataTransfer.types
3. Verify `onDragOver` still processes `hhs/node-id` drags (shell pane rearrangement)
4. Verify `onDrop` still processes `hhs/node-id` drags (shell pane rearrangement)
5. Verify when both `hhs/node-id` and `canvas/internal` are present, canvas/internal takes precedence (early return)

## Implementation Details

### ShellNodeRenderer.tsx changes

In `onDragOver` function (starting at line 160), add early return at the top:

```typescript
const onDragOver = (e: React.DragEvent) => {
  if (node.type === 'app' && (node as AppNode).chrome === false) return;

  // ADD THIS BLOCK:
  // Ignore canvas-internal drags — they are isolated to canvas pane
  if (hasType(e.dataTransfer.types, 'canvas/internal')) return;

  // Only intercept shell pane-swap drags (hhs/node-id) or bus-based drags,
  // NOT palette/canvas drags (application/sd-node-type) which must pass through
  const isShellDrag = hasType(e.dataTransfer.types, 'hhs/node-id');
  if (!isShellDrag && !isDragActive) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  if (!ref.current) return;
  setDropZone(getDropZone(ref.current.getBoundingClientRect(), e.clientX, e.clientY));
  if (isShellDrag) {
    setCanAccept(true);
    setIsDragActive(true);
  }
};
```

In `onDrop` function (starting at line 176), add early return at the top:

```typescript
const onDrop = (e: React.DragEvent) => {
  if (node.type === 'app' && (node as AppNode).chrome === false) return;

  // ADD THIS BLOCK:
  // Ignore canvas-internal drags — they are isolated to canvas pane
  if (hasType(e.dataTransfer.types, 'canvas/internal')) return;

  const isShellDrag = hasType(e.dataTransfer.types, 'hhs/node-id');
  if (!isShellDrag && !(canAccept && isDragActive)) return;
  e.preventDefault();
  const sourceId = e.dataTransfer.getData('hhs/node-id');
  if (sourceId && dropZone) {
    const targetId = (node.type === 'app' || node.type === 'tabbed') ? node.id : null;
    if (targetId && sourceId !== targetId) {
      dispatch?.({ type: 'MOVE_APP', sourceId, targetId, zone: dropZone });
    }
  } else if (canAccept && isDragActive && dragPayload) {
    bus?.send({
      type: BUS_MESSAGE_TYPES.DROP_ACCEPT,
      fromPaneId: node.id,
      target: node.id,
      payload: { nodeId: node.id, ...dragPayload },
    });
  }
  setDropZone(null);
  setIsDragActive(false);
  setCanAccept(false);
  setDragPayload(null);
};
```

## Constraints
- No file over 500 lines (ShellNodeRenderer.tsx is 344 lines, well under limit)
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs — fully implement all functions
- TDD: write tests FIRST, then implementation
- Do NOT break shell pane rearrangement drags (hhs/node-id)
- Do NOT modify `onDragEnter` or `onDragLeave` handlers

## Acceptance Criteria
- [ ] ShellNodeRenderer.tsx `onDragOver` checks for `canvas/internal` marker and returns early
- [ ] ShellNodeRenderer.tsx `onDrop` checks for `canvas/internal` marker and returns early
- [ ] Shell still accepts `hhs/node-id` drags for pane rearrangement
- [ ] ShellNodeRenderer.canvasDrag.test.tsx: 5+ tests passing
- [ ] All existing shell tests still pass
- [ ] When both `hhs/node-id` and `canvas/internal` are present, `canvas/internal` takes precedence

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-BUG-019-B-RESPONSE.md`

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
