# BUG-021: Canvas minimap white visible zone on dark bg, outline misaligned

## Objective
Fix the Canvas minimap so the visible zone indicator uses theme-appropriate colors (not white on dark background) and the corner outline aligns correctly.

## Context
The Canvas minimap shows a white visible-zone rectangle that clashes with the dark theme background. The outline at corners is misaligned. All colors must use CSS variables.

## Files to Read First
- `browser/src/primitives/canvas/`
- `browser/src/primitives/canvas/bpmn-styles.css`
- `browser/src/shell/shell-themes.css`

## Deliverables
- [ ] Replace hardcoded white/colors in minimap visible zone with CSS variables
- [ ] Fix corner outline alignment
- [ ] Visible zone readable on both light and dark themes
- [ ] Tests for minimap CSS variable usage

## Acceptance Criteria
- [ ] Minimap visible zone uses var(--sd-*) colors, no hardcoded values
- [ ] Outline aligns at corners
- [ ] Looks correct on dark theme
- [ ] Looks correct on light theme
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/canvas/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only — NO hex, NO rgb(), NO named colors
- No stubs

## Model Assignment
haiku

## Priority
P0
