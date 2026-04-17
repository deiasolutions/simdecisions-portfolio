# TASK-BUG-015: Fix Drag Onto Occupied Pane in Stage

## Objective
Fix drag-and-drop so users can drag a pane onto an already-occupied pane slot in Stage, triggering a swap or split instead of being rejected.

## Context
**Dependency:** BL-023 (shell swap/merge) is ✅ COMPLETE. SWAP_CONTENTS action exists and works correctly (200 tests passing).

**Current Problem:**
In Stage (multi-pane layout), dragging a pane onto an occupied slot does nothing. The user expects one of these outcomes:
- **Swap**: Pane A and pane B trade places
- **Split**: Pane A gets inserted next to pane B (creating a split container)
- **Tab**: Pane A joins pane B in a tabbed container

**What the Code Says:**
- `ShellNodeRenderer.tsx` lines 146-178: onDragOver handler exists, calls `e.preventDefault()`, sets drop zone
- `ShellNodeRenderer.tsx` lines 157-178: onDrop handler exists, dispatches MOVE_APP action
- `layout.ts` lines 143-184: MOVE_APP action handles occupied targets by creating tabs (line 156-168) or splits (lines 170-179)
- **Line 192:** `isDropTarget = node.type === 'app' || node.type === 'tabbed'` — should allow drops on both empty and occupied app nodes

**The Bug:**
Empirically verified by Q88N (Dave): dragging onto an occupied pane does nothing. The drop zone may not appear, or the drop may not register. Possible causes:
1. Event propagation issue (PaneChrome consuming drag events)
2. `isDropTarget` check failing for occupied panes
3. `canAccept` not being set correctly
4. Drop zone not rendering over PaneChrome
5. z-index stacking issue (DropZone under PaneChrome)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (drop target)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (drag source)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\DropZone.tsx` (visual feedback)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SwapTarget.tsx` (swap UI)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (MOVE_APP action)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\dragDropUtils.ts` (drop zone calculation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\dragDropUtils.test.ts` (existing tests)

## Deliverables
- [ ] **Diagnose the bug:** Add logging to trace drag events through PaneChrome → ShellNodeRenderer → dispatch. Identify where the event chain breaks.
- [ ] **Fix ShellNodeRenderer drag event handlers** to accept drops on occupied panes (if broken)
- [ ] **Fix DropZone** to show swap/split indicators on occupied panes (if not rendering)
- [ ] **Ensure MOVE_APP action** handles occupied target correctly (should already work per BL-023)
- [ ] **Tests for drag onto occupied pane scenarios:**
  - [ ] Drag pane A onto occupied pane B → creates tabbed container (center zone)
  - [ ] Drag pane A onto occupied pane B (left zone) → creates left split
  - [ ] Drag pane A onto occupied pane B (right zone) → creates right split
  - [ ] Drag pane A onto occupied pane B (top zone) → creates top split
  - [ ] Drag pane A onto occupied pane B (bottom zone) → creates bottom split
  - [ ] Drop zone visual indicators appear on hover over occupied panes
  - [ ] Existing drag-to-empty-slot behavior unchanged

## Test Requirements
- **TDD:** Write tests FIRST, then fix
- All existing drag-drop tests must still pass
- New tests must cover:
  - Drag from PaneChrome to occupied pane (various zones)
  - Drop zone rendering over PaneChrome
  - MOVE_APP dispatch with correct sourceId, targetId, zone

## Acceptance Criteria
- [ ] Dragging pane A onto occupied pane B triggers correct behavior (tab/split based on zone)
- [ ] Drop zone visual indicators appear on hover over occupied panes
- [ ] Existing drag-to-empty-slot behavior unchanged
- [ ] All drag-drop tests pass (existing + new)
- [ ] Smoke tests pass:
  - `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/dragDropUtils.test.ts`
  - `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.swap.test.ts`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (DropZone already compliant)
- No stubs
- TDD: tests first

## Investigation Steps (DO THESE FIRST)
1. Add `console.log` to `PaneChrome.tsx` drag handle `onDragStart` to verify it fires
2. Add `console.log` to `ShellNodeRenderer.tsx` `onDragOver` to verify it receives events for occupied panes
3. Check if `isDropTarget` is true for occupied app nodes
4. Check if `canAccept` is being set correctly during drag
5. Check if `DropZone` component renders (check z-index, check ref attachment)
6. Test in browser DevTools: drag a pane onto an occupied pane, inspect events in console
7. Compare behavior: drag onto empty pane (works?) vs drag onto occupied pane (doesn't work?)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-015-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Haiku (per spec)
**Priority:** P0
**Depends On:** BL-023 ✅ COMPLETE

---

**Q88NR signature**
Task file complete. Ready for bee dispatch.
