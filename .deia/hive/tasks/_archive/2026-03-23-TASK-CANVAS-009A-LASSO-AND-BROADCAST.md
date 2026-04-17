# TASK-CANVAS-009A: Port Lasso Selection + BroadcastChannel Multi-Window Sync

## Objective
Port lasso selection and BroadcastChannel multi-window sync from old platform canvas to new shiftcenter flow-designer.

## Context
Old platform had freeform lasso selection (LassoOverlay) and multi-window coordination via BroadcastChannel (highlight sync, search sync, execution mutations). Neither exists in the new flow-designer.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\LassoOverlay.tsx` (lasso implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\Canvas.tsx` (lines 238-343, BroadcastChannel)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\DesignMode.tsx`

## Deliverables
- [ ] `browser/src/apps/sim/components/flow-designer/LassoOverlay.tsx` — freeform lasso selection
- [ ] Lasso tool integrated into design mode (selection tool toggle: pointer/lasso/hand)
- [ ] BroadcastChannel sync: `highlight_node`, `focus-node`, `clear-highlights`, execution mutations
- [ ] Multi-window node highlighting with auto-fit
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/lasso-selection.test.tsx`
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/broadcast-sync.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 6+ lasso tests (empty selection, single node, multi-node, cancel, edge cases)
- [ ] 6+ broadcast tests (highlight, focus, clear, cross-channel sync)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Port from old platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-009A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — anything that didn't work, edge cases, recommended next tasks

DO NOT skip any section.
