# TASK-170: Implement Pin and Collapse Reducer Logic -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-15

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\pin-collapse.test.ts` (372 lines, 18 tests)

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (1 comment update)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (+77 lines: imports, TOGGLE_PIN case, TOGGLE_COLLAPSE case)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\utils.ts` (+28 lines: findParentSplit, getSibling helper functions)

## What Was Done

### Action Types
- Confirmed `TOGGLE_PIN` and `TOGGLE_COLLAPSE` action types already present in `types.ts`
- Added comment clarification for pin/collapse section

### Helper Functions (utils.ts)
- Added `findParentSplit()`: finds parent split node (binary or triple) for a given node
- Added `getSibling()`: gets the sibling node in a binary split
- Both functions are branch-aware and use existing `findParent()` utility

### Reducer Logic (reducer.ts)
- **TOGGLE_PIN case:**
  - Finds target node, validates it's an AppNode
  - Finds parent split, validates it's a binary split (not triple, not tabbed)
  - If not in binary split → no-op with dev warning
  - Toggles `node.meta.isPinned` boolean
  - When pinning: sets sibling `meta.isCollapsed = true`
  - When unpinning: restores sibling `meta.isCollapsed = false`
  - Returns new tree with both nodes updated (immutable)

- **TOGGLE_COLLAPSE case:**
  - Finds target node, validates it's an AppNode
  - Checks if node is a pinned sibling (controlled by pin state)
  - If pinned sibling → no-op with dev warning (collapse controlled by pin)
  - Otherwise: toggles `node.meta.isCollapsed` boolean
  - Can collapse/expand pinned pane itself (allowed)
  - Returns new tree (immutable)

### Tests (TDD Approach)
- Created comprehensive test suite with **18 tests**:
  - **TOGGLE_PIN:** 9 tests covering pin/unpin, sibling collapse, no-ops for invalid contexts
  - **TOGGLE_COLLAPSE:** 6 tests covering collapse/expand, pinned sibling blocking
  - **Edge Cases:** 3 tests covering root panes, nested splits, meta initialization

## Test Results

### Pin-Collapse Tests
```
✓ src/shell/__tests__/pin-collapse.test.ts (18 tests) 6ms
  ✓ TOGGLE_PIN (9 tests)
    ✓ sets isPinned=true on pane in binary split
    ✓ collapses sibling pane when pinning
    ✓ unpins pane and restores sibling when toggling again
    ✓ no-op when pane not in binary split
    ✓ no-op when pane is in tabbed container
    ✓ no-op when pane is in triple split
    ✓ no-op when node not found
    ✓ works in vertical split
    ✓ can pin either pane in a split
  ✓ TOGGLE_COLLAPSE (6 tests)
    ✓ sets isCollapsed=true on pane
    ✓ sets isCollapsed=false when toggling again
    ✓ no-op when pane is pinned sibling (controlled by pin state)
    ✓ no-op when node not found
    ✓ can collapse pane that is NOT a pinned sibling
    ✓ can collapse pinned pane itself
  ✓ Edge Cases (3 tests)
    ✓ TOGGLE_PIN on root pane (no parent) is no-op
    ✓ nested binary splits can pin independently
    ✓ meta object is initialized if not present
```

### All Shell Tests
```
Test Files  18 passed (18)
Tests       373 passed (373)
Duration    8.51s
```

## Build Verification

### Test Suite Status
- **New tests:** 18 pin-collapse tests — **ALL PASSING**
- **Existing tests:** 355 shell tests — **ALL PASSING**
- **Total:** 373 tests passing, 0 failures

### Build Output
```bash
$ npm test -- src/shell/__tests__/ --run
✓ 18 test files (373 tests) — all passing
```

No TypeScript errors, no linting issues, all tests green.

## Acceptance Criteria

- [x] Add `TOGGLE_PIN` action to `ShellAction` type in `browser/src/shell/types.ts`
- [x] Add `TOGGLE_COLLAPSE` action to `ShellAction` type
- [x] Implement `TOGGLE_PIN` reducer case in `browser/src/shell/reducer.ts`:
  - [x] Find target node by nodeId
  - [x] Find parent split node (must be binary split)
  - [x] If not in binary split → no-op (log warning)
  - [x] Toggle `node.meta.isPinned` boolean
  - [x] If pinning: find sibling, set `sibling.meta.isCollapsed = true`
  - [x] If unpinning: restore sibling `sibling.meta.isCollapsed = false`
  - [x] Return new tree (immutable update)
- [x] Implement `TOGGLE_COLLAPSE` reducer case:
  - [x] Find target node by nodeId
  - [x] Toggle `node.meta.isCollapsed` boolean
  - [x] If pane is pinned sibling (sibling.meta.isPinned), don't allow manual collapse toggle
  - [x] Return new tree
- [x] Helper function `findParentSplit(tree, nodeId)` to locate parent split of a node
- [x] Helper function `getSibling(splitNode, childNodeId)` to find the other child in a binary split
- [x] Tests written FIRST (TDD)
- [x] Test `TOGGLE_PIN` sets `isPinned = true` and collapses sibling
- [x] Test `TOGGLE_PIN` again restores both panes to normal state
- [x] Test `TOGGLE_PIN` on pane not in binary split → no-op
- [x] Test `TOGGLE_COLLAPSE` sets `isCollapsed = true`
- [x] Test `TOGGLE_COLLAPSE` again restores to expanded state
- [x] Test `TOGGLE_COLLAPSE` on pinned sibling → no-op (pinned pane controls it)
- [x] All tests pass
- [x] Edge cases:
  - [x] Pin toggle on root pane (no parent) → no-op
  - [x] Pin toggle on tabbed pane → no-op (only binary splits supported)
  - [x] Collapse toggle while pinned sibling exists → no-op

## Clock / Cost / Carbon

### Clock
- Planning & file reading: 5 minutes
- Test writing (TDD): 15 minutes
- Implementation: 12 minutes
- Testing & validation: 8 minutes
- **Total:** 40 minutes

### Cost
- Model: Claude Sonnet 4.5
- Input tokens: ~51,500
- Output tokens: ~4,200
- Estimated cost: $0.42 USD

### Carbon
- Compute time: 40 minutes (LLM inference + local testing)
- Estimated carbon: ~8g CO₂e (cloud inference + local compute)

## Issues / Follow-ups

### None — Task Complete

All deliverables met:
- Action types added (were already present, confirmed)
- Reducer logic implemented for both TOGGLE_PIN and TOGGLE_COLLAPSE
- Helper functions created (findParentSplit, getSibling)
- Comprehensive tests written first (TDD approach)
- All 18 new tests passing
- All 373 shell tests passing
- No edge cases or blockers

### Next Steps (from task chain)
- **TASK-171:** Implement collapsed pane strip UI (CSS + component)
- **TASK-172:** E2E tests for pin/collapse behavior

### Notes
- Pin behavior only works in binary splits (2 children), not triple splits or tabbed containers
- Pinned sibling collapse state is controlled exclusively by the pin state (manual collapse blocked)
- Pinned pane itself can be collapsed/expanded manually (not controlled by pin)
- Meta object is properly initialized if not present (defensive coding)
- Dev warnings logged for invalid contexts (helps debugging)
