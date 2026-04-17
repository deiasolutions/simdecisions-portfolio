# TASK-176: Wire Node Highlighting to Canvas

## Objective
Connect NodePulse component to DES event subscriber so active nodes pulse/glow during simulation.

## Context
TASK-174 creates the DES event subscriber that emits `NodeActivateEvent` objects when nodes become active during simulation. This task:
1. Subscribes to node activation events from the event subscriber
2. Manages node active state (Set<nodeId> or Map<nodeId, boolean>)
3. Overlays NodePulse components on active nodes in FlowCanvas
4. Deactivates nodes when they complete processing

The NodePulse component already exists and accepts:
- `isActive` (boolean)
- `size`, `color`, `intensity` (optional)

This task creates a React component/hook that manages node highlighting state and renders NodePulse overlays.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desEventSubscriber.ts` (from TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx`

## Deliverables
- [ ] Create `browser/src/apps/sim/components/flow-designer/NodeHighlightLayer.tsx` (max 500 lines)
- [ ] Subscribe to `NodeActivateEvent` and `NodeDeactivateEvent` from DES event subscriber
- [ ] Manage active node set (Set<nodeId>)
- [ ] Render NodePulse components positioned over active nodes
- [ ] Calculate node positions from ReactFlow nodes
- [ ] Support simultaneous multiple active nodes
- [ ] Create `browser/src/apps/sim/components/flow-designer/__tests__/NodeHighlightLayer.test.tsx` (TDD)
- [ ] Update FlowCanvas to render NodeHighlightLayer as a child

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Multiple nodes active simultaneously
  - Node activates then immediately deactivates
  - Activate event for already-active node (idempotent)
  - Deactivate event for non-active node (no-op)
  - Component unmounts while nodes are active (cleanup listeners)
  - Empty active set (no nodes, no render)
  - Node position changes while active (update overlay position)
- [ ] Mock event subscriber with vitest
- [ ] Verify active state management (add, remove)
- [ ] Verify cleanup on unmount

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only
- No stubs — all functions fully implemented
- TDD — tests first
- Depends on TASK-174 (event subscriber must exist)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-176", "status": "running", "model": "sonnet", "message": "wiring node highlighting"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-176", "files": ["browser/src/apps/sim/components/flow-designer/NodeHighlightLayer.tsx", "browser/src/apps/sim/components/flow-designer/__tests__/NodeHighlightLayer.test.tsx", "browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s.
3. Release early when done.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-176-RESPONSE.md`

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
