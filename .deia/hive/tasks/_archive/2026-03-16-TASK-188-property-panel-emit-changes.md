# TASK-188: Wire PropertyPanel to Emit node:property-changed Bus Event

## Objective
Modify PropertyPanel to emit `node:property-changed` bus event when properties are saved, allowing FlowDesigner to update the canvas node in real-time.

## Context
PropertyPanel currently calls `onSave` callback with updated properties. It needs to emit a bus event instead so any pane can listen for property changes.

The `node:property-changed` event should include:
- nodeId
- updated properties (full NodeProperties object)
- which section changed (general, timing, resources, etc.)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

## Deliverables
- [ ] Add `NodePropertyChangedData` interface to `types/messages.ts`:
  ```typescript
  export interface NodePropertyChangedData {
    nodeId: string;
    properties: NodeProperties;
    section?: string; // which tab changed
  }
  ```
- [ ] Add to ShellMessage union type
- [ ] Modify PropertyPanel's `handleSave` to emit `node:property-changed` event
- [ ] Include which section was edited (if tracking that)
- [ ] Keep backward compatibility: still call `onSave` if provided (for existing usage)
- [ ] Tests written FIRST (TDD):
  - Test save emits node:property-changed event
  - Test event payload has correct structure
  - Test event includes nodeId
  - Test event includes full properties
  - Test backward compatibility with onSave callback

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Bus is null (should still work with callback)
  - Save with no changes
  - Reset then save

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-188-RESPONSE.md`

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
