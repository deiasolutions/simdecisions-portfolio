# TASK-133: Fix SpotlightOverlay Test Selectors -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-15

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx` (modified, 3 selectors updated)

## What Was Done

- **Line 56:** Updated test `'renders backdrop with z-index 1000'` to use `screen.getByTestId('spotlight-overlay')` instead of `container.querySelector('[data-spotlight-overlay]')`
- **Line 83:** Updated test `'dispatches REPARENT_TO_BRANCH when clicking backdrop'` to use `screen.getByTestId('spotlight-overlay')` instead of `container.querySelector('[data-spotlight-overlay]')`
- **Line 137:** Updated test `'centers modal in viewport'` to use `screen.getByTestId('spotlight-overlay')` instead of `container.querySelector('[data-spotlight-overlay]')`
- Removed unused `{ container }` destructuring from the three affected test functions since `screen.getByTestId()` is now used instead of `container.querySelector()`
- All selectors now correctly match the component's `data-testid="spotlight-overlay"` attribute on line 36 of `SpotlightOverlay.tsx`

## Test Results

**Test File:** `src/shell/components/__tests__/SpotlightOverlay.test.tsx`

```
✓ 11 tests passed
  - renders spotlight modal with 800x600 size ✓
  - has orange border ✓
  - renders backdrop with z-index 1000 ✓ (FIXED)
  - renders "Spotlight" header with ⚠ icon ✓
  - renders "Click backdrop to dismiss" hint ✓
  - dispatches REPARENT_TO_BRANCH when clicking backdrop ✓ (FIXED)
  - does not dispatch when clicking inside modal ✓
  - renders EmptyPane when node is empty ✓
  - renders PaneChrome + AppFrame when node is occupied ✓
  - sets data-load-state attribute from node ✓
  - centers modal in viewport ✓ (FIXED)
```

## Build Verification

```
Test Files: 1 passed (1)
Tests:      11 passed (11)
Duration:   107ms
Status:     All tests passing
```

## Acceptance Criteria

- [x] Update line 56 in SpotlightOverlay.test.tsx: change selector from `container.querySelector('[data-spotlight-overlay]')` to `screen.getByTestId('spotlight-overlay')`
- [x] Update line 83: same fix for backdrop click test
- [x] Update line 137: same fix for centering test
- [x] All 3 currently-failing tests pass
- [x] All other tests remain passing (11 total tests in the file)
- [x] No new tests needed — fixing existing tests only
- [x] Run: `cd browser && npx vitest run src/shell/components/__tests__/SpotlightOverlay.test.tsx`
- [x] All 11 tests must pass with 0 failures

## Clock / Cost / Carbon

**Clock:** 8 minutes (2026-03-15 03:23–03:31)
**Cost:** ~1,200 tokens (read component + test file, 3 edits, 1 test run)
**Carbon:** ~0.12g CO₂ equivalent (small edits + fast test run)

## Issues / Follow-ups

**None.** Task complete with no edge cases or dependencies. The component (`SpotlightOverlay.tsx`) is correct and unchanged. All tests verify actual component behavior:
- Backdrop click dispatches REPARENT_TO_BRANCH action
- Z-index and centering styles are correctly applied
- Modal doesn't propagate click events to backdrop
