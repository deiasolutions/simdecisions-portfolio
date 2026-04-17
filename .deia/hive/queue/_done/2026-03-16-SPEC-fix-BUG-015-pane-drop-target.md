# SPEC: Fix BUG-015 — Cannot drag pane into open pane in Stage

## Priority
P0

## Bug
BUG-015: Dragging a pane into another open pane in the Stage does not work. Drop target not recognized or drop handler not firing.

## Objective
Investigate and fix the pane-into-pane drag-and-drop in the shell. The user should be able to drag one pane and drop it into an existing open pane to create a split or replace content.

## Context
This is the first real UAT of pane composition in the Stage runtime. The drag/drop infrastructure exists in the shell reducer and PaneChrome components but may not be fully wired or may have been broken during recent ports.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (drag/drop handlers on pane chrome)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (renders split/pane tree, may have drop zones)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (shell state reducer — MOVE_PANE, SPLIT_PANE actions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (shell state types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` (EGG layout → shell state)

## Investigation Steps
1. Check if PaneChrome has onDragOver + onDrop handlers
2. Check if drop events set correct dataTransfer MIME types
3. Check if reducer handles MOVE_PANE or equivalent action
4. Check if drop zones render correctly (visual feedback on dragover)
5. Check browser console for errors during drag/drop

## Acceptance Criteria
- [ ] User can drag a pane tab/chrome and drop it onto another open pane
- [ ] Drop creates a split (left/right or top/bottom) or replaces pane content
- [ ] Visual drop zone indicator appears on dragover
- [ ] Existing pane tests still pass
- [ ] New tests cover drag-drop pane composition

## Model Assignment
sonnet

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD
