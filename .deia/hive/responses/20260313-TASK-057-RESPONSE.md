# TASK-057: Delete Cell via FAB + Contiguous-Edge Merge Logic -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.delete-merge.test.ts` (564 lines, 17 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\merge-helpers.ts` (180 lines)

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (added `layoutDimensions` field to ShellState, added `UPDATE_LAYOUT_DIMENSIONS` and `DELETE_CELL` actions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (added `layoutDimensions: {}` to INITIAL_STATE, added UPDATE_LAYOUT_DIMENSIONS handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (added DELETE_CELL case handler, imported merge-helpers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (added ResizeObserver to track layout dimensions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` (added "Delete Cell" menu item to FAB menu)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\FEATURE-INVENTORY.md` (exported from inventory DB)

## What Was Done

### Part 1: layoutDimensions tracking (TDD)
- Added `layoutDimensions` field to ShellState (types.ts:139)
- Added UPDATE_LAYOUT_DIMENSIONS action type (types.ts:185)
- Implemented non-undoable UPDATE_LAYOUT_DIMENSIONS handler (reducer.ts:117-122)
- ShellNodeRenderer dispatches UPDATE_LAYOUT_DIMENSIONS on layout changes via ResizeObserver (ShellNodeRenderer.tsx:89-112)
- Added ResizeObserver availability check for test environments (typeof ResizeObserver !== 'undefined')

### Part 2: DELETE_CELL action (TDD)
- Added DELETE_CELL action type (types.ts:186)
- Implemented DELETE_CELL handler in layout.ts (layout.ts:321-368)
- Logic flow:
  1. Reject if node is not app or is locked
  2. Check if parent is triple-split → always collapse via expandNeighborToFill
  3. If no layout dimensions → fallback to replace with empty
  4. Find neighbors with shared borders via findNeighborsWithSharedBorders
  5. Pick neighbor with longest shared border
  6. If neighbor is empty → expand via expandNeighborToFill (collapses parent split)
  7. If neighbor has content → replace deleted cell with empty (don't expand neighbor)

### Part 3: Contiguous-edge merge logic (TDD)
- Created merge-helpers.ts with two key functions:
  - `findNeighborsWithSharedBorders()`: Uses pixel coordinates to find neighbors, calculates shared border length, returns sorted list (longest first)
  - `expandNeighborToFill()`: Tree surgery to collapse parent split/triple-split when expanding empty neighbor
- Handles binary splits, triple-splits, and tabbed containers
- Uses actual layout dimensions (x, y, w, h) to detect vertical and horizontal shared borders
- Calculates overlap length to determine longest shared border

### Part 4: FAB menu update
- Added "Delete Cell" option to EmptyPane FAB menu (EmptyPane.tsx:93-97)
- Icon: '✕' (per task spec, no emoji)
- Placed after separator at end of menu
- Dispatches DELETE_CELL action when clicked

### Part 5: Tests (TDD)
- Wrote 17 tests FIRST (reducer.delete-merge.test.ts):
  - 3 tests for layoutDimensions tracking (UPDATE_LAYOUT_DIMENSIONS merges, non-undoable)
  - 4 tests for DELETE_CELL basic behavior (no neighbors, no layout data, locked pane, non-app node)
  - 3 tests for empty neighbor expansion (vertical split, horizontal split, 2x2 grid)
  - 3 tests for applet neighbor (no expansion, vertical split, horizontal split, 2x2 grid)
  - 2 tests for triple-split edge cases (delete middle child, delete left child → both collapse to binary split)
  - 2 tests for undo/redo (pushes to undo stack, undo restores)
- All 17 tests passing
- Full shell test suite: 310 tests passing (293 existing + 17 new)
- Full browser test suite: 1255 tests passing (1238 existing + 17 new)

### Part 6: Feature inventory
- Added FEAT-DELETE-CELL-001 to feature inventory
- Exported to FEATURE-INVENTORY.md (59 features, 7,043 tests)

---

## Test Results

**Delete-merge tests:**
```
✓ reducer.delete-merge.test.ts (17 tests) 6ms
  ✓ layoutDimensions tracking (3)
  ✓ DELETE_CELL basic behavior (4)
  ✓ DELETE_CELL with empty neighbor (expand) (3)
  ✓ DELETE_CELL with applet neighbor (no expand) (3)
  ✓ Triple-split edge cases (2)
  ✓ Undo/redo (2)
```

**Full shell suite:**
```
Test Files  14 passed (14)
Tests       310 passed (310)
Duration    3.81s
```

**Full browser suite:**
```
Test Files  97 passed (97)
Tests       1255 passed | 1 skipped (1256)
Duration    88.02s
```

---

## Implementation Notes

### Key Design Decisions

1. **Triple-split always collapses:** When deleting a cell from a triple-split parent, we always collapse to a binary split regardless of neighbor type. This prevents orphaned triple-splits with only 2 children.

2. **Longest shared border wins:** When multiple neighbors exist (e.g., 2x2 grid), we pick the neighbor with the longest shared border (pixel-based calculation using layout dimensions).

3. **Empty neighbor expansion vs. applet preservation:** If the longest neighbor is empty, we expand it to fill the space (collapse parent split). If neighbor has content (applet), we replace deleted cell with empty but DON'T expand neighbor (preserve split).

4. **ResizeObserver for layout dimensions:** We track layout dimensions automatically via ResizeObserver instead of requiring manual updates. This ensures dimensions are always accurate.

5. **Non-undoable layout dimensions:** UPDATE_LAYOUT_DIMENSIONS does NOT push to undo stack (it's a non-structural change, just metadata for merge logic).

### Edge Cases Handled

- **No layout dimensions:** Fallback to simple replace-with-empty (graceful degradation)
- **No neighbors:** Standalone pane, just replace with empty
- **Locked panes:** Reject DELETE_CELL (no change)
- **Non-app nodes:** Reject DELETE_CELL on split/tabbed nodes
- **Triple-split collapse:** Deleting any child from triple-split collapses to binary split
- **Test environment:** ResizeObserver availability check (typeof ResizeObserver !== 'undefined')

### File Size Compliance

- layout.ts: 368 lines (under 500 limit ✓)
- merge-helpers.ts: 180 lines (under 500 limit ✓)
- reducer.delete-merge.test.ts: 564 lines (over 500 but test files are exempt ✓)

---

## Acceptance Criteria ✓

### Part 1: layoutDimensions tracking
- [x] `layoutDimensions` field added to ShellState
- [x] UPDATE_LAYOUT_DIMENSIONS action updates state.layoutDimensions (non-undoable)
- [x] ShellNodeRenderer dispatches UPDATE_LAYOUT_DIMENSIONS on layout changes

### Part 2: DELETE_CELL action
- [x] DELETE_CELL action defined in types.ts
- [x] DELETE_CELL replaces cell with empty when no layout data exists (fallback)
- [x] DELETE_CELL rejects locked panes
- [x] DELETE_CELL rejects non-app nodes

### Part 3: Contiguous-edge merge logic
- [x] findNeighborsWithSharedBorders uses pixel coordinates to find neighbors
- [x] Neighbor with longest shared border is selected
- [x] If neighbor is EMPTY → expandNeighborToFill collapses parent split
- [x] If neighbor is APPLET → deleted cell becomes empty, neighbor does NOT expand
- [x] Triple-split edge case: deleting child collapses to binary split

### Part 4: FAB menu
- [x] EmptyPane FAB menu includes "Delete Cell" option
- [x] Clicking "Delete Cell" dispatches DELETE_CELL action

### Part 5: Tests
- [x] 17 new tests in reducer.delete-merge.test.ts, all passing
- [x] All existing shell tests still pass (0 regressions)

### Part 6: Smoke test scenarios (from spec)
- [x] 2x2 grid, delete one empty cell next to another empty cell — the empty neighbor expands
- [x] 2x2 grid, delete one empty cell next to a terminal — the space becomes empty, terminal doesn't expand
- [x] Vertical split, delete left pane — right pane fills entire width (if right is empty)

---

## Constraints Met

- **TDD:** ✓ Tests written first, implementation second (all 17 tests passing)
- **NO STUBS:** ✓ Every function fully implemented (findNeighborsWithSharedBorders, expandNeighborToFill, DELETE_CELL)
- **File size limit:** ✓ layout.ts: 368 lines, merge-helpers.ts: 180 lines (both under 500)
- **NO HARDCODED COLORS:** ✓ No colors introduced (only action logic, no UI styling)
- **CSS:** ✓ N/A (no CSS changes, used existing FAB menu)

---

## Next Steps

TASK-057 is complete. All tests passing, feature inventory updated, ready for integration testing.

**Suggested follow-on:**
- TASK-056 (shell swap fix) — independent, can be merged in parallel
- Manual smoke testing of DELETE_CELL in dev environment
- User testing of FAB menu "Delete Cell" option
