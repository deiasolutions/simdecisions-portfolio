# BUG-029: Stage app-add warns about taking over window instead of offering pane replacement

## Objective
Fix the app-add flow in Stage so that adding a new app offers to place it in a pane (replace, split, or new tab) instead of warning about taking over the entire window.

## Context
EmptyPane.tsx (lines ~44-57) has app spawning logic that uses window.confirm to warn about window takeover. In Stage (multi-pane layout), this should instead offer pane replacement. The Shell.tsx navigation handler (lines ~45-49) may also need adjustment.

## Files to Read First
- `browser/src/shell/components/EmptyPane.tsx`
- `browser/src/shell/components/Shell.tsx`
- `browser/src/shell/components/AppFrame.tsx`
- `browser/src/shell/reducer.ts`
- `browser/src/shell/types.ts`

## Deliverables
- [ ] Remove or replace window.confirm takeover warning in EmptyPane.tsx
- [ ] When in Stage layout, new app replaces the pane content (no warning)
- [ ] When in single-app mode, navigate normally via ?egg= param
- [ ] Tests for both Stage and single-app mode app-add behavior

## Acceptance Criteria
- [ ] Adding app in Stage replaces pane content without warning dialog
- [ ] Adding app in single-app mode navigates normally
- [ ] No regressions in existing pane behavior
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/EmptyPane.test.tsx`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
