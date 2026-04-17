# BRIEFING: Fix MenuBar Layout — Remove Ghost Icons, Restore Undo/Redo

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

The MenuBarPrimitive was fixed for font size and unicode, but now:

1. The toolbar action buttons (save, import, export) had their emoji icons replaced with labels BUT the buttons still render on the menu bar as text. These should NOT be on the menu bar at all — they are canvas actions that should be syndicated INTO the File menu dropdown, not rendered as top-level bar buttons.

2. The undo/redo buttons that WERE on the menu bar (as toolbar actions from the canvas) should stay — but as proper undo/redo buttons after the menu names (File, Edit, View, Help, [undo] [redo]).

3. Save, import, export should be File menu items (syndicated from the canvas pane), NOT top-level bar buttons.

## Your Mission

### Read First

1. Read `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` — understand the current toolbar syndication
2. Read `browser/src/primitives/menu-bar/MenuBarPrimitive.css` — understand the styling

### Fix 1: Filter toolbar actions

In MenuBarPrimitive.tsx, the toolbar actions section (around line 407-423) renders ALL syndicated toolbar actions as buttons on the menu bar.

Change this so:
- **Only** `undo` and `redo` actions render as top-level bar buttons (small icon buttons after the menu names)
- All other toolbar actions (save, export, import, etc.) should NOT render on the bar
- Filter by checking `action.id` — only render if `action.id === 'undo'` or `action.id === 'redo'`

For undo/redo buttons:
- Use simple SVG or text: undo = `↩` (U+21A9), redo = `↪` (U+21AA) — these are standard unicode arrows, not emoji
- Or better: use `action.label` as title and render a small simple arrow character
- Style them as compact 24x24 buttons matching the menu bar height

### Fix 2: Remove ghost buttons

After filtering, the save/import/export buttons should no longer appear on the menu bar at all. They will arrive via menu syndication into the File dropdown when the canvas pane sends `menu:items-changed` events.

### Fix 3: Verify menu syndication still works

The existing code for menu syndication (syndicatedMenus state, getSyndicatedGroups function) should still work. Canvas pane can syndicate items into File/Edit/View/Tools menus via the `menu:items-changed` bus event. This is the correct mechanism for save/export/import.

Do NOT change the syndication code — just verify it's still present.

### Fix 4: Run tests

Run `npx vitest run menu-bar` from browser/. Fix any failures.

## Deliverable

Write to: `.deia/hive/responses/20260328-MENUBAR-CLEANUP.md`

## Constraints

- Edit ONLY: `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` and `browser/src/primitives/menu-bar/MenuBarPrimitive.css`
- Do NOT edit any other files
- Read each file BEFORE editing
- Keep the syndicated menu logic intact — only change the toolbar actions rendering

## Model Assignment

Sonnet — TSX + CSS surgical fix.
