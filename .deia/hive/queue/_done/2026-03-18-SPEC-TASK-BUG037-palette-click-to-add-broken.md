# SPEC: BUG-037 — Clicking item in components palette no longer adds item to canvas (reversion)

## Priority: P0

## Problem
Clicking on an item in the components palette tree-view used to add that component to the canvas. This is now broken — clicking does nothing. This is a reversion caused by a recent overnight change.

## Investigation Required
1. Check git diff on ALL files related to palette click-to-add:
   - `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`
   - `browser/src/primitives/tree-browser/TreeBrowser.tsx`
   - `browser/src/primitives/tree-browser/TreeNodeRow.tsx`
   - `browser/src/primitives/canvas/CanvasApp.tsx`
   - `browser/src/infrastructure/relay_bus/messageBus.ts`
   - `browser/src/infrastructure/relay_bus/types/messages.ts`
2. Look at recent bee response files in `.deia/hive/responses/` from 2026-03-17 and 2026-03-18 that touched these files
3. Identify which change broke the click-to-add flow
4. The flow is: palette item click → bus message (e.g. canvas:add-node or similar) → CanvasApp receives message → adds node to canvas

## CRITICAL: Be careful with the fix
- Do NOT blindly revert entire files — other changes in those files may be intentional improvements
- Identify the SPECIFIC change that broke click-to-add
- Restore ONLY the broken behavior
- Verify other functionality in the same files still works after your fix

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-022-A-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-022-RESPONSE.md`

## Test Requirements
- Test that clicking a palette item publishes the correct bus message
- Test that CanvasApp receives the message and adds a node
- Test that existing canvas nodes are not affected
- All existing tree-browser and canvas tests still pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD
- CAREFUL restoration — do not break other recent fixes

## Model: sonnet
