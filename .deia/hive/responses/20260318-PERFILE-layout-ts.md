# Per-File Consolidation: browser/src/shell/actions/layout.ts

**Compiled by:** Research Bee (Sonnet 4.5)
**Date:** 2026-03-18
**File Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`

---

## Current State

**Line count:** 432 lines
**Git hash:** a64d084 (latest commit: FIX-MOVEAPP-TESTS)
**Last modified:** 2026-03-18 11:28

**Exports:**
- `handleLayout(state, action, withUndo)` — Main action handler for layout-related shell actions

**Actions handled:**
1. `SPLIT` — Split a pane into two panes
2. `MERGE` — Merge a split back into a single pane
3. `ADD_TAB` — Add a tab to a pane or create tabbed container
4. `CLOSE_TAB` — Close a tab from a tabbed container
5. `REORDER_TAB` — Reorder tabs within a tabbed container
6. `SET_ACTIVE_TAB` — Change the active tab
7. `MOVE_APP` — Move a pane from one location to another (drag-drop)
8. `FLIP_SPLIT` — Flip split direction (vertical ↔ horizontal)
9. `TRIPLE_SPLIT` — Create a 3-way split
10. `UPDATE_TRIPLE_SPLIT_RATIOS` — Update ratios for triple splits
11. `REMOVE_TRIPLE_SPLIT_CHILD` — Collapse triple-split to binary split
12. `FLIP_TRIPLE_SPLIT` — Flip triple-split direction
13. `SET_SWAP_PENDING` — Set pending swap state
14. `SWAP_CONTENTS` — Swap contents between two panes
15. `UPDATE_RATIO` — Update split ratio
16. `DELETE_CELL` — Delete a pane (with smart neighbor expansion)

**Last known good behavior:**
- All 7 moveAppOntoOccupied tests passing (verified 2026-03-18 17:25)
- 430 total shell tests passing (from 443 total, 13 pre-existing failures)
- MOVE_APP correctly handles both sibling and non-sibling moves
- Special handling for siblings prevents parent split collapse

---

## Task History (Chronological)

### Task 1: BUG-015 — Drag Pane Into Stage (2026-03-17 23:20)

**Objective:** Fix drag-and-drop so dragging pane A onto occupied pane B works (triggers swap or creates tabs/split)

**What it was supposed to change:**
- Fix `ShellNodeRenderer.tsx` drag handlers to accept drops on occupied panes
- Update `DropZone.tsx` to show swap/split indicators
- Ensure `MOVE_APP` action handles occupied target correctly

**What the bee actually did:**
- **Modified:** `browser/src/shell/components/ShellNodeRenderer.tsx` (lines 146-162)
- **Added:** `setIsDragActive(true)` in `onDragOver` handler for `hhs/node-id` drops
- **Created test file:** `browser/src/shell/__tests__/moveAppOntoOccupied.test.ts` (11 test cases, 357 lines)
- **Did NOT modify:** `layout.ts` (MOVE_APP action was already working per BL-023)

**Root cause identified:**
- Visual feedback was missing because `isDragActive` was not set to `true`
- The outline CSS rule required both `canAccept && isDragActive` to render
- MOVE_APP action already handled occupied targets correctly (from BL-023 work)

**Status:** COMPLETE
- All acceptance criteria met
- Tests created but initially failed (7/7 failing)
- UI fix applied (visual feedback now works)
- **Critical finding:** The tests revealed a bug in MOVE_APP that BUG-015 didn't fix

---

### Task 2: BUG-044 — RAG Reliability Metadata (2026-03-18 11:23)

**Objective:** Fix RAG module collection error by adding missing `ReliabilityMetadata` class

**What it was supposed to change:**
- Add `ReliabilityMetadata` class to `hivenode/rag/indexer/models.py`
- Backend-only change, no frontend modifications expected

**What the bee actually did:**
- **Modified:** `hivenode/rag/indexer/models.py` (added ReliabilityMetadata class)
- **Did NOT touch:** `browser/src/shell/actions/layout.ts`

**Git evidence:**
```bash
git show 98241aa:browser/src/shell/actions/layout.ts
# File content identical to previous commit (888a0df)
```

**Status:** COMPLETE
- Commit 98241aa shows NO changes to layout.ts
- This task did NOT modify layout.ts (chronology report error)
- Verified by git diff: no changes between 888a0df and 98241aa for this file

**Conflict analysis verdict:** FALSE POSITIVE — BUG-044 did not touch layout.ts

---

### Task 3: FIX-MOVEAPP — Fix moveAppOntoOccupied Tests (2026-03-18 11:28)

**Objective:** Fix 7 failing tests created by BUG-015 (moveAppOntoOccupied.test.ts)

**What it was supposed to change:**
- Fix the MOVE_APP action in layout.ts to handle sibling moves correctly
- All 7 tests should pass after fix

**Root cause analysis (from response file):**
> "When source and target panes are siblings in a binary split, removing the source first caused the parent split to collapse, making the target unreachable."

**What the bee actually did:**

**Modified:** `browser/src/shell/actions/layout.ts` (lines 143-244, ~100 lines of logic)

**Key changes:**
1. **Detection logic:** Changed from `shareSameParent` to `areSiblings` with explicit `type === 'split'` check
2. **Sibling handling strategy:** Complete rewrite
   - OLD: Remove source → replace target → risk parent collapse
   - NEW: Modify parent split directly → replace target child with compound → replace source child with empty
3. **Duplication of compound structure logic:**
   - OLD: Single code path for creating tabs/splits
   - NEW: Two separate paths (sibling vs non-sibling) with duplicated logic for center/edge zones
4. **Preserved IDs:** Empty pane now replaces source slot (prevents tree collapse)

**Detailed code changes:**
```typescript
// BEFORE (lines 151-210)
const shareSameParent = sourceParent && targetParent && sourceParent.id === targetParent.id;

// Created replacement structure (tabs or split) — ONE TIME
if (zone === 'center') { /* tab logic */ }
else { /* split logic */ }

// Applied replacement — CONDITIONALLY
if (shareSameParent && sourceParent.type === 'split') {
  // Special handling for siblings
  const otherChild = sourceParent.children[0].id === sourceId ? sourceParent.children[1] : sourceParent.children[0];
  if (otherChild.id === targetId) {
    newRoot = replaceNode(state.root, sourceParent.id, replacement);
  } else {
    newRoot = removeNodeFromTree(state.root, sourceId);
    newRoot = replaceNode(newRoot, targetId, replacement);
  }
} else {
  // Standard flow
  newRoot = removeNodeFromTree(state.root, sourceId);
  newRoot = replaceNode(newRoot, targetId, replacement);
}

// AFTER (lines 151-244)
const areSiblings = sourceParent && targetParent && sourceParent.id === targetParent.id && sourceParent.type === 'split';

if (areSiblings && sourceParent.type === 'split') {
  // Sibling path: calculate indices
  const isSourceLeft = sourceParent.children[0].id === sourceId;
  const sourceIndex = isSourceLeft ? 0 : 1;
  const targetIndex = isSourceLeft ? 1 : 0;

  // Create compound structure — DUPLICATED LOGIC
  if (zone === 'center') { /* tab logic */ }
  else { /* split logic */ }

  // Modify parent directly
  const newChildren = [...sourceParent.children];
  newChildren[targetIndex] = replacement;
  newChildren[sourceIndex] = makeEmpty();
  const updatedParent = { ...sourceParent, children: newChildren };
  newRoot = replaceNode(state.root, sourceParent.id, updatedParent);

} else {
  // Non-sibling path: remove source first
  newRoot = removeNodeFromTree(state.root, sourceId);
  const targetInNew = findNode(newRoot, targetId);

  // Create compound structure — DUPLICATED LOGIC (AGAIN)
  if (zone === 'center') { /* tab logic */ }
  else { /* split logic */ }

  newRoot = replaceNode(newRoot, targetId, replacement);
}
```

**Lines of code:**
- OLD: ~60 lines for MOVE_APP
- NEW: ~100 lines for MOVE_APP (67% increase)

**Status:** COMPLETE
- All 7 tests now pass
- No regressions (430/443 shell tests passing)
- Git commit: a64d084

---

## Conflict Analysis

### Did Task 2 or 3 overwrite changes from Task 1?

**Answer:** No, because BUG-015 did NOT modify layout.ts.

**Evidence:**
1. BUG-015 response file states: "Fix ShellNodeRenderer drag event handlers" — modified ShellNodeRenderer.tsx, not layout.ts
2. BUG-015 response file states: "MOVE_APP action already working per BL-023; created tests to verify"
3. BUG-015 created test file that FAILED (7/7 failures)
4. FIX-MOVEAPP fixed the MOVE_APP action to make those tests pass

**Sequence:**
1. BUG-015 (23:20) → Modified ShellNodeRenderer.tsx → Created failing tests
2. BUG-044 (11:23) → Modified hivenode/rag/indexer/models.py → Did NOT touch layout.ts
3. FIX-MOVEAPP (11:28) → Modified layout.ts → Fixed MOVE_APP action → Tests now pass

**Conclusion:** No conflicts. Tasks operated on different files or different aspects of the same feature.

### Are all intended behaviors still present in the current code?

**YES.** All behaviors from all three tasks are present:

**From BUG-015:**
- ✅ Visual feedback on drag-over (via ShellNodeRenderer.tsx change)
- ✅ Drop zones appear on occupied panes (via DropZone component)
- ✅ MOVE_APP handles occupied targets (via FIX-MOVEAPP changes)

**From BUG-044:**
- ✅ ReliabilityMetadata class exists in RAG models (backend only)

**From FIX-MOVEAPP:**
- ✅ Sibling moves work correctly (parent split doesn't collapse)
- ✅ Non-sibling moves work correctly (standard flow preserved)
- ✅ All 7 moveAppOntoOccupied tests pass

### What's missing?

**Nothing is missing from the intended functionality.**

However, there are **code quality concerns:**

1. **Logic duplication:** The compound structure creation logic (tabs/splits) is duplicated in two branches (sibling vs non-sibling)
2. **Maintenance risk:** Any future changes to tab/split logic must be applied in two places
3. **File size:** MOVE_APP action grew from ~60 lines to ~100 lines (still under 500-line file limit)

**Recommendation:** Consider refactoring to extract compound structure creation into a helper function:
```typescript
function createCompoundStructure(zone, sourceNode, targetNode) {
  if (zone === 'center') { /* tab logic */ }
  else { /* split logic */ }
  return replacement;
}
```

This would reduce duplication and make the code easier to maintain.

---

## Required Final State

Based on all three tasks, `layout.ts` must:

### Functional Requirements

1. **MOVE_APP action (lines 143-244):**
   - ✅ Detect when source and target are siblings in a binary split
   - ✅ Handle sibling moves without collapsing parent split
   - ✅ Handle non-sibling moves with standard remove-then-replace flow
   - ✅ Support all 5 drop zones: center, left, right, top, bottom
   - ✅ Create tabbed containers for center zone drops
   - ✅ Create vertical splits for left/right zones
   - ✅ Create horizontal splits for top/bottom zones
   - ✅ Add to existing tabbed containers when dropping on tabs
   - ✅ Replace empty panes when dropping on empty slots
   - ✅ Replace source slot with empty pane (prevents collapse)

2. **All other actions (SPLIT, MERGE, TAB ops, etc.):**
   - ✅ No changes required from these tasks
   - ✅ All existing functionality preserved

### Non-Functional Requirements

- ✅ File under 500 lines (432 lines)
- ✅ No stubs or TODOs
- ✅ No console.logs or debug code
- ✅ Type-safe (TypeScript)
- ✅ Uses withUndo helper for undo/redo support
- ✅ Enforces max split depth
- ✅ Respects locked panes

### Known Limitations

- **Code duplication:** Compound structure logic duplicated in sibling/non-sibling branches
- **Complexity:** MOVE_APP action is ~100 lines (largest action handler in file)

---

## Current Test Status

### Test file: `browser/src/shell/__tests__/moveAppOntoOccupied.test.ts`

**Created by:** BUG-015 (2026-03-17 23:20)
**Fixed by:** FIX-MOVEAPP (2026-03-18 11:28)
**Line count:** 357 lines
**Test count:** 7 tests

**Test results (2026-03-18 17:25):**
```
✓ MOVE_APP with center zone on occupied pane creates tabs
✓ MOVE_APP center zone on already tabbed pane adds new tab
✓ MOVE_APP with left zone creates left split
✓ MOVE_APP with right zone creates right split
✓ MOVE_APP with top zone creates top split
✓ MOVE_APP with bottom zone creates bottom split
✓ MOVE_APP center zone on empty pane fills the slot

Test Files  1 passed (1)
Tests       7 passed (7)
Duration    14.80s
```

**Status:** ✅ ALL PASSING

### Full shell test suite

**Result (2026-03-18):**
- Total tests: 443
- Passing: 430
- Failing: 13 (pre-existing failures, unrelated to layout.ts changes)

**Status:** ✅ NO REGRESSIONS

### Test coverage for MOVE_APP action

**Scenarios covered:**
- ✅ Sibling moves with center zone → creates tabs
- ✅ Sibling moves with left zone → creates vertical split (source left)
- ✅ Sibling moves with right zone → creates vertical split (source right)
- ✅ Sibling moves with top zone → creates horizontal split (source top)
- ✅ Sibling moves with bottom zone → creates horizontal split (source bottom)
- ✅ Move onto existing tabbed container → adds tab
- ✅ Move onto empty pane → fills slot

**Scenarios NOT covered by moveAppOntoOccupied.test.ts:**
- ⚠️ Non-sibling moves (different parents)
- ⚠️ Locked panes (should reject move)
- ⚠️ Triple-split scenarios
- ⚠️ Nested splits (deep tree structures)
- ⚠️ Edge case: moving root node

**Note:** These scenarios may be covered by other test files in `browser/src/shell/__tests__/`

---

## Summary

**File status:** ✅ HEALTHY
**All tasks completed successfully:** YES
**Conflicts detected:** NO
**Tests passing:** YES (7/7 moveAppOntoOccupied, 430/443 full shell suite)
**Code quality:** GOOD (but could be refactored to reduce duplication)

**Key finding:** The chronology report incorrectly listed BUG-044 as touching layout.ts. Only BUG-015 (via test creation) and FIX-MOVEAPP (via action fix) affected the drag-drop behavior. BUG-044 was a backend-only change.

**Recommended next steps:**
1. ✅ No immediate action required — all functionality working
2. 📋 Consider refactoring MOVE_APP to extract compound structure creation into helper function
3. 📋 Add test coverage for non-sibling move scenarios (currently only tested implicitly)
4. 📋 Document the sibling detection strategy in code comments (currently minimal)

---

**Research complete. File consolidation verified against git history and test results.**
