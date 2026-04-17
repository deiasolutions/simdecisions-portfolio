# TASK-CANVAS-009B: Port Smart Edge Handles

## Objective
Port the applySmartHandles() function from old platform canvas to new shiftcenter flow-designer, enabling auto-positioned edge connection points.

## Context
Old platform had `applySmartHandles()` that auto-positions edge connection points based on relative node positions. This prevents edge crossing artifacts and produces cleaner flow diagrams. Not present in new flow-designer.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\Canvas.tsx` (line 362 and surrounding smart handle logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\edges\PhaseEdge.tsx`

## Deliverables
- [ ] Smart handle positioning logic integrated into FlowCanvas or a dedicated utility
- [ ] Handles auto-reposition based on relative node positions (top/bottom/left/right)
- [ ] Works with all node types (process + annotation)
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/smart-handles.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 6+ tests: left-of, right-of, above, below, diagonal, multi-edge scenarios

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Port from old platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-009B-RESPONSE.md`

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
