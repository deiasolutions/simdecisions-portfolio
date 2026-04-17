# TASK-187: Wire PropertyPanel to Listen for node:selected Bus Event

## Objective
Modify PropertyPanel to subscribe to `node:selected` bus event and open when a node is selected on canvas.

## Context
PropertyPanel currently receives nodeProps directly from parent. It needs to listen for bus events and manage its own open/closed state based on `node:selected` and `selection:cleared` events.

This requires:
1. Converting PropertyPanel to manage its own visibility state
2. Subscribing to bus events
3. Converting node data from bus payload to NodeProperties format

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts` (for makeDefaultNodeProperties logic)

## Deliverables
- [ ] Add `paneId` and `bus` props to PropertyPanel
- [ ] Add internal state for visibility and current nodeProps
- [ ] Subscribe to `node:selected` bus event:
  - Convert payload to NodeProperties
  - Set visibility to true
  - Update nodeProps state
- [ ] Subscribe to `selection:cleared` bus event:
  - Set visibility to false
- [ ] Unsubscribe on unmount
- [ ] When not visible, render null
- [ ] Tests written FIRST (TDD):
  - Test subscribes to node:selected
  - Test opens when node:selected received
  - Test closes when selection:cleared received
  - Test converts bus payload to NodeProperties correctly
  - Test unsubscribes on unmount

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Bus is null
  - Malformed bus event payload
  - Multiple node:selected events (should replace current)
  - Receiving selection:cleared when already closed

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-187-RESPONSE.md`

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
