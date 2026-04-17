# BRIEFING: Port Shell Chrome Components

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-14
**Priority:** P0

---

## Objective

Port 13 missing shell chrome components from the old repo (`platform/simdecisions-2/src/components/shell/`) to shiftcenter (`browser/src/shell/components/`). This is a PORT, not a rewrite. Same props, same logic, same CSS classes. TypeScript conversion + `var(--sd-*)` theming only.

## Why

The shell engine (reducer, split/merge, tabs) is solid and fully ported. But the user-facing chrome is gone — no menu bar, no workspace tabs, no spotlight, no pane menus, no notifications, no keyboard shortcuts popup, no layout switcher. Users can't discover features or manage their workspace. The shell is developer-usable but not user-usable.

## Spec

Read the full spec: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md`

It has exact props, state, CSS classes, behavior, and integration points for all 13 files.

## Source Files (OLD repo — READ ONLY, DO NOT MODIFY)

All source files are in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\`

| File | Lines | Dependencies |
|---|---|---|
| MenuBar.tsx | 431 | shellStore, settingsStore |
| ShellTabBar.tsx | 233 | shellStore |
| WorkspaceBar.jsx | 243 | shell.context, authStore |
| GovernanceProxy.tsx | 160 | shell.context, permissions |
| PaneMenu.jsx | 111 | shell.context, shell.utils, ChromeBtn, ContextMenu |
| SpotlightOverlay.jsx | 93 | shell.context, PaneChrome, AppFrame |
| PinnedPaneWrapper.jsx | 73 | shell.context, PaneChrome, AppFrame |
| NotificationModal.tsx | 64 | none |
| ScrollToBottom.tsx | 34 | none |
| LayoutSwitcher.tsx | 33 | shellStore |
| ShortcutsPopup.tsx | 27 | none |
| HighlightOverlay.tsx | 16 | none |
| dragDropUtils.ts | 62 | none |

## Target Location

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\`

## Existing ShiftCenter Shell Files to Read

Before decomposing, Q33N must read these to understand the current shell architecture:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\utils.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ContextMenu.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ChromeBtn.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx`

## Task Decomposition Guidance

Suggest 3 waves based on dependencies:

**Wave 1 — Standalone (no shell context dependencies):**
HighlightOverlay, ScrollToBottom, ShortcutsPopup, NotificationModal, LayoutSwitcher, dragDropUtils
— These are small, independent. Can be one task or two.

**Wave 2 — Shell-context-dependent:**
PaneMenu, PinnedPaneWrapper, SpotlightOverlay, GovernanceProxy
— These need shell.context / dispatch / PaneChrome / AppFrame which already exist in shiftcenter.

**Wave 3 — Top chrome bar:**
MenuBar, ShellTabBar, WorkspaceBar
— These are the most visible, most complex. MenuBar alone is 431 lines.

**Integration task (after all waves):**
Wire all components into Shell.tsx and ShellNodeRenderer.tsx. Add EGG config toggles (`ui.menuBar`, `ui.shellTabBar`, `ui.workspaceBar`).

## Model Assignment

- Wave 1: Haiku (small, straightforward ports)
- Wave 2: Sonnet (need to understand shell context integration)
- Wave 3: Sonnet (MenuBar is complex, WorkspaceBar has portal logic)
- Integration: Sonnet

## Constraints

- PORT, not rewrite. Read the old file, adapt imports and types, preserve behavior.
- TDD: tests first for each component
- CSS: `var(--sd-*)` only
- No file over 500 lines (MenuBar at 431 is fine as-is)
- No stubs
- Portal target: `.hhp-root`

## Deliverable

Write task files to `.deia/hive/tasks/`. Return to me for review before dispatching bees.
