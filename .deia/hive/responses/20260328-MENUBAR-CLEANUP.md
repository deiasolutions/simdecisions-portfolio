# MENUBAR-CLEANUP: Fix MenuBar Layout -- COMPLETE

**Status:** COMPLETE
**Model:** Opus (executed by Q33N directly per briefing)
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\__tests__\MenuBarPrimitive.test.tsx`

## What Was Done

- Filtered toolbar actions rendering: only `undo` and `redo` actions render as top-level bar buttons
- Save, import, export, and all other toolbar actions no longer render on the menu bar (they arrive via menu syndication into File dropdown)
- Undo button renders unicode arrow U+21A9 (↩), redo renders U+21AA (↪) -- standard unicode, not emoji
- Added `menu-bar-action-compact` CSS class for 24x24 compact button sizing
- Moved the flex spacer so undo/redo sit immediately after menu names (File, Edit, View, Help, [undo] [redo]) and user status is pushed to the right
- Menu syndication code (`syndicatedMenus`, `getSyndicatedGroups`, `handleSyndicatedAction`) verified intact and untouched
- Updated test "renders toolbar actions" to verify only undo/redo appear and save/export are absent
- Updated test "emits toolbar:action-invoked" to test undo button click instead of save

## Test Results

- Test file: `browser/src/primitives/menu-bar/__tests__/MenuBarPrimitive.test.tsx`
- **9 tests passed, 0 failed**
- Duration: 817ms

## Build Verification

```
 Test Files  1 passed (1)
       Tests  9 passed (9)
    Start at  11:32:23
    Duration  5.93s
```

## Acceptance Criteria

- [x] Only undo and redo render as top-level bar buttons
- [x] Save/import/export do NOT render on the bar
- [x] Undo/redo use unicode arrows (U+21A9, U+21AA), not emoji
- [x] Compact 24x24 button styling applied
- [x] Menu syndication code preserved unchanged
- [x] All tests pass

## Clock / Cost / Carbon

- **Clock:** ~5 minutes
- **Cost:** ~$0.15
- **Carbon:** negligible

## Issues / Follow-ups

- None. Canvas pane can still syndicate save/export/import into the File menu dropdown via `menu:items-changed` bus events -- that mechanism is untouched.
