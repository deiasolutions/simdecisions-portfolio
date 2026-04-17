# TASK-190: E2E Integration Test for Properties Panel Bus Wiring

## Objective
Write end-to-end integration test that verifies the complete flow: click node → PropertyPanel opens → edit property → canvas updates → click background → panel closes.

## Context
This test ensures all the pieces work together:
1. TASK-186: node click emits bus event
2. TASK-187: PropertyPanel listens and opens
3. TASK-188: PropertyPanel emits changes
4. TASK-189: FlowDesigner listens and updates
5. Background click closes panel

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__` (existing test patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`

## Deliverables
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\properties-bus-integration.test.tsx`
- [ ] Test: "node click emits node:selected bus event"
- [ ] Test: "node:selected event opens PropertyPanel with correct data"
- [ ] Test: "property edit emits node:property-changed event"
- [ ] Test: "node:property-changed updates canvas node"
- [ ] Test: "background click emits selection:cleared and closes panel"
- [ ] Test: "complete flow - click → edit → update → close"
- [ ] Test: "multiple node selections update panel correctly"
- [ ] Test: "property changes are reflected in node data immediately"

## Test Requirements
- [ ] 8+ integration tests covering full flow
- [ ] All tests pass
- [ ] Edge cases:
  - Rapid node switches
  - Edit without saving (reset)
  - Save multiple times
  - Switch nodes while panel open

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-190-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
