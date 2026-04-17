# TASK-BUG-074: Remove Layout Submenu from View Menu

## Objective

Remove the vestigial Layout submenu from the View menu in MenuBar.tsx. Layout is determined by EGG config files, not user menu selection. This is leftover UI from the old simdecisions-2 port that no longer applies to ShiftCenter architecture.

## Context

The MenuBar.tsx component currently includes a "Layout" submenu under the View menu with 8 preset options (Single Pane, Horizontal Split, Vertical Split, etc.). These presets were used in the old system where users manually switched layouts via menu.

In ShiftCenter, layouts are determined by EGG files (e.g., `canvas.egg.md`, `efemera.egg.md`), not by user menu selection. Users load different EGG configs to get different layouts — they do not change layouts via menu presets.

The Layout submenu and its handler function need to be removed entirely.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (lines 223-226 and 393-446)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (lines 157-181)

## Deliverables

- [ ] **Remove `handleLayoutChange` function** (lines 223-226 in MenuBar.tsx)
- [ ] **Remove Layout submenu JSX** (lines 393-446 in MenuBar.tsx — the entire div.menu-dropdown-item.submenu for Layout)
- [ ] **Update MenuBar.test.tsx** — remove tests at lines 157-181 (both layout-related test cases)
- [ ] **Verify View menu still works** — Theme submenu and syndicated menu groups remain functional
- [ ] **All tests pass** — no regressions in MenuBar or other components

## Test Requirements

- [ ] **TDD:** Update tests FIRST, then implementation
- [ ] Run `cd browser && npx vitest run src/shell/components/__tests__\MenuBar.test.tsx` — all tests pass
- [ ] Run `cd browser && npx vitest run` — no regressions elsewhere
- [ ] Verify manually (if possible): View menu opens, Theme submenu works, Layout is gone

## Edge Cases to Verify

- [ ] View menu still opens and closes correctly
- [ ] Theme submenu still renders and functions
- [ ] Syndicated menu groups in View menu still render
- [ ] Keyboard shortcut Alt+V still opens View menu
- [ ] Menu hover behavior (switching from File → View) still works

## Constraints

- No file over 500 lines (MenuBar.tsx is currently 655 lines, will drop to ~607 after deletion)
- CSS: var(--sd-*) only (not applicable here — this is deletion only)
- No stubs (not applicable — removing code, not adding)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BUG-074-RESPONSE.md`

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
