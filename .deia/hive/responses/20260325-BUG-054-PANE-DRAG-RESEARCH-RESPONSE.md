# BUG-054: Pane Drag Into Empty Area Research -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-25

## Root Cause Analysis

**BUG-054 is NOT broken.** The feature works exactly as designed. However, the bug report appears to be based on a misunderstanding of how empty panes render in different load states.

### The Real Issue: COLD Load State Wrapper Has No Drag Handlers

Empty panes have `loadState: 'COLD'` by default (see `makeEmpty()` in `utils.ts:36`). When `loadState === 'COLD'`, ShellNodeRenderer renders a DIFFERENT wrapper div (lines 234-249) that **does NOT have drag handlers attached**.

**Code Flow:**

1. **COLD state wrapper** (lines 234-249):
   - Renders `<EmptyPane>` inside a plain `<div>` with NO `onDragOver` or `onDrop`
   - The wrapper div at line 236 has NO drag handlers
   - Result: **Drag events never reach the handler logic**

2. **WARM state wrapper** (lines 252-282):
   - Has `pointerEvents: 'none'` in CSS (line 271)
   - Result: **Cannot receive any pointer/drag events**

3. **HOT state wrapper** (lines 285-321):
   - Has drag handlers attached at lines 308-309: `onDragOver={isDropTarget ? onDragOver : undefined}`
   - Condition: `isDropTarget = node.type === 'app' || node.type === 'tabbed'` (line 191)
   - Result: **This is the only state that accepts drops**

### Why Drag-to-Empty Doesn't Work

Empty panes created by `makeEmpty()` have `loadState: 'COLD'` (utils.ts:36). The COLD wrapper (ShellNodeRenderer.tsx:234-249) does NOT attach drag handlers. Therefore:

1. User drags pane A over empty pane B (which is COLD)
2. Empty pane B's wrapper div has no `onDragOver` handler
3. Browser never calls `e.preventDefault()` → drop is rejected by default
4. Drop never fires → MOVE_APP never dispatches

**The test passes** (moveAppOntoOccupied.test.ts:274-353) because **tests bypass rendering** — they call the reducer directly. The reducer logic is correct. The rendering layer blocks the interaction.

### The Fix

**File:** `browser/src/shell/components/ShellNodeRenderer.tsx`

**Lines to change:** 234-249 (COLD state wrapper)

**What to do:**

1. Add `onDragOver`, `onDrop`, and `onDragLeave` handlers to the COLD state wrapper (line 236)
2. Add `isDropTarget` condition check (same as HOT state, line 308)
3. Add state for `dropZone` rendering inside COLD wrapper (currently only HOT has this, line 318)

**Specific code change:**

Replace the COLD state return block (lines 234-249) with:

```tsx
// COLD — do not render app at all
if (appNode.loadState === 'COLD') {
  return (
    <div
      ref={ref}
      data-pane-id={node.id}
      data-load-state="COLD"
      data-testid="node-cold"
      style={{
        flex: 1, minWidth: 0, minHeight: 0, position: 'relative',
        display: 'flex', flexDirection: 'column',
      }}
      onDragOver={isDropTarget ? onDragOver : undefined}
      onDrop={isDropTarget ? onDrop : undefined}
      onDragLeave={isDropTarget ? onDragLeave : undefined}
    >
      {isCollapsed ? <CollapsedPaneStrip node={appNode} /> : <EmptyPane node={appNode} />}
      {dropZone && <DropZone zone={dropZone} canAccept={canAccept} />}
      {showSwap && <SwapTarget nodeId={node.id} swapPendingId={swapPendingId} />}
    </div>
  );
}
```

**Why this works:**

- Adds the same drag handler pattern used by HOT state (lines 308-310)
- Allows COLD empty panes to accept drag events
- Displays drop zone visual feedback (line 318 pattern)
- Preserves all existing logic — just wires up the event handlers

---

## Impact on Related Bugs

### BUG-059: Unknown (need bug description)

Cannot determine without reading BUG-059 description. If BUG-059 involves dragging onto empty/COLD panes, this fix would resolve it.

### BUG-066: Unknown (need bug description)

Cannot determine without reading BUG-066 description. If BUG-066 involves dragging onto empty/COLD panes, this fix would resolve it.

---

## Additional Findings

### EmptyPane Component

`EmptyPane.tsx` does NOT have its own drag handlers. It relies entirely on the ShellNodeRenderer wrapper to handle drag events. EmptyPane only handles:
- Click to focus (line 164)
- Right-click context menu (line 165)
- FAB button click (line 170)

EmptyPane itself is just a visual component — it does not participate in drag-drop beyond being a visual target.

### WARM State

WARM state panes (lines 252-282) have `pointerEvents: 'none'` and `visibility: 'hidden'`. These are intentionally non-interactive (used for preloading/warming up apps before making them visible). Drag-to-WARM should remain blocked — this is correct behavior.

### HTML5 Drag-Drop Requirements Met

The existing HOT state implementation correctly:
- Calls `e.preventDefault()` in `onDragOver` (line 152) ✓
- Sets `e.dataTransfer.dropEffect = 'move'` (line 153) ✓
- Calls `e.preventDefault()` in `onDrop` (line 166) ✓
- Uses correct MIME type `hhs/node-id` for shell drags (line 150) ✓

The problem is NOT missing `preventDefault()` — it's that the COLD wrapper never calls the handlers at all.

---

## Verification Plan

After implementing the fix:

1. **Manual test:**
   - Load an EGG with multiple panes (e.g., `canvas.egg.md` or `sim.egg.md`)
   - Delete an app from one pane to make it empty → pane becomes COLD
   - Drag another pane over the empty pane
   - Verify: Drop zone overlay appears (left/right/top/bottom/center)
   - Drop the pane
   - Verify: MOVE_APP fires, pane moves to target location

2. **Add integration test:**
   - Create `ShellNodeRenderer.drag-to-cold.test.tsx`
   - Render a COLD empty pane
   - Simulate `dragOver` event with `hhs/node-id` dataTransfer
   - Assert: `dropZone` state updates (drop zone overlay renders)
   - Simulate `drop` event
   - Assert: `dispatch` called with `MOVE_APP` action

3. **Check existing tests:**
   - Run `moveAppOntoOccupied.test.ts` — should still pass (tests bypass rendering)
   - Run full shell test suite — no regressions expected

---

## Files Modified

**None** — This is read-only research as requested.

## What Was Done

- Read full drag-drop flow from PaneChrome → ShellNodeRenderer → layout.ts
- Traced load state rendering paths (COLD/WARM/HOT)
- Identified that COLD wrapper lacks drag handlers
- Confirmed HOT wrapper has correct implementation
- Identified exact code change needed (add 3 props to COLD wrapper div)
- Verified test coverage exists but bypasses the rendering bug

## Test Results

No tests run — read-only research.

## Build Verification

No build run — read-only research.

## Acceptance Criteria

- [x] Identified exact root cause (COLD wrapper has no drag handlers)
- [x] Identified specific files and line numbers (ShellNodeRenderer.tsx:236-248)
- [x] Described the fix (add onDragOver/onDrop/onDragLeave + dropZone render to COLD wrapper)
- [ ] Determined impact on BUG-059/BUG-066 (need bug descriptions to assess)

## Clock / Cost / Carbon

- **Clock:** 25 minutes
- **Cost:** ~$0.15 (sonnet research session)
- **Carbon:** ~12g CO2e

## Issues / Follow-ups

1. **BUG-059 and BUG-066:** Need descriptions to determine if this fix resolves them
2. **Loadstate transition edge case:** If a pane transitions COLD→HOT mid-drag, the drag state (dropZone, canAccept) might not transfer. Not a current issue but worth noting for future drag refactors.
3. **Test gap:** Current tests bypass rendering. Consider adding a ShellNodeRenderer drag integration test that actually renders the component and fires DOM drag events.
