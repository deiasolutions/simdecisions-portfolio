# TASK-240: Keyboard Shortcuts — Escape Protocol, Undo, Command Palette (W4 — 4.12)

## Objective
Implement the three power-user keyboard shortcuts: Escape protocol (progressive dismiss), Ctrl+Z undo in shell context, and Ctrl+Shift+P command palette.

## Context
Wave 4 Product Polish. MenuBar.tsx has Alt+key shortcuts for menus and Escape closes menus. But the full escape protocol (dismiss modals → close maximized → blur focused pane) isn't wired. No command palette exists. Ctrl+Z should undo the last shell action (split, delete, move).

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.12

## Files to Read First
- `browser/src/shell/components/MenuBar.tsx` — Current keyboard handler (lines 52-83)
- `browser/src/shell/components/PaneChrome.tsx` — Maximize/restore with Escape hint
- `browser/src/shell/components/MaximizedOverlay.tsx` — Maximized pane overlay
- `browser/src/shell/components/ShortcutsPopup.tsx` — Existing shortcuts display
- `browser/src/shell/shellReducer.ts` — Shell state reducer (action types)

## Deliverables
- [ ] Escape Protocol (progressive dismiss):
  1. If a modal/popup is open → close it
  2. If a pane is maximized → restore it
  3. If a menu is open → close it
  4. Wire via global keydown listener in ShellRoot or MenuBar
- [ ] Ctrl+Z Undo:
  - Add undo stack to shell reducer (store last N state snapshots)
  - UNDO action restores previous state
  - Track: split, delete, merge, spawn_app actions
  - Max 10 undo levels
- [ ] Ctrl+Shift+P Command Palette:
  - New component: `CommandPalette.tsx`
  - Searchable list of available actions (split, spawn app types, toggle maximize, etc.)
  - Fuzzy filter as user types
  - Enter executes selected command
  - Escape closes palette
  - Styled with `var(--sd-*)` variables, centered modal overlay
- [ ] Update `ShortcutsPopup.tsx` to include new shortcuts
- [ ] Add tests for each shortcut
- [ ] Run: `cd browser && npx vitest run src/shell/`

## Priority
P1

## Model
sonnet
