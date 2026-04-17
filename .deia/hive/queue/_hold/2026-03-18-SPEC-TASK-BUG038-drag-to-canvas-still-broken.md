# SPEC: BUG-038 — Drag from palette to canvas still not working

## Priority: P0

## Problem
Dragging a component from the palette tree-view onto the canvas does not add the component. BUG-019 claimed to fix this by adding `stopPropagation()` to CanvasApp's drag handlers, but the feature still does not work in the browser.

## Context
- BUG-019 bee added `stopPropagation()` to onDragOver and onDrop in CanvasApp.tsx (lines 418, 424)
- The bee reported 5 tests passing for drag-drop isolation
- Despite this, dragging from palette to canvas does NOT work at runtime
- The fix may be incomplete, or a different recent change may have broken the drag source side (palette adapter, TreeNodeRow drag handlers)

## Investigation Required
1. Trace the FULL drag-drop flow end to end:
   - **Drag source:** paletteAdapter.ts sets up draggable nodes with dragMimeType and dragData in meta
   - **TreeNodeRow.tsx:** handleDragStart reads meta.dragMimeType and meta.dragData, calls e.dataTransfer.setData()
   - **CanvasApp.tsx:** onDragOver calls preventDefault (to allow drop), onDrop reads dataTransfer and creates node
2. Check if TreeNodeRow's handleDragStart is actually firing (the recent isTextIcon/BUG-035 changes touched this file)
3. Check if paletteAdapter still sets draggable: true and the correct meta fields on nodes
4. Check if CanvasApp's onDrop handler correctly reads the MIME type and creates the node
5. Check git diff for ALL recent changes to these files — something may have removed or broken the drag wiring

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-019-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG-035-RESPONSE.md`

## CRITICAL
- Trace the full flow, don't assume the stopPropagation fix was sufficient
- Check BOTH ends: drag source (palette/TreeNodeRow) AND drop target (CanvasApp)
- Recent changes to TreeNodeRow (BUG-035 isTextIcon fix) may have inadvertently broken drag

## Test Requirements
- Test full drag-drop flow: palette item → dataTransfer → canvas drop → node created
- Test TreeNodeRow sets correct dataTransfer data for draggable palette items
- Test CanvasApp onDrop creates node from dataTransfer
- All existing tests still pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD

## Model: sonnet
