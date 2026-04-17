# 2026-03-27-TASK-FIX-MULTI-CHILD-SPLIT: Fix N-Child Split Support in eggToShell.ts -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-27

## Files Modified

- `browser/src/eggs/types.ts` (line 27: updated `ratio` type)
- `browser/src/shell/eggToShell.ts` (added 3 helpers + updated split handler)
- `browser/src/shell/__tests__/eggToShell.multiChild.test.ts` (new file, 16 tests)

## What Was Done

1. **Type Update (types.ts)**
   - Changed `EggLayoutNode.ratio` from `number` to `number | number[] | string[]`
   - Allows ratio arrays like `[0.2, 0.3, 0.5]` or `["36px", "30px", "1fr"]`

2. **Helper Functions (eggToShell.ts)**
   - Added `normalizeRatios(childCount, ratio)`: Converts any ratio format to normalized `number[]` summing to 1
     - Handles single number (for 2 children)
     - Handles number arrays (normalizes to sum=1)
     - Handles string arrays with px/fr units (parses and converts)
     - Falls back to equal split for invalid inputs
   - Added `applySeamlessEdges(direction, child0, child1)`: Extracted seamless edge annotation logic
   - Added `nestSplits(children, ratios, direction, seamless, rootNodeId)`: Recursively nests N children into binary splits
     - Right-recursive: first child vs nested rest
     - Preserves correct ratios at each level
     - Applies seamless edges throughout the tree

3. **Split Handler Update (eggToShell.ts)**
   - Changed validation from `length !== 2` to `length < 2`
   - Added fast path for 2-child splits (preserves existing behavior)
   - Added N-child path (N > 2): calls `nestSplits()` to create nested binary tree
   - Preserves `secondChildAuto` flag on root split

4. **Comprehensive Tests (eggToShell.multiChild.test.ts)**
   - 16 tests covering:
     - 2-child splits (regression tests)
     - 3-child splits with number arrays
     - 3-child splits with string ratios (px + fr)
     - 4-child splits (3 levels of nesting)
     - Missing ratio (equal split fallback)
     - Seamless flag propagation
     - Edge cases (mismatched array length, px-only, fr-only)
     - Real-world chat.egg.md layout
   - All 16 tests pass

## Test Results

- **New tests:** 16/16 passing
- **Build:** Success (vite build completed in 38.51s)
- **chat.egg.md:** Now loads without error

## Commit Details

- **Commit:** 42fafd1
- **Branch:** main (pushed to origin)
- **Message:** "fix: support N-child splits in eggToShell (P0 production fix)"

## Production Impact

- **Before:** chat.shiftcenter.com failed to load with error: "split node must have exactly 2 children"
- **After:** chat.egg.md 3-child horizontal split (`["36px", "30px", "1fr"]`) loads correctly
- **Deployment:** Vercel will auto-deploy from main push

## Architecture Notes

The solution uses right-recursive binary nesting:
- For `[A, B, C]` with ratios `[r0, r1, r2]`:
  - Outer split: A (ratio r0/(r0+r1+r2)) vs inner split
  - Inner split: B (ratio r1/(r1+r2)) vs C
- Seamless edges apply at each level
- Root `nodeId` preserved on outermost split
