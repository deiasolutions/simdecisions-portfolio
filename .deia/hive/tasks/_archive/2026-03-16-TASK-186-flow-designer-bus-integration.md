# TASK-186: Integrate MessageBus into FlowDesigner

## Objective
Add MessageBus to FlowDesigner via `useShell()` hook and wire node selection to emit `node:selected` bus event.

## Context
FlowDesigner currently uses local React state for node selection. It needs to emit bus events for cross-pane communication. The MessageBus is accessed via `useShell()` hook from `relay_bus`.

Files exist:
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` — main canvas component
- `browser/src/infrastructure/relay_bus/index.ts` — exports `useShell()` hook
- `browser/src/infrastructure/relay_bus/types/messages.ts` — bus message types

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\index.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\canvasAdapter.tsx` (example of bus usage)

## Deliverables
- [ ] Import `useShell` from `relay_bus` in FlowDesigner.tsx
- [ ] Call `useShell()` to get bus instance
- [ ] Add `node:selected` message type to `types/messages.ts` if not already present
- [ ] Wire `onNodeClick` in `useNodeEditing.ts` to emit `node:selected` bus event with payload:
  ```typescript
  {
    nodeId: string,
    nodeData: PhaseNodeData,
    position: { x: number, y: number }
  }
  ```
- [ ] Wire `onPaneClick` to emit `selection:cleared` bus event
- [ ] Tests written FIRST (TDD):
  - Test bus is obtained from useShell
  - Test node click emits node:selected event
  - Test pane click emits selection:cleared event
  - Test event payloads have correct structure

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Bus is null (gracefully handle)
  - Multiple rapid node clicks
  - Node click in non-design mode (should not emit)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable here)
- No stubs — all event handlers fully implemented
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-186-RESPONSE.md`

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
