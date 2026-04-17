# BUG-023: Canvas components panel does not collapse to icon-only mode per spec

## Objective
Fix the Canvas components/palette panel so it collapses to icon-only mode when the pane is narrow, as specified in the canvas EGG design.

## Context
The components panel should collapse to show only icons (no text labels) when the pane width is below a threshold. Currently it stays in full-text mode regardless of width.

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`
- `browser/src/primitives/tree-browser/`
- `browser/sets/canvas.egg.md`

## Deliverables
- [ ] Add collapse behavior to palette panel based on pane width
- [ ] Icon-only mode shows just icons without text labels
- [ ] Smooth transition between collapsed and expanded modes
- [ ] Tests for collapse behavior at width thresholds

## Acceptance Criteria
- [ ] Panel collapses to icon-only when pane is narrow
- [ ] Panel expands to icon+text when pane is wide
- [ ] Transition is smooth (CSS transition)
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Depends On
- BUG022 (icons must exist before collapse can show icon-only mode)

## Model Assignment
haiku

## Priority
P0
