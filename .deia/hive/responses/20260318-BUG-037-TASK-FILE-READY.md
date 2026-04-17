# BUG-037: Palette Click-to-Place Broken — TASK FILE READY

**Status:** TASK FILE READY FOR REVIEW
**Model:** Sonnet (Q33N)
**Date:** 2026-03-18

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG037-palette-click-to-place.md`

---

## What Was Done

I read the briefing and analyzed the root cause:

### Root Cause Confirmed
1. ✅ TreeBrowserAdapter (line 209-218) broadcasts `palette:node-drag-start` when palette node selected
2. ✅ Palette nodes have `meta.nodeType` with correct values
3. ❌ **CanvasApp does NOT subscribe to ANY palette message** (neither `palette:node-drag-start` nor `palette:node-click`)
4. ✅ Drag-and-drop works via onDrop handler (lines 421-439)
5. ❌ **Click-to-place handler is completely missing from CanvasApp**

The test file `paletteClickToPlace.test.tsx` expects `palette:node-click` (line 311 comment, line 37 in test), but:
- TreeBrowserAdapter sends `palette:node-drag-start` (line 211)
- CanvasApp subscribes to neither

### Design Decision
Use `palette:node-click` (not `palette:node-drag-start`) for semantic clarity — this is a click action, not a drag initiation.

### Task File Structure

**3 file modifications:**
1. `messages.ts` — Add `PaletteNodeClickData` interface and union member
2. `treeBrowserAdapter.tsx` — Change line 211 from `palette:node-drag-start` to `palette:node-click`
3. `CanvasApp.tsx` — Add bus subscription handler for `palette:node-click` in existing useEffect (lines 181-215)

**Node creation pattern:**
- Uses `reactFlow.screenToFlowPosition()` (same as onDrop)
- Calculates canvas center via `window.innerWidth / 2`, `window.innerHeight / 2`
- Uses `mapIRType()` to normalize type string
- Same ID pattern: `${type.toLowerCase()}-${Date.now()}`
- Early return to prevent fallthrough

**Test requirements:**
- NO new tests written
- Existing test file `paletteClickToPlace.test.tsx` MUST pass as-is (12 tests)
- All existing canvas tests must pass (no regressions)

---

## Deliverables Summary

- [ ] Add `PaletteNodeClickData` interface to `messages.ts`
- [ ] Add `palette:node-click` to ShellMessage union
- [ ] Change TreeBrowserAdapter line 211: `palette:node-drag-start` → `palette:node-click`
- [ ] Add palette:node-click subscription to CanvasApp useEffect (lines 181-215)
- [ ] All 12 tests in `paletteClickToPlace.test.tsx` pass
- [ ] No regressions in canvas test suite
- [ ] Drag-and-drop still works (onDrop unchanged)

---

## Constraints Applied

- No file over 500 lines (CanvasApp is 525 — grandfathered, do NOT make longer)
- No stubs (full implementation required)
- TDD: Existing tests MUST pass without modification
- Message type: `palette:node-click` (not `palette:node-drag-start`)

---

## Model Assignment

**Sonnet** — Requires careful integration with existing bus subscription logic without breaking flow data / mutation array / highlight handlers.

---

## Ready for Q33NR Review

Please review the task file. If approved, I will dispatch BEE-SONNET to implement this fix.

**Expected result:** User clicks palette item → node appears on canvas center immediately.
