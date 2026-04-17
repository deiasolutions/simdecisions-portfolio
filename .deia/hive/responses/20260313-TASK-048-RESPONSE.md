# TASK-048: Theme Switching Infrastructure -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\volumeStorage.test.ts` (10 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ThemePicker.test.tsx` (5 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ThemePicker.tsx` (58 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\theme-picker.css` (80 lines)

### Replaced
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\volumeStorage.ts` (135 lines, was 21-line stub)

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\index.ts` (exports updated)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\lifecycle.ts` (removed DI pattern, direct function import)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (theme state + ThemePicker)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\Shell.test.tsx` (5 new theme tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` (ShellContextValue interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css` (ThemePicker positioning)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (body background fix)

## What Was Done

### volumeStorage (Step 1-3)
- Ported full implementation from platform (6 functions: readVolume, writeVolume, deleteVolume, hasVolume, listVolumes, migrateKey)
- Volume path format: `local://shell/theme` → localStorage key `sd:volume:shell/theme`
- Removed old DI pattern (setVolumeStorage/getVolumeStorage)
- Updated index.ts exports to export functions directly
- Updated lifecycle.ts to use direct imports instead of DI pattern
- 10 tests (all passing)

### Shell theme state (Step 4-5)
- Added theme state to Shell.tsx with localStorage persistence via volumeStorage
- Migrates old `sd:shell_theme` key to `local://shell/theme` on first load
- Applies `data-theme` attribute to `.hhp-root` (undefined for 'full-color', theme name for others)
- Added theme and setTheme to ShellContextValue interface
- Included in context value passed to ShellCtx.Provider
- 5 new tests in Shell.test.tsx (all passing)

### ThemePicker component (Step 6-8)
- Dropdown variant with 5 theme options (THEMES constant)
- Click-outside-to-close behavior via useEffect + useRef
- Shows icon for current theme on trigger button
- Menu displays theme icon + label, checkmark for active theme
- Positioned bottom-right (8px from edges) via shell.css
- All colors via CSS variables (var(--sd-*))
- 5 tests (all passing)

### Body background fix (Step 9)
- Added `background: var(--sd-bg);` to `.hhp-root` in shell-themes.css
- Keeps hardcoded `background: #0e0a1a` on body as fallback before React mounts

## Test Results

**New tests:** 20 total (10 volumeStorage + 5 Shell + 5 ThemePicker)
**Browser suite:** 1201 passed, 1 failed (pre-existing ProgressPane test unrelated to this task)
**Python suite:** 971 passed, 6 failed (pre-existing smoke tests), 27 errors (E2E timeouts, pre-existing)

All new tests passing. No regressions introduced.

## Line Count Compliance

- volumeStorage.ts: 135 lines (constraint: under 150) ✓
- ThemePicker.tsx: 58 lines (constraint: under 80) ✓
- theme-picker.css: 80 lines (constraint: under 100) ✓

## Manual Testing Checklist

- [ ] Theme persists across page reload (verify in localStorage as `sd:volume:shell/theme`)
- [ ] ThemePicker dropdown opens/closes correctly
- [ ] Clicking theme changes CSS variables visibly (check body background, text colors)
- [ ] Migration from old `sd:shell_theme` key works on first load
- [ ] ThemePicker positioned correctly (bottom-right corner)

## Definition of Done

- [x] volumeStorage.ts replaced with full implementation (6 functions exported)
- [x] lifecycle.ts updated to use new volumeStorage API
- [x] Shell.tsx has theme state + persistence + data-theme attribute
- [x] ShellContextValue has theme and setTheme fields
- [x] ThemePicker component renders and changes theme
- [x] ThemePicker CSS uses only CSS variables
- [x] Body background fix applied to .hhp-root
- [x] All 20 tests pass
- [ ] Manual test: theme persists across page reload
- [ ] Manual test: ThemePicker dropdown opens/closes correctly
- [ ] Manual test: clicking theme changes CSS variables visibly

**Task complete. Ready for manual testing and integration.**
