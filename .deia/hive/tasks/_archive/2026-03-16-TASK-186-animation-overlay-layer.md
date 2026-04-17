# TASK-186: Add Animation Overlay Layer to FlowDesigner

## Objective
Add an animation overlay layer to FlowDesigner that renders NodePulse, TokenAnimation, ResourceBar, SimClock, QueueBadge, and CheckpointFlash components when simulation is running. Map simulation state to animation component props.

## Context
FlowDesigner already receives simulation state via `useSimulationLayer` hook (line 102). The simulation emits events and updates state, but we don't yet render any animation components to visualize it. We need to add an overlay layer that shows:
- NodePulse on active nodes (nodes processing tokens)
- TokenAnimation on edges with moving tokens
- ResourceBar on resource nodes showing utilization
- SimClock showing current sim time
- QueueBadge on nodes with queued tokens
- CheckpointFlash when checkpoints are reached

All animation components already exist and are tested. We just need to wire them up.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (integration point, line 698-700 for overlay section)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts` (event types, state shape)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\QueueBadge.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\CheckpointFlash.tsx`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\AnimationOverlay.tsx` component that:
  - Takes simulation state as props (simState, simulation.stats, nodeStates, edgeTokenCounts, viewport)
  - Renders NodePulse overlays for each active node (positioned absolutely using viewport transform)
  - Renders TokenAnimation overlays for each edge with tokens
  - Renders ResourceBar overlays on resource nodes
  - Renders SimClock in top-right corner
  - Renders QueueBadge on nodes with queue_length > 0
  - Renders CheckpointFlash when checkpoint events fire
- [ ] Integrate AnimationOverlay into FlowDesigner.tsx inside the FlowCanvas overlay section (after line 700)
- [ ] Pass necessary simulation state props from FlowDesigner to AnimationOverlay
- [ ] All animations reset to idle when simulation stops (`simState.running === false`)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Simulation not running → no animations visible
  - Simulation paused → animations freeze, SimClock shows PAUSED
  - Simulation stopped → animations reset to idle
  - Node becomes active → NodePulse appears
  - Token moves along edge → TokenAnimation shows movement
  - Resource utilization changes → ResourceBar updates
  - Checkpoint reached → CheckpointFlash fires

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- File must be named exactly: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\AnimationOverlay.tsx`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-186-RESPONSE.md`

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
