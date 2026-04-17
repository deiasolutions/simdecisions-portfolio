# CHROME-MINHEIGHT-FIX: Fix Chrome Primitive Height Collapse -- COMPLETE

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-03-27

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (line 80)
   - Added `minHeight?: number` to `AppNode.meta` type via intersection type

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` (lines 210-213, 238-262)
   - Added `_minHeightPx` extraction from meta in pane converter (line 212)
   - Added minHeight injection loop before child conversion in split handler (lines 238-250)
   - Fixed 2-child fast path to use `normalizeRatios()` for string array ratios (lines 254-261)

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx` (lines 8, 12-19, 29-30, 43-44, 55)
   - Added `getChildMinHeight()` helper function
   - Applied `minHeight` from child AppNode meta to wrapper divs (both first and second child)

4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (lines 288-289, 322-323, 356-357)
   - Applied `appNode.meta?.minHeight ? appNode.meta.minHeight + 'px' : 0` in COLD, WARM, and HOT rendering blocks

5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\chromeMinHeight.test.ts` (NEW, 221 lines)
   - 8 test cases for minHeight injection

## What Was Done

- **types.ts**: Extended `AppNode.meta` type from `Record<string, unknown>` to `Record<string, unknown> & { minHeight?: number }` for type safety.
- **eggToShell.ts**: In the split handler, before any child conversion occurs, a new loop detects if the `ratio` array contains string values. For each child pane whose corresponding ratio matches `/^(\d+)px$/`, a temporary `_minHeightPx` property is injected into the EggLayoutNode. When the pane converter runs (either directly or via `nestSplits()` recursion), it reads `_minHeightPx` and adds `minHeight: N` to `AppNode.meta`. This works for both 2-child and N-child splits. Also fixed the 2-child fast path which previously ignored string array ratios (defaulting to 0.5).
- **SplitContainer.tsx**: Added a `getChildMinHeight()` helper that reads `meta.minHeight` from AppNode children. The wrapper divs for both split children now use this value instead of hardcoded `0` for their `minHeight` CSS property.
- **ShellNodeRenderer.tsx**: All three rendering blocks (COLD, WARM, HOT) now read `appNode.meta?.minHeight` and apply it as `minHeight: Npx` CSS, falling back to `0` when not present.

## Test Results

- **chromeMinHeight.test.ts**: 8/8 passed
  - Injects minHeight: 30 for "30px" ratio
  - Injects minHeight: 24 for "24px" ratio
  - Does NOT inject minHeight for "1fr" ratio
  - normalizeRatios still produces correct flex ratios
  - canvas2.egg.md layout: menu-bar=30, status-bar=24
  - chat.egg.md layout: top-bar=36, menu-bar=30
  - Applies to ANY pane (not just chrome appTypes)
  - Preserves existing meta (seamless) alongside minHeight
- **eggToShell-related tests**: 57/57 passed (eggToShell.test, multiChild, showChrome, chromeMinHeight, chatEgg.integration)
- **Reducer and type tests**: 135/135 passed (reducer.test, reducer.layout, reducer.edge-cases, types, pin-collapse)
- **Additional shell tests**: 29/29 passed (saveEgg, slideover, turtleDrawEgg, useEggInit)
- **EGG tests**: 415/419 passed (4 pre-existing failures in simEgg tests, unrelated to this change)

## Build Verification

- All shell tests pass. No regressions from this change.
- 4 pre-existing failures in simEgg tests (simEgg.minimal, simEgg.test, simEggIntegration x2) are unrelated - they test sim EGG app registration and layout structure which changed independently.

## Acceptance Criteria

- [x] `eggLayoutToShellTree()` injects `minHeight: 30` for a pane with ratio `"30px"`
- [x] `eggLayoutToShellTree()` injects `minHeight: 24` for a pane with ratio `"24px"`
- [x] `eggLayoutToShellTree()` does NOT inject minHeight for a pane with ratio `"1fr"`
- [x] `normalizeRatios()` still produces correct flex ratios (existing behavior unchanged)
- [x] For canvas2.egg.md layout: menu-bar gets `minHeight: 30`, status-bar gets `minHeight: 24`
- [x] For chat.egg.md layout: top-bar gets `minHeight: 36`, menu-bar gets `minHeight: 30`
- [x] SplitContainer applies minHeight from child node meta
- [x] ShellNodeRenderer applies minHeight on AppNode containers (COLD, WARM, HOT)
- [x] No EGG file changes
- [x] No changes to normalizeRatios() ratio output
- [x] minHeight: 0 only overridden when meta.minHeight is present
- [x] All files under 500 lines

## Before/After Behavior

**Before:** Chrome primitives (menu-bar, top-bar, status-bar) were present in the DOM but rendered at 0px height. The `normalizeRatios()` function converted "30px" to a flex ratio of ~0.03, and both `SplitContainer.tsx` and `ShellNodeRenderer.tsx` applied `minHeight: 0` to all children, allowing chrome panes to collapse to zero pixels.

**After:** When a split node has string array ratios (e.g., `["30px", "1fr", "24px"]`), each child pane whose ratio matches `"Npx"` gets `minHeight: N` injected into its `AppNode.meta`. The SplitContainer wrapper div and ShellNodeRenderer container div both read this value and apply it as CSS `minHeight`, preventing the chrome pane from collapsing below its intended height.

## Clock / Cost / Carbon

- **Clock:** ~30 minutes
- **Cost:** ~$0.50 estimated
- **Carbon:** negligible

## Issues / Follow-ups

1. **2-child fast path with string arrays was silently broken**: Before this fix, a 2-child split with `ratio: ["30px", "1fr"]` would fall through to `typeof ratio === 'number' ? ratio : 0.5`, defaulting to 0.5 instead of using normalizeRatios. This is now fixed as part of this change.
2. **4 pre-existing simEgg test failures**: `simEgg.minimal.test.ts` (1), `simEgg.test.ts` (1), `simEggIntegration.test.ts` (2) - all unrelated to chrome minHeight. These should be tracked separately.
3. **minWidth support**: The briefing focused on minHeight (for horizontal splits, which stack vertically). For vertical splits that stack horizontally, a similar `minWidth` injection could be added in the future using the same pattern.
