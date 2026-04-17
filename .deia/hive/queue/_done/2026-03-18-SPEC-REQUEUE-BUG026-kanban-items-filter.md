# BUG-026 (RE-QUEUE): Kanban EGG fails with items.filter is not a function

## Background — Why Re-Queued
Previous bee claimed COMPLETE and modified useKanban.ts, but the file doesn't exist at that path. The kanban adapter is at `browser/src/apps/kanbanAdapter.tsx` and the primitive is at `browser/src/primitives/kanban-pane/`. Needs verification that the fix actually landed and works.

## Objective
Fix the Kanban EGG so it loads without the "items.filter is not a function" error. The kanban primitive receives items in wrong format (object instead of array, or undefined).

## Files to Read First
- `eggs/kanban.egg.md`
- `browser/src/apps/kanbanAdapter.tsx` (the actual adapter file)
- `browser/src/primitives/kanban-pane/` (the kanban primitive)
- `browser/src/shell/components/appRegistry.ts`

## Deliverables
- [ ] Trace the kanban data flow from adapter to primitive
- [ ] Fix the items data shape (ensure it's always an array)
- [ ] Add defensive check: `Array.isArray(items) ? items : []`
- [ ] Test kanban loads with empty data, valid data, and malformed data

## Acceptance Criteria
- [ ] ?egg=kanban loads without errors
- [ ] Kanban board renders (even if empty)
- [ ] No "items.filter is not a function" error
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/kanban-pane/`
- [ ] `cd browser && npx vitest run --reporter=verbose src/apps/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify source code, not just tests

## Model Assignment
sonnet

## Priority
P0

## Re-Queue Metadata
- Original spec: `_done/2026-03-17-SPEC-TASK-BUG026-kanban-items-filter.md`
- Previous response: `20260317-BUG-026-RESPONSE.md`
- Failure reason: Bee modified wrong file path; actual adapter is kanbanAdapter.tsx not useKanban.ts
