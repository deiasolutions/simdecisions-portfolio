# TASK-240: Keyboard Shortcuts (Escape Protocol, Undo, Command Palette)

**Source:** WAVE-4-PRODUCT-POLISH.md, Task 4.12
**Priority:** P1
**Model:** Sonnet
**Date:** 2026-03-17

---

## Objective

Implement three power-user keyboard shortcuts for the shell:

1. **Escape Protocol (Progressive Dismiss)** — Esc key sequentially closes modals → restores maximized panes → closes menus
2. **Ctrl+Z Undo** — Undo the last shell action using existing `LAYOUT_UNDO` action with keyboard binding
3. **Ctrl+Shift+P Command Palette** — Searchable modal for all shell actions with fuzzy filtering

---

## Context

The shell already has:
- Undo/redo state management via `LAYOUT_UNDO`/`LAYOUT_REDO` actions (tested in `reducer.undo.test.ts`)
- Escape key closes menus (MenuBar.tsx, line 73)
- Maximize/restore via `MAXIMIZE`/`RESTORE` actions (reducer.ts)
- ShortcutsPopup.tsx component that displays shortcuts

**What's missing:**
- Global Escape protocol that handles sequential dismiss (modals → maximized panes → menus)
- Ctrl+Z keyboard binding to trigger `LAYOUT_UNDO`
- Command Palette component with searchable actions

---

## Files to Read First

### Shell State & Reducer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` — Shell reducer, undo actions on lines 67-89
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — ShellState, ShellAction types

### Components
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` — Root shell component (where global keyboard listener should go)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` — Existing keyboard handler (lines 52-83), Escape handling (lines 73-78)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MaximizedOverlay.tsx` — Maximized pane overlay
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` — Shows "Restore (Esc)" hint on line 205
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShortcutsPopup.tsx` — Existing shortcuts display (needs updating)

### Tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.undo.test.ts` — Undo/redo tests (all passing)

### Constants
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\constants.ts` — APP_REGISTRY (lines 64-89)

---

## Deliverables

### 1. Escape Protocol (Global Sequential Dismiss)

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

**Requirements:**
- Add global `keydown` event listener in Shell.tsx (using `useEffect`)
- On Escape key press, implement sequential dismiss logic:
  1. If MenuBar has open menu → close it (check `openMenu` state via ref or shared context)
  2. Else if a pane is maximized → dispatch `{ type: 'RESTORE' }`
  3. Else if a modal/popup is open → close it (check DOM for `.menu-modal-overlay` or `.applet-modal-backdrop`)
- Do NOT interfere with MenuBar's existing Escape handler for its own modals
- The handler should check `e.target` to avoid interfering with input fields using Escape

**Acceptance Criteria:**
- [ ] Escape key closes any open modal first (commands help, about, etc.)
- [ ] If no modal open but pane maximized, Escape restores the pane
- [ ] If no modal/maximized pane, Escape closes any open menu
- [ ] Escape does not interfere with text input (check `e.target.tagName`)

---

### 2. Ctrl+Z Undo Keyboard Binding

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

**Requirements:**
- In the same global `keydown` listener, add Ctrl+Z handler
- On `Ctrl+Z` (or `Cmd+Z` on Mac), dispatch `{ type: 'LAYOUT_UNDO' }`
- On `Ctrl+Shift+Z` (or `Cmd+Shift+Z`), dispatch `{ type: 'LAYOUT_REDO' }`
- Prevent default browser undo behavior: `e.preventDefault()`
- Do NOT trigger if user is typing in an input/textarea

**Acceptance Criteria:**
- [ ] Ctrl+Z undoes last structural shell action (split, merge, delete)
- [ ] Ctrl+Shift+Z redoes last undone action
- [ ] Does not interfere with text input fields (check `e.target.tagName`)
- [ ] Displays correct undo count in UI (optional: show undo/redo button state)

---

### 3. Command Palette

**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\CommandPalette.tsx`

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (add Ctrl+Shift+P handler, render CommandPalette)

**Requirements:**

#### CommandPalette.tsx Component
- Props: `{ isOpen: boolean; onClose: () => void }`
- Searchable modal overlay (centered, ~500px wide, ~400px tall)
- List of available commands:
  - **Layout actions:**
    - "Split Horizontal" → dispatch `SPLIT` action with focused pane
    - "Split Vertical" → dispatch `SPLIT` action with focused pane
    - "Maximize Pane" → dispatch `MAXIMIZE` with focused pane
    - "Restore Pane" → dispatch `RESTORE`
    - "Close Pane" → dispatch `CLOSE_APP` with focused pane
    - "Undo" → dispatch `LAYOUT_UNDO`
    - "Redo" → dispatch `LAYOUT_REDO`
  - **Spawn actions (from APP_REGISTRY):**
    - "Spawn Terminal" → dispatch `SPAWN_APP` with appType: 'terminal'
    - "Spawn Text Pane" → dispatch `SPAWN_APP` with appType: 'text-pane'
    - "Spawn Tree Browser" → dispatch `SPAWN_APP` with appType: 'tree-browser'
    - (More as appropriate from APP_REGISTRY, filter to category: 'primitive' or 'applet')
- Input field at top for search (autofocus when opened)
- Fuzzy filter as user types (use simple `.toLowerCase().includes()` or install a fuzzy lib if needed)
- Arrow keys navigate, Enter executes selected command, Escape closes
- Styled with `var(--sd-*)` variables only (Rule 3)
- Modal backdrop with `onClick={onClose}`

#### Shell.tsx Integration
- Add state: `const [showCommandPalette, setShowCommandPalette] = useState(false)`
- In global keydown listener, add `Ctrl+Shift+P` handler → `setShowCommandPalette(true)`
- Render `{showCommandPalette && <CommandPalette isOpen={showCommandPalette} onClose={() => setShowCommandPalette(false)} />}`

**Acceptance Criteria:**
- [ ] Ctrl+Shift+P opens command palette
- [ ] Command palette shows searchable list of shell actions
- [ ] Typing filters commands (case-insensitive)
- [ ] Arrow keys navigate, Enter executes, Escape closes
- [ ] All styles use `var(--sd-*)` only (no hardcoded colors)
- [ ] Modal is centered and styled consistently with existing modals
- [ ] Commands execute correctly (split, maximize, close, spawn, undo, redo)

---

### 4. Update ShortcutsPopup

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShortcutsPopup.tsx`

**Requirements:**
- ShortcutsPopup takes a `features` prop with shortcuts
- Currently used by applets (kanban, etc.) to display shortcuts
- Shell should pass new shortcuts to any component that renders ShortcutsPopup
- Or: create a shell-specific shortcuts list in MenuBar or Shell.tsx

**Note:** ShortcutsPopup is already generic. You just need to ensure the new shortcuts are passed to it or displayed somewhere. If MenuBar has a "Help → Keyboard Shortcuts" menu item, make sure it shows the new shortcuts.

**Acceptance Criteria:**
- [ ] New shortcuts (Escape, Ctrl+Z, Ctrl+Shift+Z, Ctrl+Shift+P) appear in help documentation or shortcuts popup
- [ ] Shortcuts are clearly labeled with descriptions

---

## Test Requirements

### Files to create:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\CommandPalette.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\globalKeyboardShortcuts.test.tsx`

### Test scenarios:

#### CommandPalette.test.tsx (minimum 8 tests)
1. Renders when `isOpen={true}`
2. Does not render when `isOpen={false}`
3. Shows all commands on initial render
4. Filters commands when user types in search input
5. Arrow down selects next command
6. Arrow up selects previous command
7. Enter key executes selected command (verify dispatch called)
8. Escape key calls `onClose`

#### globalKeyboardShortcuts.test.tsx (minimum 10 tests)
1. Escape closes modal if modal is open
2. Escape restores maximized pane if no modal open
3. Escape closes menu if no modal/maximized pane
4. Escape does not trigger if focus is in input field
5. Ctrl+Z dispatches LAYOUT_UNDO
6. Ctrl+Z does not trigger if focus is in textarea
7. Ctrl+Shift+Z dispatches LAYOUT_REDO
8. Ctrl+Shift+P opens command palette
9. Ctrl+Shift+P does not open palette if already open
10. Global keyboard shortcuts do not interfere with each other

**Run tests:**
```bash
cd browser && npx vitest run src/shell/components/__tests__/CommandPalette.test.tsx
cd browser && npx vitest run src/shell/components/__tests__/globalKeyboardShortcuts.test.tsx
```

---

## Constraints (10 Hard Rules)

- **Rule 3:** CSS uses `var(--sd-*)` only. No hex, rgb(), or named colors.
- **Rule 4:** No file over 500 lines. CommandPalette.tsx should be ~200 lines max.
- **Rule 5:** TDD. Tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 10:** NO GIT OPERATIONS. No commits, no push.

---

## File Size Constraint

After implementation, verify:
- Shell.tsx remains under 500 lines (currently ~100 lines, adding ~50 lines for keyboard handlers = ~150 total)
- CommandPalette.tsx under 500 lines (target: ~200 lines)

If CommandPalette.tsx approaches 300 lines, consider extracting fuzzy filter logic or command list to a separate file.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-240-RESPONSE.md`

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

---

## Expected Outcome

After this task:
- Escape key provides a smart, progressive dismiss protocol (modals → maximized → menus)
- Ctrl+Z/Ctrl+Shift+Z provide undo/redo for shell layout actions
- Ctrl+Shift+P opens a searchable command palette with all shell actions
- All shortcuts are documented in help/shortcuts popup
- All tests pass (18+ new tests)
- No hardcoded colors, all files under 500 lines

---

END OF TASK FILE
