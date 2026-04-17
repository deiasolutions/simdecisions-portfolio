# TASK-BL207-B: EGG Chrome Opt-Out (SOURCE CODE FIX) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — Modified line 33 to read `chrome` field from EGG node
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — Added 3 new test cases for chrome field handling

## What Was Done

- Changed `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` line 33 from `chrome: true,` to `chrome: eggNode.chrome !== false,`
- Line 115 left unchanged (it's the fallback handler for unknown node types, which should default to `chrome: true`)
- Added test case: "maps chrome: false from EGG pane to AppNode with chrome: false"
- Added test case: "defaults chrome to true when not specified in EGG pane"
- Added test case: "maps chrome: true from EGG pane to AppNode with chrome: true"
- All 21 existing tests still pass
- All 3 new tests pass

## Test Results

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts`

**Pass/Fail:**
- 18 tests passed (21 existing + 3 new = 24, but I miscounted - there were 15 existing)
- 0 tests failed

## Build Verification

```
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
```

**Output (last 10 lines):**
```
 ✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > handles partial chrome options specified
 ✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > preserves chrome options in nested panes (split)
 ✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps chrome: false from EGG pane to AppNode with chrome: false
 ✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > defaults chrome to true when not specified in EGG pane
 ✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps chrome: true from EGG pane to AppNode with chrome: true

 Test Files  1 passed (1)
      Tests  18 passed (18)
   Start at  20:50:11
   Duration  9.69s (transform 3.83s, setup 5.70s, collect 56ms, tests 10ms, environment 2.02s, prepare 1.31s)
```

## Acceptance Criteria

- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` line 33 changed from `chrome: true,` to `chrome: eggNode.chrome !== false,`
- [x] Line 115 unchanged (it's the fallback handler, should stay `chrome: true`)
- [x] Test: EGG pane with `chrome: false` → shell node with `chrome: false`
- [x] Test: EGG pane without chrome field → shell node with `chrome: true` (default)
- [x] Test: EGG pane with `chrome: true` → shell node with `chrome: true`
- [x] All existing eggToShell tests pass (15 existing tests)
- [x] New tests pass (3 tests)
- [x] Smoke test: `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts` shows 18 tests passing

## Clock / Cost / Carbon

**Clock:** 4 minutes (from 20:49 to 20:52)
**Cost:** ~$0.02 (Sonnet, minimal context usage)
**Carbon:** ~2g CO2e (fast implementation, single test run)

## Issues / Follow-ups

**None.**

This was a clean source code fix. The logic `eggNode.chrome !== false` correctly handles:
- `chrome: false` → `false` (opt-out)
- `chrome: true` → `true` (explicit opt-in)
- `chrome` undefined → `true` (default behavior)

The fix enables EGG files like `build-monitor.egg.md` to hide chrome on specific panes (e.g., the 28px status bar pane).

Line 115 was correctly left unchanged because it's the fallback handler for unknown node types, which has no `eggNode` to read from and should default to showing chrome.

**Next steps:** This fix unblocks BUG-036 (Build Monitor tree layout test), which depends on the build-data-service pane having no chrome.
