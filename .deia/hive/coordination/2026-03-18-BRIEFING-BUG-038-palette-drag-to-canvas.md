# BRIEFING: BUG-038 — Palette Drag-to-Canvas Not Working

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Priority:** P0
**Model Assignment:** Sonnet

---

## Objective

Fix the drag-and-drop flow so users can drag palette items (components) from the tree-browser onto the canvas to create nodes.

## Problem

Despite BUG-019 claiming to fix this, dragging from palette to canvas doesn't work at runtime. Investigation reveals:

1. **BUG-019's `stopPropagation()` fix was NEVER COMMITTED** — response said "uncommitted changes," but current CanvasApp.tsx (lines 417-423) does NOT contain stopPropagation() calls
2. **paletteAdapter doesn't set drag metadata** — it creates nodes with `draggable: true` but NEVER sets `meta.dragMimeType` or `meta.dragData`
3. **TreeNodeRow expects drag metadata** — handleDragStart (lines 99-110) reads `meta.dragMimeType` and `meta.dragData`, but paletteAdapter never provides them
4. **CanvasApp expects specific MIME type** — onDrop reads `'application/sd-node-type'` (line 423) but nothing sets this

## Root Causes

### Cause 1: Missing Drag Metadata in paletteAdapter
File: `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`

Current code (lines 50-61):
```typescript
function entryToNode(entry: PaletteEntry): TreeNodeData {
  return {
    id: `palette-node-${entry.nodeType.toLowerCase().replace(/\s+/g, '-')}`,
    label: entry.label,
    icon: entry.icon,
    draggable: true,
    meta: {
      nodeType: entry.nodeType,  // ❌ TreeNodeRow doesn't use this
      description: entry.description,
    },
  }
}
```

**Missing:** `dragMimeType` and `dragData` fields that TreeNodeRow expects.

### Cause 2: Missing stopPropagation in CanvasApp
File: `browser/src/primitives/canvas/CanvasApp.tsx`

Current code (lines 416-423):
```typescript
const onDragOver = useCallback((event: React.DragEvent) => {
  event.preventDefault();  // ❌ No stopPropagation
  event.dataTransfer.dropEffect = 'move';
}, []);

const onDrop = useCallback((event: React.DragEvent) => {
  event.preventDefault();  // ❌ No stopPropagation
  const type = event.dataTransfer.getData('application/sd-node-type') as CanvasNodeType;
  // ...
```

BUG-019's fix was never committed.

## Files to Fix

### Priority 1: paletteAdapter.ts
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`

**Required change:** Add `dragMimeType` and `dragData` to meta in `entryToNode()`:

```typescript
function entryToNode(entry: PaletteEntry): TreeNodeData {
  return {
    id: `palette-node-${entry.nodeType.toLowerCase().replace(/\s+/g, '-')}`,
    label: entry.label,
    icon: entry.icon,
    draggable: true,
    meta: {
      nodeType: entry.nodeType,
      description: entry.description,
      dragMimeType: 'application/sd-node-type',  // ← ADD THIS
      dragData: { nodeType: entry.nodeType },    // ← ADD THIS
    },
  }
}
```

### Priority 2: CanvasApp.tsx
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

**Required change:** Add `stopPropagation()` to both drag handlers (lines ~417, ~422):

```typescript
const onDragOver = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.stopPropagation(); // ← ADD THIS — prevents shell pane drag system
  event.dataTransfer.dropEffect = 'move';
}, []);

const onDrop = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.stopPropagation(); // ← ADD THIS — prevents shell pane drag system
  const type = event.dataTransfer.getData('application/sd-node-type') as CanvasNodeType;
  // ...
```

### Priority 3: Fix onDrop data reading
Current code reads `dragData.nodeType`, but we need to handle JSON parsing:

```typescript
const onDrop = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.stopPropagation();

  const rawData = event.dataTransfer.getData('application/sd-node-type');
  if (!rawData || !reactFlow) return;

  let nodeType: CanvasNodeType;
  try {
    const parsed = JSON.parse(rawData);
    nodeType = parsed.nodeType;
  } catch {
    // Fallback: treat rawData as plain string
    nodeType = rawData as CanvasNodeType;
  }

  if (!nodeType) return;

  // ... rest of onDrop logic
```

## Context Files

### Related Response Files
- `.deia/hive/responses/20260317-BUG-019-RESPONSE.md` — claimed fix, but changes never committed
- `.deia/hive/responses/20260318-TASK-BUG-035-RESPONSE.md` — recent TreeNodeRow changes (isTextIcon)

### Source Files (Read These)
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` (96 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (169 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 414-440)

### Test Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas.dragDrop.test.tsx` (BUG-019 created this, 5 tests)
- May need new integration test verifying full flow: paletteAdapter → TreeNodeRow → CanvasApp

## Acceptance Criteria

Q33N: write task files that ensure:

1. **AC1:** paletteAdapter sets `dragMimeType` and `dragData` in node meta
2. **AC2:** TreeNodeRow handleDragStart reads metadata and calls `setData()`
3. **AC3:** CanvasApp onDragOver and onDrop call `stopPropagation()`
4. **AC4:** CanvasApp onDrop correctly parses JSON dragData
5. **AC5:** Dragging palette item to canvas creates a node at drop position
6. **AC6:** All existing tests still pass
7. **AC7:** New integration test verifies full drag flow end-to-end

## Test Requirements

- TDD: Tests first, then fixes
- Test the FULL flow: palette metadata → dataTransfer → canvas receives → node created
- Test that palette nodes have correct dragMimeType/dragData
- Test that TreeNodeRow sets dataTransfer correctly
- Test that CanvasApp reads dataTransfer and creates node
- Test that stopPropagation prevents shell interference
- All existing canvas/tree-browser tests must pass

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD

## Dispatch Instructions for Q33N

1. Read all 3 source files listed above
2. Read BUG-019 response to understand what was attempted
3. Write task file(s) for bees (likely 1-2 tasks: one for paletteAdapter fix, one for CanvasApp fix)
4. Include full context in task files: what the drag flow is, what's missing, what to add
5. Return task files to Q33NR for review BEFORE dispatching bees
6. After Q33NR approval, dispatch bees (Haiku or Sonnet)

## Notes

- This is a P0 blocker — users cannot add components to canvas
- BUG-019 bee thought it fixed this but only fixed part of the problem (and didn't commit)
- The real issue is paletteAdapter not setting up drag metadata
- TreeNodeRow code is correct (reads meta fields), just nothing provides them

---

**End of Briefing**
