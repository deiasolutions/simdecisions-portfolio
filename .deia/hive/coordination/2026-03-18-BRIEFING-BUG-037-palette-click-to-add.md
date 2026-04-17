# BRIEFING: BUG-037 — Palette Click-to-Add Broken

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0

---

## Problem

Clicking on an item in the components palette tree-view no longer adds that component to the canvas. This is a reversion.

## Root Cause Analysis

After investigating the codebase and recent changes (BUG-022 response files), I've identified the issue:

**The architecture is partially wired:**

1. ✅ `treeBrowserAdapter.tsx` (line 209-218) correctly broadcasts `palette:node-drag-start` when a palette node is selected
2. ✅ Palette nodes have `meta.nodeType` with the correct type (Task, Queue, Start, etc.)
3. ❌ **`CanvasApp.tsx` does NOT subscribe to `palette:node-drag-start` or `palette:node-click` messages**
4. ✅ CanvasApp has drag-and-drop handlers (`onDrop`, line 421) but these require physical dragging
5. ❌ **Click-to-place functionality is missing from CanvasApp**

**Test evidence:**
- `paletteClickToPlace.test.tsx` line 322 shows the message type is `palette:node-drag-start`
- Line 311 test name says "message type must be exactly palette:node-click"
- This suggests there was confusion about which message type to use

## What Broke It

Looking at BUG-022 responses:
- BUG-022 fixed icon rendering and drag metadata
- It did NOT implement the click-to-place handler in CanvasApp
- The response file says "Click handling already wired" (line 35) but this is incorrect
- TreeBrowserAdapter broadcasts the message, but CanvasApp never listens

## Solution

**Add bus subscription to CanvasApp** to handle `palette:node-drag-start` (or standardize to `palette:node-click`):

1. In `CanvasApp.tsx`, add a new subscription in the existing `useEffect` (lines 181-215)
2. When `type === 'palette:node-drag-start'` (or `palette:node-click`), extract `nodeType` from `msg.data`
3. Create a new node at canvas center (or last click position)
4. Add it to the canvas via `setNodes()`

**Decision needed:** Should we use `palette:node-drag-start` or `palette:node-click`?
- Current code sends: `palette:node-drag-start`
- Test file says: `palette:node-click`
- Recommendation: **Use `palette:node-click`** for clarity (it's a click action, not drag)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 179-215 for bus subscription, lines 421-439 for onDrop pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 208-218 for how message is sent)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (shows expected behavior)

## Deliverables

1. **Add click-to-place handler to CanvasApp.tsx:**
   - Subscribe to `palette:node-click` in existing bus subscription (line 181-215)
   - Extract `nodeType` from `msg.data.nodeType`
   - Create node at canvas center (use `reactFlow.getViewport()` to calculate)
   - Use same node creation logic as `onDrop` handler (lines 431-438)

2. **Update treeBrowserAdapter.tsx** (line 211):
   - Change message type from `palette:node-drag-start` to `palette:node-click`
   - Keep data payload the same: `{ nodeType: node.meta.nodeType }`

3. **Update bus message types:**
   - Add `palette:node-click` to `browser/src/infrastructure/relay_bus/types/messages.ts`

4. **Update tests:**
   - Verify `paletteClickToPlace.test.tsx` still passes
   - Add integration test: click palette item → verify node appears on canvas

## Constraints

- No file over 500 lines (CanvasApp.tsx is currently 525 lines — already over limit but grandfathered)
- CSS: var(--sd-*) only
- No stubs
- TDD: Write test first, then implementation
- Do NOT break existing drag-and-drop functionality

## Test Requirements

- [ ] Test: Click palette Task node → Task node appears on canvas center
- [ ] Test: Click palette Queue node → Queue node appears on canvas center
- [ ] Test: Click palette Start node → Start node appears on canvas center
- [ ] Test: Multiple clicks create multiple nodes (not replace)
- [ ] Test: Dragging still works (don't break `onDrop`)
- [ ] All existing canvas tests still pass

## Model Assignment

**Sonnet** — This requires careful integration with existing bus subscription logic

## Success Criteria

User can click a palette item and it immediately appears on the canvas at the center (or a reasonable default position).

---

**Q33N: Please write task files for this fix and return them for my review.**
