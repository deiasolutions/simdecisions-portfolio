# TASK-133: Fix SpotlightOverlay Test Selectors

## Objective
Fix 3 failing tests in `SpotlightOverlay.test.tsx` by updating test selectors to match current component DOM structure.

## Context
The component (`SpotlightOverlay.tsx`) uses `data-testid="spotlight-overlay"` for the backdrop element, but the tests query for `data-spotlight-overlay` (without the "testid" part). This causes querySelector to return null, leading to failures when attempting to fire click events or read style properties.

The component itself is correct — it uses the standard `data-testid` attribute pattern from @testing-library/react. The tests need to be updated to use the correct selector method.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx` (failing tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx` (component source — verify `data-testid="spotlight-overlay"` on line 36)

## Deliverables
- [ ] Update line 56 in SpotlightOverlay.test.tsx: change `container.querySelector('[data-spotlight-overlay]')` to use `screen.getByTestId('spotlight-overlay')`
- [ ] Update line 83: same fix for backdrop click test
- [ ] Update line 137: same fix for centering test
- [ ] All 3 currently-failing tests pass
- [ ] All other tests remain passing (11 total tests in the file)

## Test Requirements
- [ ] No new tests needed — fixing existing tests only
- [ ] Run: `cd browser && npx vitest run src/shell/components/__tests__/SpotlightOverlay.test.tsx`
- [ ] All 11 tests must pass with 0 failures
- [ ] Edge cases: ensure tests verify correct behavior (backdrop click dispatches REPARENT_TO_BRANCH, centering styles are correct)

## Constraints
- No file over 500 lines (test file is currently 144 lines — no risk)
- Do NOT modify the component (`SpotlightOverlay.tsx`) — it's correct
- Do NOT change other tests that are already passing
- Use `screen.getByTestId('spotlight-overlay')` from @testing-library/react instead of querySelector
- TDD: Tests must verify actual component behavior

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-133-RESPONSE.md`

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
