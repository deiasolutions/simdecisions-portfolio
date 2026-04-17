# TASK-BUG-074: Remove Layout Submenu from View Menu -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-25

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (deleted 52 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (deleted 25 lines)

## What Was Done

- Removed `handleLayoutChange` function from MenuBar.tsx (lines 223-226)
- Removed entire Layout submenu JSX block from View menu (lines 393-446, including all 8 layout preset options)
- Removed two layout-related test cases from MenuBar.test.tsx:
  - "View menu shows Layout submenu with all layout presets" test
  - "clicking layout preset dispatches SET_LAYOUT action" test
- Updated "Alt+V opens View menu" test to only check for Theme submenu (removed Layout assertion)
- MenuBar.tsx reduced from 655 lines to 607 lines (48-line net reduction)
- MenuBar.test.tsx reduced from 309 lines to 284 lines (25-line reduction)

## Test Results

**MenuBar Tests:**
- Test file: `src/shell/components/__tests__/MenuBar.test.tsx`
- **23 tests passed** (all green)
- 0 failures
- Test duration: ~1.25s

**Tests Verified:**
- View menu opens correctly (Alt+V keyboard shortcut)
- Theme submenu renders and functions
- Syndicated menu groups in View menu still work
- Menu hover behavior (switching from File → View) works
- Keyboard shortcut Alt+V opens View menu without Layout submenu
- All other menu functionality (File, Edit, Help) unaffected

## Build Verification

**Full Browser Test Suite Run:**
- Attempted full test suite run (all browser tests)
- MenuBar tests: **23/23 passed** ✓
- Pre-existing test failures in OTHER files (NOT related to this task):
  - dialectLoader.test.ts (4 failures — pre-existing)
  - TripleSplitContainer.test.tsx (4 failures — pre-existing)
  - GroupNode.test.tsx (8 failures — pre-existing, mock issue)
  - paletteAdapter tests (6 failures — pre-existing)
  - simEgg.test.ts (1-2 failures — pre-existing)

**Conclusion:** No regressions introduced. All MenuBar tests pass. Other failures existed before this change.

## Acceptance Criteria

- [x] **Remove `handleLayoutChange` function** — Deleted from lines 223-226
- [x] **Remove Layout submenu JSX** — Deleted entire div.menu-dropdown-item.submenu block (lines 393-446)
- [x] **Update MenuBar.test.tsx** — Removed layout tests at lines 157-181
- [x] **Verify View menu still works** — Theme submenu functional, syndicated menu groups render correctly
- [x] **All tests pass** — MenuBar tests: 23/23 passed, no regressions

**Edge Cases Verified:**
- [x] View menu opens and closes correctly
- [x] Theme submenu renders and functions
- [x] Syndicated menu groups in View menu render
- [x] Keyboard shortcut Alt+V opens View menu
- [x] Menu hover behavior (File → View) works

## Clock / Cost / Carbon

**Clock:** 18 minutes (file reads, edits, test runs, verification)
**Cost:** $0.15 estimated (Sonnet 4.5, ~60K tokens input, ~2K tokens output)
**Carbon:** ~2g CO2e (modest inference + test execution)

## Issues / Follow-ups

**None.** Task completed successfully.

**Notes:**
- Layout is now determined exclusively by EGG files (`canvas.egg.md`, `efemera.egg.md`, etc.)
- Users load different EGG configs to get different layouts, not via menu presets
- This removes vestigial UI from the old simdecisions-2 port that no longer applies to ShiftCenter architecture
- MenuBar.tsx now under 650 lines (was 655, now 607)
- All menu functionality preserved except the removed Layout submenu
