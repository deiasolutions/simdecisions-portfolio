# BUG-022: Canvas components panel shows plain list, no icons, click does nothing

## Objective
Fix the Canvas components/palette panel so it shows icons for each component type and clicking a component initiates drag-to-canvas or click-to-place behavior.

## Context
The components panel (driven by paletteAdapter) currently shows a plain text list with no icons. Clicking items does nothing. The adapter needs to provide icon data and wire click/drag handlers.

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`
- `browser/src/primitives/tree-browser/`
- `browser/src/primitives/canvas/`
- `eggs/canvas.egg.md`

## Deliverables
- [ ] Add icons to palette adapter component entries
- [ ] Wire click handler to place component on canvas (or initiate drag)
- [ ] Components panel shows visual icons per component type
- [ ] Tests for palette adapter icon data and click handling

## Acceptance Criteria
- [ ] Components panel shows icons next to each component name
- [ ] Clicking a component places it on canvas or starts drag
- [ ] All component types have appropriate icons
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
