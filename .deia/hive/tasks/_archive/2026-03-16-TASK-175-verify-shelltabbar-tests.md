# TASK-175: Verify ShellTabBar component tests and functionality

## Objective
Verify that all ShellTabBar component tests pass and tab switching works correctly with the shell reducer.

## Context

ShellTabBar component is already fully implemented with:
- Tab display from first TabbedNode in layout
- Active tab indicator
- Close button on closeable tabs (not on hive tab)
- [+] add tab button with menu
- 16 existing tests covering all tab actions

**This task verifies existing functionality — no new code required unless tests fail.**

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ShellTabBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`

## Deliverables

- [ ] Run ShellTabBar tests: `cd browser && npx vitest run src/shell/components/__tests__/ShellTabBar.test.tsx`
- [ ] Verify all 16 tests pass
- [ ] If any tests fail: fix the implementation to match the test expectations
- [ ] Verify tab actions dispatch correct reducer actions:
  - Clicking tab dispatches SET_ACTIVE_TAB with correct tabbedNodeId and index
  - Clicking close button dispatches CLOSE_TAB
  - Clicking [+] button opens add menu
  - Selecting add menu option dispatches ADD_TAB
- [ ] Verify tab icons render correctly:
  - hive: ▶
  - designer: ◆
  - browser: 🌐
  - ledger: 📊

## Test Requirements

- [ ] All existing 16 tests pass
- [ ] No new tests required (comprehensive coverage already exists)
- [ ] Edge cases already covered:
  - Empty tab bar (no tabs)
  - Active tab indicator
  - Close button only on closeable tabs
  - Close button click doesn't trigger tab click
  - Add menu opens/closes
  - Tab icons for each type

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (already compliant)
- No stubs (already fully implemented)
- TDD: tests already written

## Acceptance Criteria

- [ ] All 16 ShellTabBar tests pass
- [ ] No console errors during test run
- [ ] No implementation changes needed (tests validate existing code works)
- [ ] If fixes needed: implementation matches test expectations exactly

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-175-RESPONSE.md`

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
