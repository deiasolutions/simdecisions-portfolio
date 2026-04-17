# TASK-221: Fix Pane Drag-Drop Target Not Working

## Objective
Fix the drag-and-drop system so users can drag a pane (via the drag handle in PaneChrome) and drop it onto another open pane to create a split or tab. The drop target is not currently recognizing drops.

## Context
After investigating the codebase, the drag-drop infrastructure exists but has a wiring issue:

**Current State:**
- PaneChrome.tsx has a drag handle (line 118-126) with `draggable` and `onDragStart`
- ShellNodeRenderer.tsx has drop handlers (`onDragOver`, `onDrop`, `onDragLeave`) on the wrapper div (lines 301-303)
- The MOVE_APP action in reducer.ts is fully implemented and working
- DropZone visual feedback component exists and works

**The Bug:**
The drag handle is inside PaneChrome's title bar, but the drop target handlers are on ShellNodeRenderer's outer wrapper div. When dragging, the pointer events may not be reaching the drop target properly, or the drop zone detection is not triggering. The `e.preventDefault()` in `onDragOver` is critical for allowing drops — if it's not called, the drop won't work.

**Root Cause (likely):**
- The drag handle's cursor changes to `grab` but may not be propagating drag events correctly
- OR the drop target wrapper is not receiving `dragover` events because PaneChrome consumes them
- OR `e.dataTransfer.types.includes('hhs/node-id')` check (line 152) is failing

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (drag handle)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (drop target)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (MOVE_APP implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\DropZone.tsx` (visual feedback)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\utils.ts` (getDropZone helper)

## Deliverables
- [ ] Fix drag-drop so pane can be dragged and dropped onto another pane
- [ ] Visual drop zone indicator appears on dragover (left/right/top/bottom/center)
- [ ] Drop creates correct split (left/right/top/bottom) or tab (center)
- [ ] Drag handle cursor behavior works correctly (grab → grabbing)
- [ ] Tests cover all drop zones (center, left, right, top, bottom)
- [ ] Existing shell tests still pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - [ ] Dragging pane onto itself (should no-op)
  - [ ] Dragging onto locked pane (should block)
  - [ ] Dragging onto chrome:false pane (should no-op per ShellNodeRenderer line 147-148)
  - [ ] Drop zone positioning at edges (left, right, top, bottom)
  - [ ] Drop zone center creates tab
  - [ ] Visual feedback shows correct zone during drag
  - [ ] Drop on empty pane replaces content (per layout.ts line 154-155)

## Implementation Guidance
**Diagnosis Steps (do these FIRST):**
1. Add console.logs to PaneChrome `onDragStart` to verify it fires and sets dataTransfer correctly
2. Add console.logs to ShellNodeRenderer `onDragOver` to verify it receives events
3. Check if `e.dataTransfer.types` includes `'hhs/node-id'` during drag
4. Check if `e.preventDefault()` is being called in `onDragOver`
5. Test in browser DevTools: inspect drag events, check dataTransfer contents

**Likely Fixes:**
- Ensure PaneChrome title bar does NOT stop propagation of drag events
- Ensure ShellNodeRenderer wrapper receives dragover events (may need to adjust z-index or pointer-events)
- Verify `e.dataTransfer.effectAllowed = 'move'` in onDragStart is correct
- Verify `e.dataTransfer.dropEffect = 'move'` in onDragOver is set
- Consider adding `onDragEnter` handler to ShellNodeRenderer for better event handling
- Ensure drop zone ref is correctly attached and getBoundingClientRect works
- Consider adding data-drop-target attribute for debugging

**Testing Approach:**
Write tests that simulate:
1. Drag event on PaneChrome drag handle
2. Dragover event on ShellNodeRenderer wrapper at different positions (edges, center)
3. Drop event with correct dataTransfer data
4. Verify reducer receives MOVE_APP action with correct sourceId, targetId, zone

## Constraints
- No file over 500 lines (PaneChrome: 227 lines, ShellNodeRenderer: 316 lines — both OK)
- CSS: var(--sd-*) only (already enforced)
- No stubs
- TDD: write tests first, then fix

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-221-RESPONSE.md`

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
