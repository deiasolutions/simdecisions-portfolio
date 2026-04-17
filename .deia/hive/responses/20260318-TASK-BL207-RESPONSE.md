# TASK-BL207: EGG Chrome Opt-Out — Fix Hardcoded chrome:true -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — Line 115 changed from `chrome: true,` to `chrome: eggNode.chrome !== false,`

**Note:** Line 33 was already fixed in a prior commit (77b9c15). Line 115 was fixed during this session but appears to have been committed by another bee (cd0f00e) concurrently.

## What Was Done

- ✅ Verified line 33 already had `chrome: eggNode.chrome !== false,` (fixed in commit 77b9c15)
- ✅ Modified line 115 from `chrome: true,` to `chrome: eggNode.chrome !== false,`
- ✅ Ran eggToShell.test.ts — all 18 tests pass, including 3 chrome-specific tests
- ✅ Verified the fix respects EGG config `chrome` field:
  - `chrome: false` in EGG → AppNode with `chrome: false`
  - `chrome: true` in EGG → AppNode with `chrome: true`
  - No `chrome` field in EGG → AppNode with `chrome: true` (default)
- ✅ Confirmed backward compatibility: panes without `chrome` field default to showing title bar

## Test Results

**Test File:** `browser/src/shell/__tests__/eggToShell.test.ts`

```
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > converts single pane EGG layout to AppNode
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > converts horizontal split with 2 panes to SplitNode with 2 AppNode children
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > converts vertical split to SplitNode with correct direction
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > preserves ratio from EGG split node
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps EGG pane appType to AppNode appType
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps EGG pane config to AppNode appConfig
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > generates unique IDs for shell nodes when not provided
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > sets default LoadState.HOT for all app nodes
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > handles nested splits (split inside split)
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > returns valid BranchesRoot with layout, empty float/pinned/spotlight
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps chrome options from EGG pane to AppNode with defaults
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > applies default chrome options when not specified
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > preserves undefined chrome options as defaults
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > handles partial chrome options specified
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > preserves chrome options in nested panes (split)
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps chrome: false from EGG pane to AppNode with chrome: false
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > defaults chrome to true when not specified in EGG pane
✓ src/shell/__tests__/eggToShell.test.ts > eggToShell > maps chrome: true from EGG pane to AppNode with chrome: true

Test Files  1 passed (1)
     Tests  18 passed (18)
  Start at  20:51:57
  Duration  3.72s (transform 1.36s, setup 2.33s, collect 31ms, tests 6ms, environment 531ms, prepare 142ms)
```

**Chrome-specific tests (all passing):**
- ✅ `maps chrome: false from EGG pane to AppNode with chrome: false`
- ✅ `defaults chrome to true when not specified in EGG pane`
- ✅ `maps chrome: true from EGG pane to AppNode with chrome: true`

## Build Verification

**eggToShell.test.ts:** 18/18 tests passing ✅

**Broader shell test suite:** 827/855 tests passing (28 failures pre-existing, unrelated to this change)
- Failures are in reducer.lifecycle.test.ts related to volumeStorage mocking
- No regression from this change

**Verified behavior:**
- EGG panes with `"chrome": false` now produce shell AppNodes with `chrome: false`
- EGG panes with `"chrome": true` produce shell AppNodes with `chrome: true`
- EGG panes without `chrome` field produce shell AppNodes with `chrome: true` (default/backward compatible)

## Acceptance Criteria

- [x] `chrome: true` is NO LONGER hardcoded on line 33 (was already fixed in 77b9c15)
- [x] `chrome: true` is NO LONGER hardcoded on line 115 (fixed in this session)
- [x] EGG pane with `"chrome": false` produces shell node with `chrome: false`
- [x] EGG pane without chrome field produces shell node with `chrome: true`
- [x] EGG pane with `"chrome": true` produces shell node with `chrome: true`
- [x] All eggToShell tests pass (18/18)
- [x] build-monitor.egg.md test case ready (build-service pane has `chrome: false` on line 37)

## Clock / Cost / Carbon

**Clock:** 8 minutes (including test runs)
**Cost:** $0.12 (estimated: Sonnet input tokens ~50K, output ~3K)
**Carbon:** ~0.5g CO2e (estimated based on Claude API carbon intensity)

## Issues / Follow-ups

**None.** The task is complete.

**Test coverage:** The existing test suite already had 3 tests specifically for the chrome field behavior (lines 276-309 in eggToShell.test.ts). No new tests were needed.

**Concurrent fix:** During this session, another bee (TASK-236) also fixed line 115 as part of their work. The change was auto-committed by the queue runner in commit cd0f00e while this bee's tests were running. Both fixes were identical, so there is no conflict.

**Expected runtime behavior:** When the build-monitor EGG is loaded, the build-service pane (line 37 in build-monitor.egg.md with `"chrome": false`) will now correctly render without a title bar, appearing as a compact 28px status bar instead of 56px.

**Edge case handled:** The fallback path for unknown node types (lines 103-127) now also respects the chrome field from the original EGG node, maintaining consistency across all code paths.
