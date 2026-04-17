# TASK-CANVAS-009C: Port Missing Property Panel Sections

## Objective
Port the 6 missing property panel sections from old platform to new shiftcenter flow-designer, bringing property editing to full parity.

## Context
Old platform had 16 property sections. New flow-designer has 6 tabs (General, Timing, Resources, Guards, Actions, Oracle). Missing: Queue, Operator, Outputs, Badges, Edge properties, Design properties. Port them.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\panels\properties\` (all files — read the directory)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\GeneralTab.tsx` (reference pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts`

## Deliverables
- [ ] `properties/QueueTab.tsx` — queue discipline, capacity, priority rules
- [ ] `properties/OperatorTab.tsx` — operator assignments, skill requirements
- [ ] `properties/OutputsTab.tsx` — output variables, data mappings
- [ ] `properties/BadgesTab.tsx` — visual badges, status indicators
- [ ] `properties/EdgePropertiesTab.tsx` — edge labels, weights, guards, conditions
- [ ] `properties/DesignTab.tsx` — design-level metadata, documentation notes
- [ ] Register all 6 new tabs in `PropertyPanel.tsx`
- [ ] Add TypeScript types for each tab's data model in `types.ts`
- [ ] Test file: `browser/src/apps/sim/components/flow-designer/__tests__/property-tabs-extended.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 12+ tests (2 per tab): renders correctly, validates input, shows defaults, saves to node data
- [ ] Edge cases: empty values, invalid inputs, edge properties on different edge types

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — every tab fully functional with real form fields
- Port from old platform — match the field names and behavior

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-009C-RESPONSE.md`

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
