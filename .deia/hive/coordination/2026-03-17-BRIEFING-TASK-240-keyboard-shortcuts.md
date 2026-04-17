# BRIEFING: TASK-240 — Keyboard Shortcuts (Escape Protocol, Undo, Command Palette)

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Source Spec:** `docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.12
**Priority:** P1
**Model Assignment:** Sonnet (for complex state management and keyboard event handling)

---

## Objective

Implement three power-user keyboard shortcuts for the shell:

1. **Escape Protocol (Progressive Dismiss)** — Esc key sequentially closes modals → restores maximized panes → closes menus
2. **Ctrl+Z Undo** — Undo the last shell action (split, delete, move) with an undo stack (max 10 levels)
3. **Ctrl+Shift+P Command Palette** — Searchable modal for all shell actions with fuzzy filtering

---

## Context

Wave 4 Product Polish. The shell already has:
- Alt+key shortcuts for menus (MenuBar.tsx, lines 52-83)
- Escape closes menus (MenuBar.tsx)
- Maximize/restore with visual Escape hint (PaneChrome.tsx)
- A ShortcutsPopup.tsx that displays existing shortcuts

But these are NOT implemented:
- **Full escape protocol** — the sequential dismiss logic isn't wired globally
- **Undo stack** — no state history in shellReducer
- **Command palette** — doesn't exist

The bee must add these three features, update the shortcuts popup, and write tests for each.

---

## Files to Reference

**Existing keyboard handling:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (lines 52-83) — Current keyboard handler
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` — Maximize/restore with Escape hint
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MaximizedOverlay.tsx` — Maximized pane overlay
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShortcutsPopup.tsx` — Existing shortcuts display

**Shell state:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shellReducer.ts` — Shell state reducer (action types, state shape)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\ShellRoot.tsx` — Shell root component (likely place for global keydown listener)

---

## Deliverables Required

The bee must create task files that deliver:

### 1. Escape Protocol
- Global keydown listener in ShellRoot or MenuBar
- Sequential dismiss logic:
  1. If a modal/popup is open → close it
  2. Else if a pane is maximized → restore it
  3. Else if a menu is open → close it
- Hook into existing shell state (maximized pane, menu state, modal state)

### 2. Ctrl+Z Undo
- Add undo stack to shell reducer state (array of ShellState snapshots)
- New action: `UNDO` → restores previous state
- Track state changes for: `split`, `delete`, `merge`, `spawn_app` actions
- Max 10 undo levels (push new state, pop oldest if > 10)
- Ctrl+Z keyboard binding

### 3. Ctrl+Shift+P Command Palette
- New component: `CommandPalette.tsx`
- Searchable list of shell actions:
  - Split vertical/horizontal
  - Spawn app (all app types from registry)
  - Toggle maximize current pane
  - Close current pane
  - (More as appropriate)
- Fuzzy filter as user types
- Enter executes selected command
- Escape closes palette
- Styled with `var(--sd-*)` variables only (Rule 3)
- Centered modal overlay (similar to existing modals)

### 4. Update ShortcutsPopup
- Add the three new shortcuts to the display

### 5. Tests
- Test for escape protocol (sequential dismiss logic)
- Test for undo (state restoration after split/delete/merge)
- Test for command palette (render, search, execute, close)
- Run: `cd browser && npx vitest run src/shell/`

---

## Constraints (10 Hard Rules Apply)

- **Rule 3:** CSS uses `var(--sd-*)` only. No hex, rgb(), or named colors.
- **Rule 4:** No file over 500 lines. Modularize at 500.
- **Rule 5:** TDD. Tests first.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 10:** NO GIT OPERATIONS. Bee writes code, runs tests, writes response file. No commits.

---

## Model Assignment

**Sonnet** — This task requires complex state management (undo stack), global keyboard event coordination, and a new interactive component (command palette). Haiku is insufficient for this scope.

---

## Success Criteria

Q33N's task files must specify:

- [ ] Absolute file paths for all files to read, modify, or create
- [ ] Clear acceptance criteria for each of the 3 features
- [ ] Test requirements: how many tests, which scenarios, which files
- [ ] CSS constraint verification: all styles use `var(--sd-*)`
- [ ] File size constraint: confirm no file exceeds 500 lines
- [ ] Response file template requirement (8 sections)

---

## Next Steps

1. Q33N: Read the referenced files
2. Q33N: Write task file(s) for this work (may be 1 task or broken into 2-3 if scope is large)
3. Q33N: Return task files to Q33NR for review
4. Q33NR: Review and approve
5. Q33N: Dispatch bee(s)
6. Q33N: Review bee response(s)
7. Q33N: Report results to Q33NR

---

**END OF BRIEFING**
