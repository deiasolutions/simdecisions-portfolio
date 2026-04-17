# TASK-187: Animation Event Mapping Tests

**ARCHIVED: Redundant with TASK-186's internal TDD approach**

Q33NR determined that TASK-186 already includes test-driven development for the AnimationOverlay component. Having TASK-187 write tests separately would create ordering issues (cannot test a component that doesn't exist yet). TASK-186 will handle both interface definition, tests, and implementation in one TDD flow.

---

## Objective
Write comprehensive tests for simulation event → animation state mapping. Test that when simulation events fire (token_move, node_activate, resource_claim, etc.), the AnimationOverlay component correctly updates animation component visibility and props.

## Context
TASK-186 creates the AnimationOverlay component. This task writes tests FIRST to verify that simulation events correctly map to animation state. We need at least 5 tests covering different event types and their visual effects.

The test strategy:
1. Mock simulation state (simState, stats, nodeStates, edgeTokenCounts)
2. Render AnimationOverlay with that state
3. Assert correct animation components are rendered with correct props
4. Update state (simulating event emission)
5. Assert animations update accordingly

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\AnimationOverlay.tsx` (created by TASK-186)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts` (event types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\animation.test.tsx` (existing animation component tests for reference)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\__tests__\AnimationOverlay.test.tsx` with tests for:
  - **node_activate event** → NodePulse appears on that node
  - **token_move event** → TokenAnimation appears on that edge
  - **resource_claim event** → ResourceBar updates fill level
  - **checkpoint_reached event** → CheckpointFlash fires
  - **sim_stats event** → SimClock updates time, ResourceBar updates utilization
  - **node_activate with queue_length > 0** → QueueBadge appears with count
  - **simulation stop** → all animations reset (no NodePulse, no TokenAnimation, SimClock hidden)
  - **simulation pause** → SimClock shows PAUSED
- [ ] All tests pass
- [ ] Tests use vitest mocking and @testing-library/react

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - No simulation running → overlay renders nothing (or only static elements)
  - Multiple nodes active → multiple NodePulse overlays
  - Multiple edges with tokens → multiple TokenAnimation overlays
  - Resource utilization > 0.8 → ResourceBar shows red color
  - Queue count > 999 → QueueBadge shows "999+"

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- File must be named exactly: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\__tests__\AnimationOverlay.test.tsx`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-187-RESPONSE.md`

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
