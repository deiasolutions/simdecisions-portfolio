# BRIEFING: Fix SpotlightOverlay Test Failures (WAVE0-07)

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-15-WAVE0-07)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Priority:** P0.020
**Model Assignment:** haiku

---

## Objective

Fix 3 test failures in `browser/src/shell/components/__tests__/SpotlightOverlay.test.tsx`. All failures indicate the `data-spotlight-overlay` selector is returning null. The component may have changed its DOM structure or selector.

---

## Context from Q88N

This is part of WAVE0 cleanup. Three tests are failing:
1. "renders overlay with children" - Cannot fire click event on null backdrop
2. "calls onClose when backdrop clicked" - Cannot fire click event on null backdrop
3. "centers modal in viewport" - Cannot read properties of null (reading 'style')

The root cause: `data-spotlight-overlay` selector returns null. The component structure may have changed.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx`

---

## Acceptance Criteria

- [ ] Update test selectors to match current SpotlightOverlay component structure
- [ ] All 3 failing tests pass
- [ ] No new test failures introduced
- [ ] Test assertions verify the correct behavior (backdrop rendering, click handling, centering)

---

## Constraints

- **TDD:** Tests must verify actual component behavior
- **No stubs**
- **Max 500 lines per file**
- **Fix tests to match component reality** — do not change component to match old tests unless component is actually broken

---

## Smoke Test

- [ ] `cd browser && npx vitest run src/shell/components/__tests__/SpotlightOverlay.test.tsx` passes all tests
- [ ] No regressions in other shell tests

---

## Instructions for Q33N

1. Read the test file and component file
2. Identify what selector the component actually uses
3. Write a single task file for a bee to fix the test selectors
4. Return the task file for Q33NR review
5. DO NOT dispatch the bee yet — wait for Q33NR approval
