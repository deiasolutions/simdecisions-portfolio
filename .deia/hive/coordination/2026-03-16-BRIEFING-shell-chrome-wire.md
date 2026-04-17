# BRIEFING: Wire shell chrome components

**Date:** 2026-03-16
**Priority:** P1.10
**Model:** haiku
**From:** Q33NR
**To:** Q33N

---

## Objective

Wire existing shell chrome components (MenuBar, ShellTabBar, SpotlightOverlay) into working state:
- MenuBar renders with all menu items functional
- ShellTabBar switches between workspaces/tabs correctly
- SpotlightOverlay opens via Ctrl+Shift+P keyboard shortcut

## Context

The shell chrome components already exist but need integration testing and keyboard shortcut wiring:

### Existing Components

1. **MenuBar** (`browser/src/shell/components/MenuBar.tsx`)
   - File | Edit | View | Help menus with items
   - Already has shell dispatch hooks
   - Needs verification that all actions work

2. **ShellTabBar** (`browser/src/shell/components/ShellTabBar.tsx`)
   - Displays tabs from first TabbedNode in layout
   - Shows active indicator, close buttons, [+] add button
   - Already has SET_ACTIVE_TAB, CLOSE_TAB, ADD_TAB actions

3. **SpotlightOverlay** (`browser/src/shell/components/SpotlightOverlay.tsx`)
   - Renders node in spotlight branch with backdrop
   - Click backdrop to dismiss
   - **MISSING:** Ctrl+Shift+P keyboard shortcut to open

### Shell Reducer Actions

Available in `browser/src/shell/reducer.ts`:
- `SET_ACTIVE_TAB` — switch active tab in a TabbedNode
- `CLOSE_TAB` — close tab by index
- `ADD_TAB` — add new tab to TabbedNode
- `REPARENT_TO_BRANCH` — move node between branches (layout/spotlight/float/pinned)
- `SET_FOCUS` — set focused pane
- `SPLIT`, `MERGE`, `FLIP_SPLIT` — layout operations
- `MAXIMIZE`, `RESTORE` — maximize/restore pane
- `SET_SWAP_PENDING` — swap pane positions

### What Needs Wiring

1. **MenuBar actions** — verify all menu items dispatch correct actions:
   - File menu: New Tab, Close Tab, Settings
   - Edit menu: Cut/Copy/Paste, Clear Terminal
   - View menu: Layout presets, Theme switching
   - Help menu: Commands, About modals

2. **ShellTabBar** — verify tab switching works correctly with shell state

3. **SpotlightOverlay keyboard shortcut** — add global Ctrl+Shift+P listener to:
   - Find focused pane (or create empty pane)
   - Dispatch `REPARENT_TO_BRANCH` with `toBranch: 'spotlight'`
   - Escape key already dismisses (handled in overlay)

### Files to Work With

**Components:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (may need spotlight keyboard shortcut here)

**State/Types:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (may not exist yet)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ShellTabBar.test.tsx` (may not exist yet)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx` (already exists)

## Acceptance Criteria

From spec:
- [ ] MenuBar renders with menu items
- [ ] Tab switching works
- [ ] Spotlight overlay opens/closes
- [ ] Tests written and passing

## Constraints

- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- Max 500 lines per file
- Heartbeats to build monitor every 3 minutes
- File claim system for parallel bee coordination

## Smoke Test

```bash
cd browser && npx vitest run src/shell/
```

No new test failures.

---

## Your Tasks (Q33N)

1. **Read the files** listed above to understand current state
2. **Write task files** for bee execution:
   - One task for MenuBar wiring + tests
   - One task for ShellTabBar verification + tests
   - One task for SpotlightOverlay keyboard shortcut + tests
3. **Return task files to Q33NR** for review before dispatch
4. **Do NOT dispatch bees yet** — wait for Q33NR approval

---

**Q33NR will review your task files and approve dispatch.**
