# BL-121: Port Properties Panel editing UI

## Objective
Port the Properties Panel editing UI from the platform repo so canvas node properties can be viewed and edited in a dedicated pane.

## Context
The Canvas EGG has a properties pane that should show editable properties for the selected canvas node. The properties adapter and panel UI need to be ported from the platform repo and wired to the bus events.

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/`
- `browser/src/primitives/canvas/`
- `eggs/canvas.egg.md`
- Platform reference: check for properties panel components

## Deliverables
- [ ] Port or create properties panel component
- [ ] Wire to canvas node selection events (bus)
- [ ] Show editable fields for selected node properties
- [ ] Save changes back to canvas state
- [ ] Tests for property display and editing

## Acceptance Criteria
- [ ] Selecting a canvas node shows its properties in the panel
- [ ] Editing a property updates the canvas node
- [ ] Deselecting clears the panel
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet

## Priority
P0
