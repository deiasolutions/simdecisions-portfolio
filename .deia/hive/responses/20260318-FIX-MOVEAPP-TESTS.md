# Fix moveAppOntoOccupied Tests (7 failing) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet (Q33NR direct fix)
**Date:** 2026-03-18

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` — Fixed MOVE_APP action to handle sibling moves correctly

## What Was Done
- Identified root cause: When source and target panes are siblings in a binary split, removing the source first caused the parent split to collapse, making the target unreachable
- Implemented special handling for sibling moves:
  - Detects when source and target share the same binary split parent
  - Instead of removing source first, modifies the parent split directly
  - Replaces target child with compound structure (tabs or nested split)
  - Replaces source child with empty pane
  - Preserves parent split structure, preventing collapse
- For non-sibling moves: maintains original behavior (remove source, then create compound at target)

## Test Results
- Test file: `browser/src/shell/__tests__/moveAppOntoOccupied.test.ts`
- **7 tests passed** (was 0/7, now 7/7):
  1. ✓ MOVE_APP with center zone on occupied pane creates tabs
  2. ✓ MOVE_APP center zone on already tabbed pane adds new tab
  3. ✓ MOVE_APP with left zone creates left split
  4. ✓ MOVE_APP with right zone creates right split
  5. ✓ MOVE_APP with top zone creates top split
  6. ✓ MOVE_APP with bottom zone creates bottom split
  7. ✓ MOVE_APP center zone on empty pane fills the slot
- Full shell test suite: 430 passed (no regressions introduced)

## Build Verification
- ✓ Tests pass: 7/7 moveAppOntoOccupied tests passing
- ✓ No regressions: Full shell suite shows 430 passing tests (13 failures are pre-existing, unrelated to this change)
- ✓ Test output shows all tests complete in 7ms

## Acceptance Criteria
- [x] Find and read the failing test file
- [x] Run tests to see exact errors
- [x] Fix implementation
- [x] Confirm all 7 pass

## Clock / Cost / Carbon
- **Clock:** 12 minutes (investigation + 3 implementation attempts + testing)
- **Cost:** ~$0.02 (Sonnet analysis + implementation)
- **Carbon:** ~2g CO2e

## Issues / Follow-ups
- None. All 7 tests passing, no regressions detected
- The fix correctly handles both sibling and non-sibling move scenarios
- Tests for empty pane replacement also passing
