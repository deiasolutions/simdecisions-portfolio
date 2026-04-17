# BUG-019: Canvas component drag captured by Stage instead of dropping on canvas

## Objective
Fix drag behavior so dragging components from the Canvas palette drops them onto the canvas surface, not captured by the Stage shell's pane drag system.

## Context
When dragging a component from the Canvas components panel onto the canvas drawing surface, the Stage shell intercepts the drag event and tries to treat it as a pane swap/move instead. The canvas needs to capture drag events within its own surface before they bubble to the shell.

## Files to Read First
- `browser/src/primitives/canvas/`
- `browser/src/shell/components/ShellNodeRenderer.tsx`
- `browser/src/shell/dragDropUtils.ts`
- `eggs/canvas.egg.md`

## Deliverables
- [ ] Fix canvas to stopPropagation on internal drag events
- [ ] Ensure shell drag handlers ignore canvas-internal drags
- [ ] Components from palette drop correctly onto canvas surface
- [ ] Tests for canvas drag isolation from shell

## Acceptance Criteria
- [ ] Dragging palette component onto canvas creates a node, not a pane swap
- [ ] Shell pane drag still works outside canvas surface
- [ ] No event conflicts between canvas and shell drag systems
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/canvas/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
