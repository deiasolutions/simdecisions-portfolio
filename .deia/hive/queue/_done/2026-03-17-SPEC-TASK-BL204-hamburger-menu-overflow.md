# BL-204: Fix hamburger menu overflow direction in pane status bars

## Objective
Fix the pane hamburger menu (PaneMenu.tsx) so it opens in the correct direction when near viewport edges, preventing menu items from being clipped or inaccessible.

## Context
PaneMenu.tsx (lines ~50-108) has direction calculation logic (openRight, openDown) and viewport overflow fallback (lines ~80-103). The menu currently overflows off-screen when panes are at the edges of the viewport. The transform calculation at line ~164-169 also needs fixing.

## Files to Read First
- `browser/src/shell/components/PaneMenu.tsx`
- `browser/src/shell/components/PaneChrome.tsx`
- `browser/src/shell/shell-themes.css`

## Deliverables
- [ ] Fix direction calculation to detect viewport edges correctly
- [ ] Fix overflow fallback to flip menu direction when near edges
- [ ] Fix transform calculation for proper positioning
- [ ] Tests for menu at all 4 viewport edges (top, bottom, left, right)
- [ ] Tests for menu in small panes

## Acceptance Criteria
- [ ] Menu opens fully visible when pane is at top edge
- [ ] Menu opens fully visible when pane is at bottom edge
- [ ] Menu opens fully visible when pane is at left edge
- [ ] Menu opens fully visible when pane is at right edge
- [ ] No CSS hardcoded colors
- [ ] All tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneChrome.test.tsx`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
