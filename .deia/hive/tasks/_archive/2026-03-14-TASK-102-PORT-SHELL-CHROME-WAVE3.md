# TASK-102: Port Shell Chrome — Wave 3 (Top Chrome Bars)

## Objective
Port 3 top-level chrome bar components from old repo to shiftcenter: MenuBar, ShellTabBar, WorkspaceBar. These are the most visible, most complex components in the shell chrome.

## Context
Wave 3 (final wave) of a 3-wave shell chrome port. These components are the user-facing chrome bars that provide workspace navigation, menu commands, and system-level controls. The spec is at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md`.

**Rule:** PORT, NOT REWRITE. Same props, same logic, same CSS classes. TypeScript conversion + `var(--sd-*)` theming only.

**Dependencies:** Wave 1 (TASK-100) and Wave 2 (TASK-101) should complete first to provide NotificationModal, ShortcutsPopup, LayoutSwitcher.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md` (lines 32–103 for these 3 components)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\MenuBar.tsx` (431 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ShellTabBar.tsx` (233 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\WorkspaceBar.jsx` (243 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (ShellState, ShellAction)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (actions, history)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\useShell.ts` (useShell hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (existing Shell with placeholders for MenuBar/ShellTabBar)

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (port from old, replace stub in Shell.tsx)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx` (port from old, replace stub in Shell.tsx)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx` (port from old)
- [ ] Vitest unit tests for all 3 components

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - MenuBar: Alt+F/E/V/H keyboard shortcuts, Escape closes menus, submenu navigation, modal backdrop click closes, File/Edit/View/Help menus with correct items, Settings integration, Theme submenu, Commands modal, About modal
  - ShellTabBar: active tab indicator, tab type icons (▶ hive, ◆ designer, 🌐 browser, 📊 ledger), close button on closeable tabs (hive cannot close), [+] dropdown for add tab (Designer/Browser/Ledger), click tab activates its pane
  - WorkspaceBar: undo/redo with past/future action labels, disabled when history empty, Ctrl+Shift+Z/Y shortcuts, active pane indicator (app type icon, label, "active" badge), theme toggle with portal (fixed position, z-index 9999, mouseDown+preventDefault), user badge (avatar, display name/email, logout)

## Constraints
- No file over 500 lines (MenuBar is 431 lines, acceptable)
- CSS: `var(--sd-*)` only
- No stubs
- Props interfaces MUST match spec exactly
- CSS class names MUST match spec
- Portal target for modals/pickers: `.hhp-root`
- WorkspaceBar sub-components (UndoRedoButtons, ActivePaneIndicator, ThemeToggle, UserBadge) are inline, NOT separate files
- MenuBar: wire to existing shell dispatch for layout presets (SET_LAYOUT action)
- WorkspaceBar: wire to existing shell state.past/future for undo/redo, use existing ThemePicker or build new one if needed
- ShellTabBar: read tabs from shell state, wire to SET_ACTIVE_TAB, ADD_TAB, CLOSE_TAB actions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-102-RESPONSE.md`

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
