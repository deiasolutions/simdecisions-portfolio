# TASK-BUG-036: Build Monitor Tree Layout Fix -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-18

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`

## What Was Done

- **mapActiveBees() function:** Moved detail information (model, elapsed time, cost) from child node to main label. Last message still appears as optional child when present. Removed detail child node.
- **mapCompletedTasks() function:** Moved detail information (time, duration, cost) from child node to main label. Removed all children (set to empty array).
- **Test Updates:** Updated 3 mapActiveBees tests to verify detail in label and children structure. Updated 5 mapCompletedTasks tests to verify detail in label and empty children.

## Test Results

- Test file: `src/primitives/tree-browser/adapters/__tests__/buildStatusMapper.test.ts`
- **38 tests passed** (10 mapActiveBees, 6 mapRunnerQueue, 16 mapBuildLog, 6 mapCompletedTasks)
- 0 tests failed
- Duration: 35ms

## Build Verification

✅ All tests pass.

```
 ✓ src/primitives/tree-browser/adapters/__tests__/buildStatusMapper.test.ts (38 tests) 35ms

 Test Files  1 passed (1)
      Tests  38 passed (38)
   Duration  3.67s
```

## Acceptance Criteria

- [x] Active bee detail (model, elapsed, cost) appears in label, not as child
- [x] Active bee lastMsg still appears as child (when present)
- [x] Completed task detail (time, duration, cost) appears in label, no children
- [x] All tests updated and passing
- [x] No hardcoded colors
- [x] No files over 500 lines
- [x] Response file written

## Clock / Cost / Carbon

- **Clock:** 133.3s (2.2 minutes)
- **Cost:** $1.12 USD
- **Carbon:** ~0.45 g CO2e (estimated)

## Issues / Follow-ups

None. All deliverables complete. Build monitor tree layout now shows details inline in the label, reducing vertical space and eliminating unnecessary child nodes.
