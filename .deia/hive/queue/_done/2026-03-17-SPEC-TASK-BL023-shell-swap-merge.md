# BL-023: Shell reducer swap/delete/merge fixes

## Objective
Fix the shell reducer's SWAP_CONTENTS, DELETE_CELL, and MERGE action handlers so panes can be swapped, deleted, and merged correctly in Stage multi-pane layouts.

## Context
The shell reducer in `browser/src/shell/actions/layout.ts` handles SWAP_CONTENTS (lines ~280-310), DELETE_CELL (lines ~321-366), and MERGE (lines ~75-83). The merge helper functions in `browser/src/shell/merge-helpers.ts` handle neighbor detection and expansion. These operations are broken or incomplete, causing drag-drop and pane management failures across all EGGs.

## Files to Read First
- `browser/src/shell/actions/layout.ts`
- `browser/src/shell/merge-helpers.ts`
- `browser/src/shell/dragDropUtils.ts`
- `browser/src/shell/reducer.ts`
- `browser/src/shell/types.ts`
- `browser/src/shell/__tests__/reducer.swap.test.ts`
- `browser/src/shell/__tests__/reducer.delete-merge.test.ts`

## Deliverables
- [ ] Fix SWAP_CONTENTS handler to correctly swap two pane contents by ID
- [ ] Fix DELETE_CELL handler to remove a pane and redistribute space to neighbors
- [ ] Fix MERGE handler to combine adjacent panes with shared borders
- [ ] Fix findNeighborsWithSharedBorders() in merge-helpers.ts
- [ ] Fix expandNeighborToFill() in merge-helpers.ts
- [ ] All existing tests still pass
- [ ] New tests for edge cases: swap with self, delete last pane, merge non-adjacent

## Acceptance Criteria
- [ ] SWAP_CONTENTS correctly swaps two pane contents
- [ ] DELETE_CELL removes pane and redistributes space
- [ ] MERGE combines adjacent panes
- [ ] All reducer tests pass
- [ ] No file over 500 lines

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.swap.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.delete-merge.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.test.ts`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD: write tests first

## Model Assignment
sonnet

## Priority
P0
