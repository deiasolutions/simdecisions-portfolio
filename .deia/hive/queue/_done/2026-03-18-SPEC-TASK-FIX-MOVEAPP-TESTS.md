# Fix moveAppOntoOccupied Tests (7 failing)

## Priority
P1

## Model Assignment
haiku

## Objective
Fix 7 failing moveAppOntoOccupied shell tests.

## What's Broken
- "MOVE_APP with center zone on occupied pane creates tabs"
- "MOVE_APP with left zone on occupied pane creates split"
- "MOVE_APP with right zone on occupied pane creates split"
- "MOVE_APP with top zone on occupied pane creates split"
- "MOVE_APP with bottom zone on occupied pane creates split"
- "MOVE_APP onto already-tabbed container adds to tabs"
- "MOVE_APP onto split parent creates nested structure"

Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "moveAppOntoOccupied (7 failed)"

## Files to Read First
- Find the test file (search for `moveAppOntoOccupied` in `browser/src/`)
- `browser/src/shell/` — reducer and related shell logic

## What To Do
1. Find and read the failing test file
2. Run tests to see exact errors
3. Fix implementation or tests
4. Confirm all 7 pass

## Response
Write response to: `.deia/hive/responses/20260318-FIX-MOVEAPP-TESTS.md`
