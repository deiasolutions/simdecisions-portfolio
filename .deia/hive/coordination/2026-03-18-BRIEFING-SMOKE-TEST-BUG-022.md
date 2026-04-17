# BRIEFING: Smoke Test BUG-022 Canvas Components Sidebar

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P1

## Objective

Verify that the BUG-022 fix (canvas components panel icons + click-to-place) actually works. Run the relevant browser tests and report results.

## Context

BUG-022 was fixed on 2026-03-17 by two bees:
- BUG-022-A: Icon rendering in TreeNodeRow (Unicode icons vs CSS class detection)
- BUG-022-B: Click-to-place via `palette:node-click` bus message

Completion report: `.deia/hive/responses/20260317-Q88NR-BUG-022-COMPLETION-REPORT.md`

## What Q33N Must Do

1. Run the BUG-022 specific test files:
   - `browser/src/primitives/tree-browser/TreeNodeRow.icon.test.tsx` (if exists)
   - `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.palette-icons.integration.test.tsx` (if exists)
   - `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx` (if exists)
   - Find these files (bees may have placed them in slightly different paths) using glob search

2. Run the full browser test suite: `cd browser && npx vitest run`

3. Check for regressions — are there any new test failures vs the last known green state?

4. Verify the modified files exist and are not stubs:
   - `browser/src/primitives/tree-browser/TreeNodeRow.tsx` — should have icon type detection
   - `browser/src/primitives/canvas/CanvasApp.tsx` — should have palette:node-click subscriber
   - `browser/src/primitives/tree-browser/TreeBrowser.tsx` — should have handleSelect wrapper

5. Report results to Q33NR. If tests pass, recommend marking BUG-022 RESOLVED in inventory.

## Constraints

- This is verification only. Do NOT modify any code.
- Do NOT dispatch bees. Just run tests and report.
- If tests fail, report which ones and why — Q33NR will decide next steps.
