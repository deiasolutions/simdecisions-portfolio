# TASK-177: Wire Resource Utilization Display

## Objective
Connect ResourceBar component to DES event subscriber so resource nodes show color-coded utilization bars during simulation.

## Context
TASK-174 creates the DES event subscriber that emits `ResourceUtilizationEvent` objects with resource capacity and current utilization. This task:
1. Subscribes to resource utilization events
2. Manages resource utilization state (Map<resourceId, utilization>)
3. Renders ResourceBar components inside or overlaid on resource nodes
4. Updates utilization in real-time as events arrive

The ResourceBar component already exists and accepts:
- `utilization` (0-1 float)
- `label`, `height`, `width`, `showLabel`, `showPercentage` (optional)
- Auto color-codes: green (<60%), orange (60-80%), red (>80%)

This task creates a React component that wires resource utilization events to ResourceBar rendering.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desEventSubscriber.ts` (from TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\ResourceNode.tsx`

## Deliverables
- [ ] Create `browser/src/apps/sim/components/flow-designer/ResourceUtilizationLayer.tsx` (max 500 lines)
- [ ] Subscribe to `ResourceUtilizationEvent` from DES event subscriber
- [ ] Manage resource utilization map (Map<resourceId, utilization>)
- [ ] Render ResourceBar components positioned over resource nodes
- [ ] Calculate resource node positions from ReactFlow nodes
- [ ] Support multiple resource nodes simultaneously
- [ ] Update utilization dynamically (smooth transitions via CSS)
- [ ] Create `browser/src/apps/sim/components/flow-designer/__tests__/ResourceUtilizationLayer.test.tsx` (TDD)
- [ ] Update FlowCanvas to render ResourceUtilizationLayer as a child

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Multiple resources updating simultaneously
  - Utilization exceeds 1.0 (clamp to 1.0)
  - Utilization goes negative (clamp to 0.0)
  - Resource event for unknown resource ID (ignore or log warning)
  - Component unmounts while resources active (cleanup listeners)
  - Empty utilization map (no resources, no render)
  - Rapid utilization changes (100ms intervals) — verify no flicker
- [ ] Mock event subscriber with vitest
- [ ] Verify utilization state management (update existing, add new)
- [ ] Verify cleanup on unmount

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only
- No stubs — all functions fully implemented
- TDD — tests first
- Depends on TASK-174 (event subscriber must exist)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-177", "status": "running", "model": "sonnet", "message": "wiring resource utilization"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-177", "files": ["browser/src/apps/sim/components/flow-designer/ResourceUtilizationLayer.tsx", "browser/src/apps/sim/components/flow-designer/__tests__/ResourceUtilizationLayer.test.tsx", "browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s.
3. Release early when done.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-177-RESPONSE.md`

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
