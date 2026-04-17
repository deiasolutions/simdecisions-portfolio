# SPEC: Shell Reducer — Swap, Delete, Merge Fixes

## Priority
P0

## Objective
Fix three broken/missing shell reducer operations: pane swap without data loss, delete empty cell via FAB, and contiguous-edge merge on cell delete.

## Context
The shell reducer lives at `browser/src/shell/`. It was ported in TASK-008 (231 tests). Three operations are broken or missing per the applet-grid-layout-notes.md design doc.

Files to read first:
- `browser/src/shell/reducer.ts` — main reducer (or whatever the current filename is — check the directory)
- `browser/src/shell/utils.ts` — tree manipulation helpers
- `browser/src/shell/types.ts` — ShellTreeNode, ShellState types
- `browser/src/shell/constants.ts` — action types
- `browser/src/shell/__tests__/` — existing tests
- `browser/src/shell/components/EmptyPane.tsx` — FAB menu on empty panes (if it exists, check `browser/src/shell/` directory listing)

## Acceptance Criteria

### Fix 1: Swap without data loss
- [ ] When two panes are swapped, the swap changes the `appType` and `config` fields on the pane nodes — it does NOT unmount/remount the DOM components
- [ ] React keys on PaneContent containers do NOT change during swap — only the content reference changes
- [ ] State inside each app (terminal history, editor content, scroll position) is preserved after swap
- [ ] Test: swap terminal and text-pane, verify both retain their content

### Fix 2: Delete empty cell via FAB
- [ ] The FAB menu on empty panes includes a "Delete Cell" option
- [ ] Clicking "Delete Cell" removes the empty pane from the tree
- [ ] The space freed by deletion is handled by the merge rules (Fix 3)
- [ ] Test: create a split with one empty pane, delete it, verify the other pane fills the space

### Fix 3: Contiguous-edge merge on delete
- [ ] When a cell is deleted, check the neighbor that shares the longest continuous border
- [ ] If that neighbor is an EMPTY cell → the empty cell expands to fill the deleted space
- [ ] If that neighbor is an APPLET (has content) → the deleted space becomes an empty cell (neighbor does NOT auto-expand)
- [ ] Merge check uses COMPUTED LAYOUT POSITIONS (actual rendered pixel coordinates), not tree parentage
- [ ] Test: 2x2 grid, delete one empty cell next to another empty cell — the empty neighbor expands
- [ ] Test: 2x2 grid, delete one empty cell next to a terminal — the space becomes empty, terminal doesn't expand
- [ ] Test: vertical split, delete left pane — right pane fills entire width

### General
- [ ] All existing shell reducer tests still pass (0 regressions)
- [ ] 12+ new tests for swap, delete, and merge operations
- [ ] No file over 500 lines

## Smoke Test
- [ ] Load chat.egg.md, split a pane, swap two panes — content preserved in both
- [ ] Create an empty pane via split, delete it via FAB — space is reclaimed correctly

## Model Assignment
sonnet

## Constraints
- The merge rule implementation may need access to rendered layout dimensions. If the reducer doesn't have access to pixel coordinates, add a `layoutDimensions` field to ShellState that the renderer updates on each layout. The reducer reads it for merge decisions.
- Do NOT change the existing split/merge actions that work — only add the new behavior
