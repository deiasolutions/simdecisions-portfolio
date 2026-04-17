# BUG-025: Sim EGG fails to load

## Objective
Fix the Sim EGG so it loads successfully when navigating to ?egg=sim.

## Context
The Sim EGG fails to load entirely. This could be a missing adapter, unregistered app type, missing primitive, or bad EGG config. Need to trace the load path and fix whatever is broken.

## Files to Read First
- `eggs/sim.egg.md`
- `browser/src/shell/components/appRegistry.ts`
- `browser/src/shell/eggToShell.ts`
- `browser/src/shell/components/PaneContent.tsx`
- `browser/src/apps/`

## Deliverables
- [ ] Trace sim EGG load path and identify failure point
- [ ] Fix the failure (register missing app type, fix adapter, fix config)
- [ ] Sim EGG loads and shows its panes
- [ ] Test that sim EGG parses and renders

## Acceptance Criteria
- [ ] ?egg=sim loads without errors
- [ ] Sim EGG panes render correctly
- [ ] No console errors on load
- [ ] Test passes

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
