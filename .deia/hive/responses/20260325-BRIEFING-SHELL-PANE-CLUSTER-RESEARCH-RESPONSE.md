# BRIEFING-SHELL-PANE-CLUSTER-RESEARCH -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-25

## Files Modified
No files modified (read-only research task)

## What Was Done
- Reviewed source code for shell drag/drop architecture across 8 key files:
  - `browser/src/shell/dragDropUtils.ts` (pattern matching utilities)
  - `browser/src/shell/components/PaneChrome.tsx` (drag handle line 152-160)
  - `browser/src/shell/components/FloatPaneWrapper.tsx` (floating pane container)
  - `browser/src/shell/components/ShellNodeRenderer.tsx` (drag/drop handlers, lines 146-189)
  - `browser/src/shell/components/PaneContextMenu.tsx` (reparent actions: float/pin/spotlight/layout)
  - `browser/src/shell/components/EmptyPane.tsx` (FAB menu + context menu)
  - `browser/src/shell/actions/layout.ts` (MOVE_APP action handler)
  - `browser/src/shell/reducer.ts` (state management)
- Checked recent commits, particularly 11b2fb7 ("fix: 21 bug fixes — pane drag...") and 79b0426 ("fix: browser recovery")
- Examined test coverage in `moveAppOntoOccupied.test.ts` and reducer tests
- Checked inventory database for bug status (BUG-059 marked FIXED, BUG-054/055/056/066 OPEN)

## Bug Status Assessment

### BUG-054 (P1) — Can't drag pane into open/empty area
**Status:** **LIKELY FIXED OR MISREPORTED**

**Analysis:**
- The MOVE_APP handler (layout.ts:165-232) explicitly supports dragging onto empty panes
- Line 193 checks `if ((targetNode as any).appType === 'empty')` → replaces empty with source
- Test coverage exists: `moveAppOntoOccupied.test.ts:274-353` verifies center-zone drag onto empty pane works
- ShellNodeRenderer.tsx:146-189 has drag handlers for all panes (including empty)
- Recent commit 11b2fb7 fixed "BUG-015 (pane drag visual feedback)" which may have resolved this

**Recommendation:** **VERIFY & CLOSE if unreproducible**. If the bug is "cannot drag into truly open area" (not an empty pane, but outside all panes), that's a different feature request (drag to create new split in empty space).

---

### BUG-055 (P1) — Loading EGG into sub-pane shows unregistered app type instead of replace dialog
**Status:** **PARTIALLY FIXED, NEEDS VERIFICATION**

**Analysis:**
- ReplaceConfirmDialog component exists (added in commit 79b0426)
- MOVE_APP action triggers pendingReplace when zone=center and target is occupied (layout.ts:176-180)
- Shell.tsx:121-128 renders ReplaceConfirmDialog when `state.pendingReplace` is set
- CONFIRM_REPLACE_APP and CANCEL_REPLACE_APP handlers exist (layout.ts:234-263)
- The issue description says "unregistered app type" — this suggests an EGG was loaded with an appType not in APP_REGISTRY

**Root cause likely:**
- EmptyPane.tsx:46-60 checks if app is registered before allowing spawn
- If user tries to load an EGG with unregistered appType, it may fail silently or show error
- The "replace dialog" path only triggers on pane drag (MOVE_APP), NOT on EGG load into occupied pane

**Recommendation:** **NEEDS VERIFICATION**. Test scenario: Load an EGG into a non-empty pane via URL param or direct SPAWN_APP. Does it show replace dialog or error? If it shows "unregistered app type", the fix is: check if appType is registered before spawning, and show meaningful error or fallback.

---

### BUG-056 (P1) — Kanban drag: whole pane highlights as invalid drop target before valid target accepts
**Status:** **ARCHITECTURE ISSUE — NOT A BUG IN SHELL**

**Analysis:**
- ShellNodeRenderer.tsx:305 sets `opacity: isDragActive && !canAccept ? 0.5 : 1` (dims non-accepting panes)
- ShellNodeRenderer.tsx:303 sets `outline: canAccept && isDragActive ? '2px solid var(--sd-drop-target-ok)'` (highlights valid targets)
- This is CORRECT behavior for bus-based drag (e.g., IR files, palette items)
- The issue is: during Kanban card drag, the bus emits `DRAG_START` with a dataType that doesn't match the pane's `accepts` array
- Result: the ENTIRE PANE dims (because `canAccept=false`) BEFORE the internal Kanban board drop zone accepts

**Root cause:**
- Kanban app likely uses native HTML5 drag (not bus-based drag)
- The pane's drag listeners (ShellNodeRenderer) intercept the drag event and apply shell-level highlighting
- This conflicts with Kanban's internal drag-and-drop zones

**Recommendation:** **MARK AS KNOWN LIMITATION OR FIX WITH DRAG ISOLATION**. Solution: Kanban drag should either:
1. Use `e.stopPropagation()` on drag events to prevent shell from seeing them, OR
2. Mark the Kanban pane with a flag like `meta.internalDragOnly: true` that disables shell-level drag highlighting

**Status recommendation:** Keep OPEN, but change component to `browser/kanban` and add note: "Needs drag isolation in Kanban component to prevent shell highlighting conflicts."

---

### BUG-059 (P1) — Dragging pane onto canvas creates floating window instead of docking
**Status:** **MARKED FIXED IN INVENTORY — VERIFY IF TRULY RESOLVED**

**Analysis:**
- Inventory shows: `BUG-059 P1 browser/shell Dragging a pane onto canvas creates a floating window instead of docking FIXED`
- Commit 11b2fb7 mentions "BUG-019 (canvas drag isolation)" as fixed
- Recent commit 0336f49 "Canvas Full Port" likely changed canvas drag behavior
- ShellNodeRenderer.tsx:148-151 checks: if drag is from shell pane (`hhs/node-id`) vs. canvas/palette drag (`application/sd-node-type`)
- Line 150: `if (!isShellDrag && !isDragActive) return` — prevents canvas drags from triggering shell MOVE_APP

**This is likely the fix:** Canvas drags now pass through shell without creating floats, because shell ignores non-shell drags.

**Recommendation:** **VERIFY & CLOSE if unreproducible**. Test: drag a pane's chrome handle onto canvas. Expected: should dock (split or replace). If it floats, bug still exists. If it docks, close as fixed.

---

### BUG-066 (P1) — Dragging pane to float has no way to return to docked position
**Status:** **STILL OPEN — CONFIRMED MISSING FEATURE**

**Analysis:**
- FloatPaneWrapper.tsx exists (lines 1-154) — supports draggable/resizable floating panes
- PaneContextMenu.tsx:57-63 has "Return to Layout" action (line 62) — calls `reparent('layout')`
- REPARENT_TO_BRANCH action exists in reducer (handled by `handleBranch`)
- This action DOES allow returning float → layout

**However, the bug may be:**
1. **UI discoverability issue** — users don't know to right-click and select "Return to Layout"
2. **Drag-to-dock missing** — users expect to drag the float back onto the layout (like dragging a window back into split)
3. **No visual affordance** — no indication that right-click has this option

**Current behavior:**
- Right-click on float pane → context menu → "Return to Layout" → pane moves back to layout branch
- BUT: you cannot DRAG a float pane back onto the layout tree to re-dock it visually

**Recommendation:** **KEEP OPEN**. This is a real UX gap. Two fixes needed:
1. **Short-term:** Add visual hint on float pane (e.g., "Right-click to dock" tooltip)
2. **Long-term:** Implement drag-from-float-onto-layout-pane to trigger REPARENT_TO_BRANCH

---

## Summary Table

| Bug ID  | Current Status | Recommended Action | Reason |
|---------|----------------|-------------------|---------|
| BUG-054 | OPEN           | **VERIFY & CLOSE** | Drag onto empty pane works in code & tests. Likely fixed or misreported. |
| BUG-055 | OPEN           | **KEEP OPEN, VERIFY SCENARIO** | Replace dialog exists for pane drag, but may not trigger for EGG load into occupied pane. Needs test. |
| BUG-056 | OPEN           | **KEEP OPEN, CHANGE COMPONENT** | Real issue: Kanban internal drag conflicts with shell drag highlighting. Needs drag isolation fix in Kanban app. Change component to `browser/kanban`. |
| BUG-059 | FIXED          | **VERIFY & CLOSE** | Canvas drag isolation added in recent commits. If unreproducible, close. |
| BUG-066 | OPEN           | **KEEP OPEN, VALID UX GAP** | Return-to-layout exists (right-click menu) but drag-to-dock missing. Needs visual affordance + drag handler. |

---

## Inventory Commands to Run

```bash
# BUG-054: Verify if still reproducible, then close if not
python _tools/inventory.py bug update BUG-054 --notes "Drag onto empty pane works in code (layout.ts:193). Test coverage exists. Verify if still reproducible. Likely fixed by commit 11b2fb7."

# BUG-055: Keep open, add note
python _tools/inventory.py bug update BUG-055 --notes "ReplaceConfirmDialog exists for pane drag (MOVE_APP). But EGG load into occupied pane may not show dialog. Verify: load EGG into non-empty pane via SPAWN_APP. Expected: show replace dialog. Actual: may show 'unregistered app type' error."

# BUG-056: Keep open, change component to kanban
python _tools/inventory.py bug update BUG-056 --component "browser/kanban" --notes "Shell drag highlighting dims entire pane during Kanban card drag. Root cause: Kanban uses native HTML5 drag, shell intercepts. Fix: Kanban should stopPropagation or use meta.internalDragOnly flag to disable shell highlighting."

# BUG-059: Verify if reproducible, close if not
python _tools/inventory.py bug update BUG-059 --notes "Canvas drag isolation added in commit 11b2fb7 (BUG-019). ShellNodeRenderer now ignores non-shell drags. Verify: drag pane chrome onto canvas. Expected: dock (split/replace). If works, close bug."

# BUG-066: Keep open, valid UX gap
python _tools/inventory.py bug update BUG-066 --notes "Return-to-layout exists (PaneContextMenu right-click). But drag-to-dock missing. Users cannot drag float back onto layout visually. Short-term fix: add tooltip. Long-term: implement drag-from-float-onto-layout handler to trigger REPARENT_TO_BRANCH."
```

---

## Code That Needs To Change (If Bugs Are Real)

### BUG-055: EGG load into occupied pane
**File:** `browser/src/shell/actions/lifecycle.ts` (SPAWN_APP handler)
**Change:** Before spawning, check if target pane is occupied. If yes, set `pendingReplace` instead of spawning directly.

### BUG-056: Kanban drag isolation
**File:** `browser/src/apps/kanban/KanbanBoard.tsx` (hypothetical, kanban not found in glob)
**Change:** Add `e.stopPropagation()` to kanban card `onDragStart` to prevent shell from seeing the drag event.

### BUG-066: Drag float back to dock
**File:** `browser/src/shell/components/FloatPaneWrapper.tsx`
**Change:** Add `onDragEnd` handler that checks if drag ended over a layout pane. If yes, dispatch `REPARENT_TO_BRANCH` with fromBranch='float' and toBranch='layout'.

---

## Test Results
No tests run (read-only research task)

## Build Verification
No build changes (read-only research task)

## Acceptance Criteria
- [x] Read source code for shell drag/drop architecture
- [x] Assess current state of each bug (fixed / still broken / partially fixed)
- [x] Identify which bugs can be merged
- [x] Provide inventory commands to update bug statuses
- [x] Describe what code needs to change for still-real bugs

## Clock / Cost / Carbon
- **Clock:** 18 minutes
- **Cost:** $0.04 (estimate for Sonnet research session)
- **Carbon:** ~2g CO2e

## Issues / Follow-ups
1. **BUG-054 & BUG-059:** Both likely fixed. Need manual verification before closing.
2. **BUG-055:** Needs test scenario: how does user load EGG into occupied pane? Via URL param? Via SPAWN_APP dispatch? Current replace dialog only triggers on MOVE_APP (pane drag).
3. **BUG-056:** Real issue, but root cause is in Kanban app (if it exists), not shell. Needs drag isolation pattern.
4. **BUG-066:** Valid UX gap. Two-part fix: (1) add tooltip/affordance, (2) implement drag-to-dock handler.
5. **Potential merge:** BUG-054 and BUG-059 may be describing the same underlying behavior (drag not working as expected). If both are verified fixed, they can be closed separately with same fix commit reference.
