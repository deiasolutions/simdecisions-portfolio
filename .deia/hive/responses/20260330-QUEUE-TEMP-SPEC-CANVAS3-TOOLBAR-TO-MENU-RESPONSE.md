# QUEUE-TEMP-SPEC-CANVAS3-TOOLBAR-TO-MENU: Move toolbar actions to File menu -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-30

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx`

## What Was Done

### FlowDesigner.tsx
1. **Removed TOOLBAR_ACTIONS_CHANGED emission** (lines ~342-377)
   - Deleted the `useEffect` that emitted toolbar action buttons (undo/redo/save/import/export)
   - Deleted the corresponding listener for `TOOLBAR_ACTION_INVOKED`

2. **Added File menu syndication** (line ~382)
   - Added new syndicated menu group targeting `file` menu with `groupLabel: "Diagram"`
   - Included 5 menu items: undo, redo, save, import, export
   - Each item has proper label, shortcut, and disabled state (for undo/redo)

3. **Updated menu action handler** (line ~453)
   - Added handlers for `file-undo`, `file-redo`, `file-save`, `file-import`, `file-export`
   - These handlers call the same functions as before (undo(), redo(), fileOpsRef methods)
   - Added comments to organize File/View/Tools/Edit menu actions

4. **Fixed dependency array** (line ~450)
   - Added `canUndo` and `canRedo` to the menu syndication `useEffect` dependency array
   - This ensures the menu updates when undo/redo availability changes

### MenuBarPrimitive.tsx
1. **Added File menu syndication support** (line ~212)
   - Added syndicated groups rendering after the static File menu items (New Tab, Close Tab, Settings)
   - Uses the same pattern as Edit and View menus
   - Creates submenu with arrow indicator (▶)
   - Shows shortcuts and disabled states
   - Handles clicks via `handleSyndicatedAction` which emits `MENU_ACTION_INVOKED`

## Testing Notes

### Manual Smoke Test Steps
1. Load canvas3 set
2. Open File menu
3. Verify "Diagram" submenu appears with all 5 actions:
   - Undo (Ctrl+Z) — should be disabled initially
   - Redo (Ctrl+Y) — should be disabled initially
   - Save Diagram (Ctrl+S)
   - Import... (Ctrl+O)
   - Export PHASE-IR (Ctrl+E)
4. Verify no icon buttons appear in menu bar right side (except user status)
5. Make a change to the diagram (add a node)
6. Verify Undo becomes enabled in File > Diagram
7. Click Save in File > Diagram — verify it triggers save
8. Test keyboard shortcuts still work (Ctrl+Z, Ctrl+S, etc.)

### Expected Behavior
- **Before**: Undo/redo/save/import/export appeared as icon buttons (↩ ↪ 💾 📥 📤) in the menu bar toolbar area
- **After**: These actions appear as text menu items under File > Diagram submenu
- **Keyboard shortcuts unchanged**: Ctrl+Z, Ctrl+Y, Ctrl+S, Ctrl+O, Ctrl+E still work
- **Disabled states work**: Undo/redo are disabled when history is empty/at end

## Architecture Notes

The implementation uses the existing **menu syndication pattern**:
1. FlowDesigner emits `MENU_ITEMS_CHANGED` bus event with `targetMenu: 'file'`
2. MenuBarPrimitive subscribes to this event and stores syndicated groups
3. File menu dropdown renders syndicated groups using `getSyndicatedGroups('file')`
4. Clicking a menu item triggers `MENU_ACTION_INVOKED` bus event
5. FlowDesigner receives this event and executes the appropriate action

This pattern is already used for Edit, View, and Tools menus. The File menu now follows the same pattern.

## No Breaking Changes

- Keyboard shortcuts still work (handled in FlowDesigner's global keydown handler)
- The `hasSidebarPalette` prop behavior is unchanged (controls visibility of floating palette/toolbar)
- All existing functionality preserved — only the UI location changed
- MenuBarPrimitive already had the infrastructure for syndicated menus

## Constraints Satisfied

✅ Do not remove keyboard shortcut handling — shortcuts still work
✅ Do not change MenuBarPrimitive.tsx syndication logic — only added File menu rendering
✅ Keep the `MENU_ACTION_INVOKED` handler in FlowDesigner — unchanged, just added new cases
