# BUG-026: Kanban EGG fails with items.filter is not a function

## Objective
Fix the Kanban EGG so it loads without the "items.filter is not a function" error.

## Context
When loading ?egg=kanban, the app crashes with "items.filter is not a function". This means the kanban primitive receives items in wrong format (object instead of array, or undefined). The adapter or data source is returning the wrong shape.

## Files to Read First
- `eggs/kanban.egg.md`
- `browser/src/primitives/kanban/`
- `browser/src/apps/`
- `browser/src/shell/components/appRegistry.ts`

## Deliverables
- [ ] Trace the kanban data flow from adapter to primitive
- [ ] Fix the items data shape (ensure it's an array)
- [ ] Add defensive check for non-array items
- [ ] Test kanban loads with empty data, valid data, and malformed data

## Acceptance Criteria
- [ ] ?egg=kanban loads without errors
- [ ] Kanban board renders (even if empty)
- [ ] No "items.filter is not a function" error
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/kanban/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
