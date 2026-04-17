# TASK-057: Delete Cell via FAB + Contiguous-Edge Merge Logic

**Date:** 2026-03-13
**Priority:** P0
**Model:** Sonnet
**Spec:** 2026-03-13-1801-SPEC-shell-swap-delete-merge.md
**Parent Briefing:** 2026-03-13-BRIEFING-shell-swap-delete-merge.md
**Depends on:** TASK-056 (swap fix, independent)

---

## Objective

Implement cell deletion via FAB menu + smart contiguous-edge merge that uses rendered layout positions to expand empty neighbors or create empty cells when applet neighbors exist.

---

## Problem

**Bug 2:** EmptyPane.tsx has a FAB menu with split/merge/tab options, but NO "Delete Cell" option.

**Bug 3:** When a cell is deleted (via current MERGE action), the reducer uses tree parentage to pick which sibling to keep. This doesn't work for complex layouts (2x2 grids, triple-splits, etc). We need merge logic that:

1. Uses COMPUTED LAYOUT POSITIONS (pixel coordinates) to find the neighbor with the longest shared border
2. If that neighbor is EMPTY → expand the empty cell to fill deleted space
3. If that neighbor is an APPLET (has content) → replace deleted cell with empty cell (neighbor does NOT auto-expand)

**Current MERGE action (layout.ts:74-82):**
```typescript
case 'MERGE': {
  const split = findNode(state.root, action.splitNodeId);
  if (!split || split.type !== 'split') return state;
  return withUndo(
    state,
    replaceNode(state.root, action.splitNodeId, split.children[action.keepChild ?? 0]),
    'Merge pane'
  );
}
```

This only handles binary splits by picking one child. It does NOT:
- Check pixel coordinates
- Find longest shared border
- Handle triple-splits or 2x2 grids
- Distinguish empty vs occupied neighbors

---

## Solution

### Part 1: Add layoutDimensions to ShellState

The reducer needs access to rendered layout positions to calculate shared borders. Add a new field to ShellState:

```typescript
export interface ShellState {
  root: BranchesRoot;
  focusedPaneId: string | null;
  maximizedPaneId: string | null;
  swapPendingId: string | null;
  layoutDimensions: Record<string, { x: number; y: number; w: number; h: number }>; // NEW
  workspaces: Workspace[];
  ledger: LedgerEvent[];
  lastFocusedByAppType: Record<string, string>;
  settingsRegistry: Record<string, PaneSettings>;
  past: ShellHistoryEntry[];
  future: ShellHistoryEntry[];
}
```

The renderer (ShellNodeRenderer or PaneContent) updates this field via a new action `UPDATE_LAYOUT_DIMENSIONS` every time layout changes.

### Part 2: Add UPDATE_LAYOUT_DIMENSIONS action

The renderer calls this action after every layout pass:

```typescript
dispatch({
  type: 'UPDATE_LAYOUT_DIMENSIONS',
  dimensions: {
    [nodeId]: { x: rect.left, y: rect.top, w: rect.width, h: rect.height }
  }
});
```

The reducer merges this into `state.layoutDimensions` (non-undoable update).

### Part 3: Add DELETE_CELL action

New action in types.ts:

```typescript
| { type: 'DELETE_CELL'; nodeId: string }
```

Implementation in actions/layout.ts:

```typescript
case 'DELETE_CELL': {
  const node = findNode(state.root, action.nodeId);
  if (!node || node.type !== 'app') return state;
  if (isLocked(state.root, action.nodeId)) return state;

  // Find all neighbors using layoutDimensions
  const dims = state.layoutDimensions[action.nodeId];
  if (!dims) {
    // Fallback: no layout data, just replace with empty
    return withUndo(state, replaceNode(state.root, action.nodeId, makeEmpty()), 'Delete cell');
  }

  const neighbors = findNeighborsWithSharedBorders(state.root, state.layoutDimensions, dims);
  if (neighbors.length === 0) {
    // Standalone pane, just replace with empty
    return withUndo(state, replaceNode(state.root, action.nodeId, makeEmpty()), 'Delete cell');
  }

  // Find neighbor with longest shared border
  const longest = neighbors.reduce((max, n) => n.sharedLength > max.sharedLength ? n : max);

  const longestNode = findNode(state.root, longest.nodeId);
  if (!longestNode || longestNode.type !== 'app') {
    // Not an app node, can't merge, replace with empty
    return withUndo(state, replaceNode(state.root, action.nodeId, makeEmpty()), 'Delete cell');
  }

  // Check if neighbor is empty
  if (longestNode.appType === 'empty') {
    // Expand empty neighbor to fill deleted space
    // This requires tree surgery to collapse the parent split
    const newRoot = expandNeighborToFill(state.root, action.nodeId, longest.nodeId);
    return withUndo(state, newRoot, 'Delete cell (expand neighbor)');
  } else {
    // Neighbor has content — replace deleted cell with empty, don't expand neighbor
    return withUndo(state, replaceNode(state.root, action.nodeId, makeEmpty()), 'Delete cell');
  }
}
```

### Part 4: Helper functions

**`findNeighborsWithSharedBorders(root, layoutDimensions, targetDims)`**

Iterate all nodes in the tree. For each node:
1. Get its layout dimensions
2. Check if it shares a border with the target node
3. Calculate shared border length (horizontal or vertical edge)
4. Return list of neighbors sorted by shared length

**`expandNeighborToFill(root, deletedNodeId, expandedNodeId)`**

Tree surgery to remove `deletedNodeId` and expand `expandedNodeId` to fill the space. This requires:
1. Find common parent split/triple-split
2. Remove deletedNodeId from children array
3. If parent becomes 1-child split → collapse parent to the remaining child
4. If parent is triple-split with 2 children left → convert to binary split
5. Return new root

### Part 5: Add "Delete Cell" to EmptyPane FAB menu

Edit EmptyPane.tsx (lines 41-89). Add a new menu item:

```typescript
const menuItems: ContextMenuItem[] = [
  // ... existing split/tab/applet items ...
  { separator: true, label: '' },
  {
    icon: '✕',
    label: 'Delete Cell',
    action: () => dispatch?.({ type: 'DELETE_CELL', nodeId: node.id }),
  },
];
```

Place it after the merge option (if parent is split) or at the end of the menu.

---

## Files to Modify

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`**
   - Add `layoutDimensions` field to ShellState
   - Add `UPDATE_LAYOUT_DIMENSIONS` action type
   - Add `DELETE_CELL` action type

2. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`**
   - Update INITIAL_STATE to include `layoutDimensions: {}`
   - Add handler for UPDATE_LAYOUT_DIMENSIONS (non-undoable merge into state)

3. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`**
   - Add DELETE_CELL case with merge logic
   - Implement `findNeighborsWithSharedBorders` helper
   - Implement `expandNeighborToFill` helper (or create new file `browser/src/shell/merge-helpers.ts` if this file approaches 500 lines)

4. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`**
   - Add ResizeObserver or ref callback to track layout dimensions
   - Dispatch UPDATE_LAYOUT_DIMENSIONS when dimensions change

5. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx`**
   - Add "Delete Cell" menu item to FAB menu

---

## Implementation Steps

### Step 1: Write tests FIRST (TDD)

Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.delete-merge.test.ts`

Write 12+ tests:

```typescript
describe('DELETE_CELL + Contiguous-Edge Merge', () => {
  describe('layoutDimensions tracking', () => {
    it('UPDATE_LAYOUT_DIMENSIONS merges dimensions into state', () => {
      // Setup: empty state
      // Action: UPDATE_LAYOUT_DIMENSIONS with {node1: {x: 0, y: 0, w: 100, h: 100}}
      // Assert: state.layoutDimensions[node1] === {x: 0, y: 0, w: 100, h: 100}
    });

    it('UPDATE_LAYOUT_DIMENSIONS is non-undoable (does not push to undo stack)', () => {
      // Setup: state with past.length = 0
      // Action: UPDATE_LAYOUT_DIMENSIONS
      // Assert: past.length still 0
    });
  });

  describe('DELETE_CELL basic behavior', () => {
    it('replaces cell with empty when no neighbors exist', () => {
      // Setup: single app node (root layout)
      // Action: DELETE_CELL
      // Assert: node appType becomes 'empty'
    });

    it('replaces cell with empty when no layout dimensions available', () => {
      // Setup: 2-pane split, layoutDimensions empty
      // Action: DELETE_CELL on one pane
      // Assert: pane becomes empty (fallback behavior)
    });

    it('rejects DELETE_CELL on locked pane', () => {
      // Setup: locked app node
      // Action: DELETE_CELL
      // Assert: state unchanged
    });

    it('rejects DELETE_CELL on non-app node (split/tabbed)', () => {
      // Setup: split node
      // Action: DELETE_CELL on split.id
      // Assert: state unchanged
    });
  });

  describe('findNeighborsWithSharedBorders', () => {
    it('finds vertical neighbor (left/right) with shared border', () => {
      // Setup: vertical split, two panes side-by-side
      // Mock layoutDimensions: pane1 {x:0, y:0, w:50, h:100}, pane2 {x:50, y:0, w:50, h:100}
      // Expected: pane1 and pane2 share vertical border of length 100
    });

    it('finds horizontal neighbor (top/bottom) with shared border', () => {
      // Setup: horizontal split, two panes stacked
      // Mock layoutDimensions: pane1 {x:0, y:0, w:100, h:50}, pane2 {x:0, y:50, w:100, h:50}
      // Expected: pane1 and pane2 share horizontal border of length 100
    });

    it('finds longest shared border in 2x2 grid', () => {
      // Setup: 2x2 grid (split vertical, each child is horizontal split)
      // Delete top-left pane — should find two neighbors (top-right, bottom-left)
      // Expected: whichever has longer shared border wins
    });

    it('returns empty array when no neighbors share borders', () => {
      // Setup: tabbed container with one pane (isolated, no spatial neighbors)
      // Expected: neighbors = []
    });
  });

  describe('DELETE_CELL with empty neighbor (expand)', () => {
    it('expands empty neighbor when deleting adjacent empty cell (vertical split)', () => {
      // Setup: vertical split, left pane empty, right pane empty
      // Action: DELETE_CELL on left pane
      // Assert: split collapses, right pane fills entire space
    });

    it('expands empty neighbor when deleting adjacent empty cell (horizontal split)', () => {
      // Setup: horizontal split, top pane empty, bottom pane empty
      // Action: DELETE_CELL on top pane
      // Assert: split collapses, bottom pane fills entire space
    });

    it('expands empty neighbor in 2x2 grid (longest border wins)', () => {
      // Setup: 2x2 grid, delete one empty cell
      // Mock layoutDimensions to favor one neighbor
      // Assert: favored empty neighbor expands
    });
  });

  describe('DELETE_CELL with applet neighbor (no expand)', () => {
    it('replaces deleted cell with empty when neighbor is applet (vertical split)', () => {
      // Setup: vertical split, left=empty, right=terminal
      // Action: DELETE_CELL on left
      // Assert: left becomes empty, terminal does NOT expand (split remains)
    });

    it('replaces deleted cell with empty when neighbor is applet (horizontal split)', () => {
      // Setup: horizontal split, top=empty, bottom=text-pane
      // Action: DELETE_CELL on top
      // Assert: top becomes empty, text-pane does NOT expand
    });

    it('replaces deleted cell with empty in 2x2 grid with applet neighbor', () => {
      // Setup: 2x2 grid, delete one empty cell next to terminal
      // Assert: deleted cell becomes empty, terminal stays same size
    });
  });

  describe('Triple-split edge cases', () => {
    it('deletes middle child of triple-split, collapses to binary split', () => {
      // Setup: triple-split (3 panes)
      // Action: DELETE_CELL on middle pane
      // Assert: triple-split becomes binary split with left and right children
    });

    it('deletes left child of triple-split, collapses to binary split', () => {
      // Setup: triple-split
      // Action: DELETE_CELL on left pane
      // Assert: triple-split becomes binary split with middle and right
    });
  });

  describe('Undo/redo', () => {
    it('DELETE_CELL pushes to undo stack', () => {
      // Setup: 2-pane split
      // Action: DELETE_CELL
      // Assert: past.length increased by 1
    });

    it('undo restores deleted cell', () => {
      // Setup: delete a cell, then undo
      // Assert: cell restored
    });
  });
});

describe('EmptyPane FAB menu', () => {
  it('includes "Delete Cell" option', () => {
    // Render EmptyPane, click FAB
    // Assert: menu includes item with label "Delete Cell"
  });

  it('dispatches DELETE_CELL when "Delete Cell" is clicked', () => {
    // Setup: mock dispatch
    // Render EmptyPane, click FAB, click "Delete Cell"
    // Assert: dispatch called with { type: 'DELETE_CELL', nodeId: node.id }
  });
});
```

Run tests, verify they fail.

### Step 2: Add layoutDimensions to ShellState

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`:

Add field to ShellState interface (around line 134):

```typescript
export interface ShellState {
  root: BranchesRoot;
  focusedPaneId: string | null;
  maximizedPaneId: string | null;
  swapPendingId: string | null;
  layoutDimensions: Record<string, { x: number; y: number; w: number; h: number }>; // NEW
  workspaces: Workspace[];
  ledger: LedgerEvent[];
  lastFocusedByAppType: Record<string, string>;
  settingsRegistry: Record<string, PaneSettings>;
  past: ShellHistoryEntry[];
  future: ShellHistoryEntry[];
}
```

Add action types (around line 169):

```typescript
export type ShellAction =
  // ... existing actions ...
  | { type: 'UPDATE_LAYOUT_DIMENSIONS'; dimensions: Record<string, { x: number; y: number; w: number; h: number }> }
  | { type: 'DELETE_CELL'; nodeId: string }
  // ... rest of actions ...
```

### Step 3: Update INITIAL_STATE

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (around line 18):

```typescript
export const INITIAL_STATE: ShellState = {
  root: {
    type: 'branches',
    layout: makeEmpty(),
    float: [],
    pinned: [],
    spotlight: null,
  },
  focusedPaneId: null,
  maximizedPaneId: null,
  swapPendingId: null,
  layoutDimensions: {}, // NEW
  workspaces: [],
  ledger: [],
  lastFocusedByAppType: {},
  settingsRegistry: {},
  past: [],
  future: [],
};
```

Add handler in shellReducer (around line 193):

```typescript
case 'UPDATE_LAYOUT_DIMENSIONS':
  return {
    ...state,
    layoutDimensions: { ...state.layoutDimensions, ...action.dimensions }
  };

case 'DELETE_CELL':
  return handleLayout(state, action, withUndo);
```

### Step 4: Implement DELETE_CELL logic

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`.

**Option A:** If file is under 400 lines, add helpers at the top and case at the bottom.

**Option B:** If file is near 500 lines, create new file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\merge-helpers.ts` with:

```typescript
export function findNeighborsWithSharedBorders(
  root: BranchesRoot | ShellTreeNode,
  layoutDimensions: Record<string, { x: number; y: number; w: number; h: number }>,
  targetDims: { x: number; y: number; w: number; h: number }
): Array<{ nodeId: string; sharedLength: number; edge: 'left' | 'right' | 'top' | 'bottom' }> {
  // Iterate all nodes, check if they share borders with target
  // ...
}

export function expandNeighborToFill(
  root: BranchesRoot | ShellTreeNode,
  deletedNodeId: string,
  expandedNodeId: string
): BranchesRoot | ShellTreeNode {
  // Tree surgery: remove deletedNodeId, expand expandedNodeId
  // ...
}
```

Then import in layout.ts and implement DELETE_CELL case.

### Step 5: Update ShellNodeRenderer to track dimensions

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`.

Add ResizeObserver or ref callback around line 66:

```typescript
useEffect(() => {
  if (node.type !== 'app' || !ref.current) return;

  const observer = new ResizeObserver(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    dispatch?.({
      type: 'UPDATE_LAYOUT_DIMENSIONS',
      dimensions: {
        [node.id]: { x: rect.left, y: rect.top, w: rect.width, h: rect.height }
      }
    });
  });

  observer.observe(ref.current);
  return () => observer.disconnect();
}, [node.id, dispatch]);
```

### Step 6: Add "Delete Cell" to EmptyPane FAB menu

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx`.

Add menu item after line 89:

```typescript
const menuItems: ContextMenuItem[] = [
  // ... existing items (split, tabs, applets, merge) ...
  { separator: true, label: '' },
  {
    icon: '✕',
    label: 'Delete Cell',
    action: () => dispatch?.({ type: 'DELETE_CELL', nodeId: node.id }),
  },
];
```

### Step 7: Run tests

```bash
cd browser
npx vitest run src/shell/__tests__/reducer.delete-merge.test.ts
```

All 12+ tests must pass.

### Step 8: Run full shell test suite

```bash
cd browser
npx vitest run src/shell/__tests__/
```

Ensure 0 regressions (all existing 231 tests + TASK-056's 9 tests + 12 new tests = 252+ tests passing).

---

## Acceptance Criteria

### Part 1: layoutDimensions tracking
- [ ] `layoutDimensions` field added to ShellState
- [ ] UPDATE_LAYOUT_DIMENSIONS action updates state.layoutDimensions (non-undoable)
- [ ] ShellNodeRenderer dispatches UPDATE_LAYOUT_DIMENSIONS on layout changes

### Part 2: DELETE_CELL action
- [ ] DELETE_CELL action defined in types.ts
- [ ] DELETE_CELL replaces cell with empty when no layout data exists (fallback)
- [ ] DELETE_CELL rejects locked panes
- [ ] DELETE_CELL rejects non-app nodes

### Part 3: Contiguous-edge merge logic
- [ ] findNeighborsWithSharedBorders uses pixel coordinates to find neighbors
- [ ] Neighbor with longest shared border is selected
- [ ] If neighbor is EMPTY → expandNeighborToFill collapses parent split
- [ ] If neighbor is APPLET → deleted cell becomes empty, neighbor does NOT expand
- [ ] Triple-split edge case: deleting child collapses to binary split

### Part 4: FAB menu
- [ ] EmptyPane FAB menu includes "Delete Cell" option
- [ ] Clicking "Delete Cell" dispatches DELETE_CELL action

### Part 5: Tests
- [ ] 12+ new tests in reducer.delete-merge.test.ts, all passing
- [ ] All existing shell tests still pass (0 regressions)

### Part 6: Smoke test scenarios (from spec)
- [ ] 2x2 grid, delete one empty cell next to another empty cell — the empty neighbor expands
- [ ] 2x2 grid, delete one empty cell next to a terminal — the space becomes empty, terminal doesn't expand
- [ ] Vertical split, delete left pane — right pane fills entire width

---

## Constraints

- **TDD:** Write tests first, then implementation
- **NO STUBS:** Every function fully implemented
- **File size limit:** 500 lines (if layout.ts approaches 500, create merge-helpers.ts)
- **NO HARDCODED COLORS:** Only CSS variables (no colors in this task)
- **CSS:** `var(--sd-*)` only

---

## Files Created/Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.delete-merge.test.ts`
- (Optional) `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\merge-helpers.ts` (if layout.ts approaches 500 lines)

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx`

---

## Testing

```bash
# Run delete-merge tests
cd browser
npx vitest run src/shell/__tests__/reducer.delete-merge.test.ts

# Run full shell suite
npx vitest run src/shell/__tests__/

# Expected: 12+ new tests passing, 240+ existing tests (231 shell + 9 swap) still passing (252+ total)
```

---

## Notes

- The key challenge is calculating shared borders from pixel coordinates. The algorithm should:
  1. For each candidate neighbor, check if any edge overlaps with the deleted cell's edges
  2. Calculate overlap length (for vertical neighbors, check y-overlap; for horizontal, check x-overlap)
  3. Return the neighbor with the longest overlap
- The expandNeighborToFill function must handle:
  - Binary splits (simple: replace split with expanded child)
  - Triple-splits (convert to binary split)
  - Nested splits (recursively collapse parents if they become 1-child splits)
- The FAB menu icon for "Delete Cell" should be visually distinct from "Merge Pane" — use '✕' or '🗑' (but avoid emoji per global rule — use '✕')

---

## Response File

When done, write: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-057-RESPONSE.md`

Use the 8-section mandatory format from BOOT.md.
