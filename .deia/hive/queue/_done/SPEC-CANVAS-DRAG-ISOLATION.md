# SPEC-CANVAS-DRAG-ISOLATION

## Bugs
BUG-019, BUG-053

## Priority
P0

## Model
sonnet

## Summary
Dragging palette components to canvas is intercepted by Stage/Shell drop handlers. The canvas drop zone never receives the drop. Same bug affects SimDecisions palette drag.

## Existing Task File
READ THIS FIRST: `.deia/hive/tasks/2026-03-17-TASK-BUG-019-canvas-drag-isolation.md`
Contains complete specification with 10 tests, exact line numbers, and fix pseudocode.

## Key Files
- `browser/src/primitives/canvas/CanvasApp.tsx` — onDrop handler, needs `stopPropagation()`
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` — lines 46-61, drag start handler
- `browser/src/shell/components/ShellNodeRenderer.tsx` — lines 146-178, onDragOver/onDrop
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts` — palette node metadata

## Required Changes
1. Canvas `onDragOver` and `onDrop`: add `stopPropagation()` + `preventDefault()`
2. Palette adapter: add `canvasInternal: true` metadata to draggable nodes
3. TreeNodeRow `handleDragStart`: set `canvas/internal` data type in dataTransfer
4. ShellNodeRenderer: guard `onDragOver`/`onDrop` to ignore drags with `canvas/internal` type

## Tests Required
1. Palette drag sets `canvas/internal` dataTransfer type
2. Canvas onDrop calls stopPropagation
3. Shell drop handler ignores `canvas/internal` drags
4. End-to-end: drag palette item → drops on canvas, not shell

## Depends On
Nothing

## Acceptance Criteria
- [ ] Palette nodes can be dragged from tree-browser to canvas without Shell intercepting the drop
- [ ] Canvas `onDragOver` and `onDrop` handlers include `stopPropagation()` and `preventDefault()`
- [ ] Palette adapter adds `canvasInternal: true` metadata to draggable nodes
- [ ] TreeNodeRow `handleDragStart` sets `canvas/internal` data type in dataTransfer
- [ ] ShellNodeRenderer guards `onDragOver`/`onDrop` to ignore drags with `canvas/internal` type
- [ ] All 4 tests passing: palette drag sets marker, canvas stops propagation, shell ignores canvas drags, end-to-end drag works
- [ ] Existing shell pane rearrangement drag-drop still works (no regression)
