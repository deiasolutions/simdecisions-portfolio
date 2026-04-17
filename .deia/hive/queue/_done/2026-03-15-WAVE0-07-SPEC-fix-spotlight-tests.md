# WAVE0-07: Fix SpotlightOverlay Test Failures

## Priority
P0.020

## Model Assignment
haiku

## Objective
Fix 3 test failures in `browser/src/shell/components/__tests__/SpotlightOverlay.test.tsx`:
1. "renders overlay with children" - Cannot fire click event on null backdrop
2. "calls onClose when backdrop clicked" - Cannot fire click event on null backdrop
3. "centers modal in viewport" - Cannot read properties of null (reading 'style')

All failures indicate the `data-spotlight-overlay` selector is returning null. The component may have changed its DOM structure or selector.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx`

## Acceptance Criteria
- [ ] Update test selectors to match current SpotlightOverlay component structure
- [ ] All 3 failing tests pass
- [ ] No new test failures introduced
- [ ] Test assertions verify the correct behavior (backdrop rendering, click handling, centering)

## Constraints
- TDD: Tests must verify actual component behavior
- No stubs
- Max 500 lines per file
- Fix tests to match component reality — do not change component to match old tests unless component is actually broken

## Smoke Test
- [ ] `cd browser && npx vitest run src/shell/components/__tests__/SpotlightOverlay.test.tsx` passes all tests
- [ ] No regressions in other shell tests
