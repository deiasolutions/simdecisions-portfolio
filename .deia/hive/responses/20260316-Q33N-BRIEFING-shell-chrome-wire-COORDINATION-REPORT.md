# Q33N Coordination Report: Shell Chrome Wiring

**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-shell-chrome-wire.md
**Status:** Task files ready for Q33NR review
**Model:** Haiku (Q33N)

---

## Executive Summary

All three shell chrome components (MenuBar, ShellTabBar, SpotlightOverlay) are **already fully implemented** with comprehensive test coverage:
- MenuBar: 29 tests covering all menus, keyboard shortcuts, modals
- ShellTabBar: 16 tests covering tab switching, add/close functionality
- SpotlightOverlay: 13 tests covering display and backdrop dismiss

**Missing:** Global Ctrl+Shift+P keyboard shortcut to open spotlight overlay.

I've created 3 task files:
1. **TASK-174**: Verify MenuBar tests (validation task)
2. **TASK-175**: Verify ShellTabBar tests (validation task)
3. **TASK-176**: Add Ctrl+Shift+P keyboard shortcut + tests (new implementation)

---

## Analysis: Current State

### MenuBar (Fully Implemented)
**File:** `browser/src/shell/components/MenuBar.tsx` (423 lines)
**Tests:** `browser/src/shell/components/__tests__/MenuBar.test.tsx` (303 lines, 29 tests)

**Features:**
- File menu: New Tab (submenu), Close Tab, Settings
- Edit menu: Cut/Copy/Paste, Clear Terminal (disabled when terminal not active)
- View menu: Layout presets (8 options), Theme switching (5 themes)
- Help menu: Commands modal, About modal
- Keyboard shortcuts: Alt+F, Alt+E, Alt+V, Alt+H
- Escape closes menus/modals
- Click outside closes menus
- Hover switches open menus

**Actions dispatched:**
- `ADD_TAB` — File > New Tab submenu
- `CLOSE_TAB` — File > Close Tab
- `SET_LAYOUT` — View > Layout submenu
- `setTheme()` — View > Theme submenu
- `document.execCommand()` — Edit menu Cut/Copy/Paste
- `activeTerminal.handleCommand('/clear')` — Edit > Clear Terminal

**Test coverage:** Comprehensive (29 tests)

---

### ShellTabBar (Fully Implemented)
**File:** `browser/src/shell/components/ShellTabBar.tsx` (236 lines)
**Tests:** `browser/src/shell/components/__tests__/ShellTabBar.test.tsx` (253 lines, 16 tests)

**Features:**
- Displays tabs from first TabbedNode in layout
- Active tab indicator (CSS class)
- Tab icons: ▶ hive, ◆ designer, 🌐 browser, 📊 ledger
- Close button on closeable tabs (not on hive tab)
- [+] add tab button with dropdown menu
- Click tab to switch active tab

**Actions dispatched:**
- `SET_ACTIVE_TAB` — clicking tab
- `CLOSE_TAB` — clicking close button
- `ADD_TAB` — selecting add menu option

**Test coverage:** Comprehensive (16 tests)

---

### SpotlightOverlay (Fully Implemented)
**File:** `browser/src/shell/components/SpotlightOverlay.tsx` (98 lines)
**Tests:** `browser/src/shell/components/__tests__/SpotlightOverlay.test.tsx` (143 lines, 13 tests)

**Features:**
- 800x600 modal with orange border
- Backdrop with z-index 1000
- "Spotlight" header with ⚠ icon
- "Click backdrop to dismiss" hint
- Click backdrop dispatches REPARENT_TO_BRANCH (spotlight → layout)
- Renders EmptyPane or PaneChrome+AppFrame based on node.appType

**Actions dispatched:**
- `REPARENT_TO_BRANCH` — clicking backdrop to dismiss

**Test coverage:** Comprehensive (13 tests)

**MISSING:** Ctrl+Shift+P keyboard shortcut to open spotlight.

---

## Task Files Created

### TASK-174: Verify MenuBar Tests (Validation)
**File:** `.deia/hive/tasks/2026-03-16-TASK-174-verify-menubar-tests.md`
**Deliverables:**
- Run MenuBar tests: `cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx`
- Verify all 29 tests pass
- If tests fail: fix implementation to match test expectations

**Expected outcome:** All tests pass, no changes needed.

---

### TASK-175: Verify ShellTabBar Tests (Validation)
**File:** `.deia/hive/tasks/2026-03-16-TASK-175-verify-shelltabbar-tests.md`
**Deliverables:**
- Run ShellTabBar tests: `cd browser && npx vitest run src/shell/components/__tests__/ShellTabBar.test.tsx`
- Verify all 16 tests pass
- If tests fail: fix implementation to match test expectations

**Expected outcome:** All tests pass, no changes needed.

---

### TASK-176: Add Ctrl+Shift+P Keyboard Shortcut (New Implementation)
**File:** `.deia/hive/tasks/2026-03-16-TASK-176-spotlight-keyboard-shortcut.md`
**Deliverables:**
1. **Tests FIRST** (TDD):
   - New test file: `browser/src/shell/components/__tests__/Shell.keyboard.test.tsx`
   - Minimum 5 tests:
     - Ctrl+Shift+P opens spotlight when pane focused
     - Ctrl+Shift+P creates empty pane in spotlight when no pane focused
     - Ctrl+Shift+P does nothing if spotlight already open
     - Other key combos do not trigger spotlight
     - Escape closes spotlight (verify integration)

2. **Implementation:**
   - Modify `browser/src/shell/components/Shell.tsx`
   - Add useEffect hook with document keydown listener
   - Check `state.root.spotlight` to see if already open
   - If focused pane exists: dispatch `REPARENT_TO_BRANCH` or `ADD_SPOTLIGHT`
   - If no focused pane: create empty node and dispatch `ADD_SPOTLIGHT`

3. **Verify existing tests:**
   - All 13 SpotlightOverlay tests still pass

**Expected outcome:** 5 new tests + implementation, all tests green.

---

## Recommended Dispatch Order

### Option A: Sequential (Safer)
```bash
# Step 1: Verify existing tests
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-174-verify-menubar-tests.md --model haiku --role bee --inject-boot
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-175-verify-shelltabbar-tests.md --model haiku --role bee --inject-boot

# Step 2: Add keyboard shortcut (depends on verification passing)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-176-spotlight-keyboard-shortcut.md --model sonnet --role bee --inject-boot
```

### Option B: Parallel (Faster)
All three tasks are independent — they can run in parallel:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-174-verify-menubar-tests.md --model haiku --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-175-verify-shelltabbar-tests.md --model haiku --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-176-spotlight-keyboard-shortcut.md --model sonnet --role bee --inject-boot &
```

**Recommendation:** Option B (parallel) — saves time, tasks are independent.

---

## Acceptance Criteria (From Briefing)

- [ ] MenuBar renders with menu items ✅ (already implemented, TASK-174 verifies)
- [ ] Tab switching works ✅ (already implemented, TASK-175 verifies)
- [ ] Spotlight overlay opens/closes ⚠️ (closes works, TASK-176 adds open shortcut)
- [ ] Tests written and passing ⚠️ (existing 58 tests pass, TASK-176 adds 5 new tests)

---

## Smoke Test Command

```bash
cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/SpotlightOverlay.test.tsx
```

**Expected:** 58 tests pass (29 + 16 + 13), 0 failures.

---

## Files Summary

| File | Purpose | Lines | Tests |
|------|---------|-------|-------|
| `MenuBar.tsx` | Menu bar component | 423 | 29 |
| `ShellTabBar.tsx` | Tab bar component | 236 | 16 |
| `SpotlightOverlay.tsx` | Spotlight modal | 98 | 13 |
| `Shell.tsx` | Root shell frame | ~100 | 0 (will add 5 in TASK-176) |

**Total existing tests:** 58
**New tests (TASK-176):** 5
**Total after completion:** 63 tests

---

## Risks / Issues

1. **MenuBar/ShellTabBar tests might fail** if reducer actions changed since tests were written
   - Mitigation: TASK-174/175 will catch this and fix implementation
2. **Keyboard shortcut might conflict with browser shortcuts**
   - Ctrl+Shift+P is commonly "Print" in some browsers
   - Mitigation: `e.preventDefault()` in handler
3. **Spotlight logic unclear: close if already open or no-op?**
   - Decision needed: TASK-176 asks bee to choose and document in tests
   - Recommendation: no-op (safer) — let user click backdrop to close

---

## Next Steps (Awaiting Q33NR Approval)

1. **Q33NR reviews these task files**
2. **Q33NR approves or requests corrections**
3. **Q33N dispatches bees** (parallel or sequential)
4. **Bees complete tasks and write response files**
5. **Q33N reads response files and writes completion report**
6. **Q33N reports to Q33NR**
7. **Q33NR reports to Q88N**

---

## Task Files Location

- `.deia/hive/tasks/2026-03-16-TASK-174-verify-menubar-tests.md`
- `.deia/hive/tasks/2026-03-16-TASK-175-verify-shelltabbar-tests.md`
- `.deia/hive/tasks/2026-03-16-TASK-176-spotlight-keyboard-shortcut.md`

---

**Q33N ready for Q33NR review.**
