# TASK-174: Verify MenuBar component tests and functionality

## Objective
Verify that all MenuBar component tests pass and all menu actions work correctly with the shell reducer.

## Context

MenuBar component is already fully implemented with:
- File | Edit | View | Help menus
- Keyboard shortcuts: Alt+F, Alt+E, Alt+V, Alt+H
- 29 existing tests covering all menu items and actions
- Actions dispatch to shell reducer (ADD_TAB, SET_LAYOUT, CLOSE_TAB, etc.)

**This task verifies existing functionality — no new code required unless tests fail.**

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`

## Deliverables

- [ ] Run MenuBar tests: `cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx`
- [ ] Verify all 29 tests pass
- [ ] If any tests fail: fix the implementation to match the test expectations
- [ ] Verify menu actions dispatch correct reducer actions:
  - File > New Tab submenu dispatches ADD_TAB
  - File > Close Tab dispatches CLOSE_TAB
  - View > Layout submenu dispatches SET_LAYOUT
  - View > Theme submenu calls setTheme()
  - Edit menu Cut/Copy/Paste work (document.execCommand)
  - Edit > Clear Terminal calls activeTerminal.handleCommand('/clear')
  - Help > Commands opens modal
  - Help > About opens modal

## Test Requirements

- [ ] All existing 29 tests pass
- [ ] No new tests required (comprehensive coverage already exists)
- [ ] Edge cases already covered:
  - Keyboard shortcuts (Alt+F/E/V/H)
  - Escape closes menus/modals
  - Click outside closes menus
  - Hover switches open menus
  - Disabled states when terminal not active
  - Modal backdrop click dismisses modal

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (already compliant)
- No stubs (already fully implemented)
- TDD: tests already written

## Acceptance Criteria

- [ ] All 29 MenuBar tests pass
- [ ] No console errors during test run
- [ ] No implementation changes needed (tests validate existing code works)
- [ ] If fixes needed: implementation matches test expectations exactly

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-174-RESPONSE.md`

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
