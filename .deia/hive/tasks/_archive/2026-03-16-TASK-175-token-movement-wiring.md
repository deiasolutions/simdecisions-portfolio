# TASK-175: Wire Token Movement to Canvas

## Objective
Connect TokenAnimation component to DES event subscriber so tokens visually move along edges during simulation.

## Context
TASK-174 creates the DES event subscriber that emits `TokenMoveEvent` objects. This task:
1. Subscribes to token movement events from the event subscriber
2. Manages a collection of active token animations (state: Map<tokenId, TokenAnimationState>)
3. Renders TokenAnimation components overlaid on the FlowCanvas
4. Updates token positions based on events
5. Removes completed tokens from the canvas

The TokenAnimation component already exists and accepts:
- `startPos`, `endPos` (x/y coordinates)
- `duration` (milliseconds)
- `isActive` (boolean)
- `color`, `size` (optional)

This task creates the React component/hook that manages the token animation collection and wires it to the event subscriber.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desEventSubscriber.ts` (from TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvasTypes.ts`

## Deliverables
- [ ] Create `browser/src/apps/sim/components/flow-designer/TokenAnimationLayer.tsx` (max 500 lines)
- [ ] Subscribe to `TokenMoveEvent` from DES event subscriber
- [ ] Manage token animation state (Map<tokenId, {startPos, endPos, startTime, edgeId}>)
- [ ] Render TokenAnimation components for each active token
- [ ] Calculate edge start/end positions from ReactFlow nodes/edges
- [ ] Remove tokens when animation completes (duration elapsed)
- [ ] Support multiple simultaneous tokens on different edges
- [ ] Create `browser/src/apps/sim/components/flow-designer/__tests__/TokenAnimationLayer.test.tsx` (TDD)
- [ ] Update FlowCanvas to render TokenAnimationLayer as a child

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Multiple tokens on same edge (don't overwrite)
  - Token events arrive out of order
  - Edge coordinates change mid-animation
  - Component unmounts while tokens are active (cleanup listeners)
  - Empty token map (no tokens, no render)
  - Token completes before next event arrives
- [ ] Mock event subscriber with vitest
- [ ] Verify token state management (add, update, remove)
- [ ] Verify cleanup on unmount

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only
- No stubs — all functions fully implemented
- TDD — tests first
- Depends on TASK-174 (event subscriber must exist)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-175", "status": "running", "model": "sonnet", "message": "wiring token movement"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-175", "files": ["browser/src/apps/sim/components/flow-designer/TokenAnimationLayer.tsx", "browser/src/apps/sim/components/flow-designer/__tests__/TokenAnimationLayer.test.tsx", "browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s.
3. Release early when done.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-175-RESPONSE.md`

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
