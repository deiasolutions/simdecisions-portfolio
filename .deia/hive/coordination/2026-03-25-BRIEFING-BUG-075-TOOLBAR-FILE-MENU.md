# BRIEFING: SPEC-BUG-075 — Move save/import/export from toolbar to File menu

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-25
**Spec:** `.deia/hive/queue/_active/SPEC-BUG-075-toolbar-file-menu.md`
**Model Assignment:** sonnet
**Priority:** P1

---

## Objective

Canvas toolbar currently exposes save/import/export as toolbar buttons alongside undo/redo. These file operations belong in the File menu instead. Split FlowDesigner's toolbar action syndication so only undo/redo remain as toolbar icons, and syndicate save/import/export to the File menu via `menu:items-changed` bus event.

## Context

### Current State (FlowDesigner.tsx lines 338-372)

FlowDesigner publishes 5 toolbar actions via `toolbar:actions-changed`:
- undo, redo (history operations — KEEP in toolbar)
- save, import, export (file operations — MOVE to File menu)

MenuBar.tsx currently has a File menu (lines 268-314) but it only shows:
- New Tab submenu
- Close Tab
- Settings

MenuBar already supports syndicated menu groups for Edit menu (lines 344-377) and View menu (lines 467-500). The same pattern needs to be applied to the File menu.

### What Needs to Change

1. **FlowDesigner.tsx (lines 338-356):**
   - Split the toolbar actions array into two separate bus emissions:
     - `toolbar:actions-changed` with ONLY undo/redo
     - `menu:items-changed` with save/import/export targeting File menu

2. **MenuBar.tsx (lines 268-314):**
   - Add syndicated groups rendering to File menu dropdown using `getSyndicatedGroups('file')`
   - Follow the exact same pattern as Edit menu (lines 344-377) or View menu (lines 467-500)

### Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (lines 338-372 — toolbar/menu syndication)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (lines 268-314 — File menu, lines 344-377 — Edit menu pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowToolbar.tsx` (for reference — this is the floating toolbar UI that displays the syndicated actions)

### Expected Behavior After Fix

**When canvas pane is focused:**
- Toolbar area shows: Undo (↩) | Redo (↪)
- File menu shows:
  - New Tab ▶
  - Close Tab
  - Settings
  - ─── (divider)
  - Flow ▶
    - Save Flow (Ctrl+S)
    - Import Flow
    - Export Flow

**When canvas pane is NOT focused:**
- Toolbar area is empty
- File menu shows only default items (New Tab, Close Tab, Settings)

### Acceptance Criteria (from spec)

- [ ] Toolbar area only shows undo/redo icons when canvas is focused
- [ ] File menu shows Save Flow, Import Flow, Export Flow when canvas is focused
- [ ] Clicking File > Save Flow triggers save action
- [ ] Clicking File > Import Flow triggers import action
- [ ] Clicking File > Export Flow triggers export action
- [ ] Undo/Redo still work from toolbar buttons
- [ ] Tests updated and all passing
- [ ] Build passes with no regressions

### Test Requirements

**FlowDesigner tests:**
- Verify `toolbar:actions-changed` emits only 2 actions (undo, redo)
- Verify `menu:items-changed` emits 1 group with targetMenu='file' and 3 items (save, import, export)
- Verify both emissions happen when hasSidebarPalette=false
- Verify both emissions update when canUndo/canRedo change

**MenuBar tests:**
- Verify File menu renders syndicated groups from `getSyndicatedGroups('file')`
- Verify clicking syndicated File menu items emits `menu:action-invoked` with correct actionId
- Verify File menu items are NOT shown when syndicatedMenus is empty (no focused pane)

### Constraints (from spec)

- TDD: update tests first, then implementation
- No file over 500 lines (both files are under this)
- CSS: var(--sd-*) only (no CSS changes needed)
- No stubs
- Menu syndication must use the same pattern as the Edit menu syndicated groups

### Smoke Test Commands

```bash
cd browser && npx vitest run src/apps/sim/ -- all sim tests pass
cd browser && npx vitest run src/shell/ -- all shell tests pass
cd browser && npx vitest run -- no regressions
```

---

## Task File Requirements

Write 1-2 task files (you decide if this is one task or needs to be split).

Each task file must include:
- Absolute file paths for all files to read/modify
- Specific line numbers to reference
- Test requirements with exact scenarios
- Deliverables matching the acceptance criteria
- All 8 sections of the response file template

Return the task files to me for review. Do NOT dispatch bees until I approve.

---

## Notes

- This is a simple refactoring — no new features, just moving existing actions from one syndication channel to another.
- The bus event types already exist (`menu:items-changed`, `menu:action-invoked`).
- The MenuBar already knows how to render syndicated groups (see Edit/View menus).
- FlowDesigner already listens for `menu:action-invoked` (lines 442-494) and handles save/import/export actions.
- The only NEW code is: splitting the toolbar emission and adding File menu syndication rendering in MenuBar.

**End of briefing.**
