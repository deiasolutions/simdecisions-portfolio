# TASK-179: DES Animation Integration E2E Test

## Objective
Write end-to-end integration tests that verify all DES animations (tokens, nodes, resources, clock) respond correctly to real DES simulation events.

## Context
TASK-174 through TASK-178 create the event subscriber and wiring layers. This task writes comprehensive integration tests that:
1. Run a real DES simulation via `/api/des/run`
2. Verify that TokenAnimationLayer renders moving tokens
3. Verify that NodeHighlightLayer activates nodes
4. Verify that ResourceUtilizationLayer updates resource bars
5. Verify that SimClock displays correct time and speed
6. Verify that playback controls work end-to-end

This is a **black-box integration test** that treats the entire animation system as a unit and verifies it against real backend responses.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desEventSubscriber.ts` (from TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\TokenAnimationLayer.tsx` (from TASK-175)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodeHighlightLayer.tsx` (from TASK-176)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ResourceUtilizationLayer.tsx` (from TASK-177)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\PlaybackControls.tsx` (from TASK-178)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`

## Deliverables
- [ ] Create `browser/src/apps/sim/components/flow-designer/__tests__/desAnimationE2E.test.tsx` (max 500 lines)
- [ ] Test: Tokens move along edges when simulation runs
- [ ] Test: Nodes pulse when active during simulation
- [ ] Test: Resource bars update color based on utilization
- [ ] Test: SimClock displays correct elapsed time
- [ ] Test: Playback controls (play/pause/speed) work correctly
- [ ] Test: Animation stops when simulation completes
- [ ] Test: Reset clears all animations and resets clock
- [ ] Mock fetch to return realistic DES simulation responses
- [ ] Use fake timers to control poll intervals
- [ ] Verify component state changes (active tokens, active nodes, utilization values)

## Test Requirements
- [ ] Tests written FIRST (TDD) — EXCEPTION: This is an integration test written AFTER components exist
- [ ] All tests pass
- [ ] Edge cases:
  - Empty flow (no nodes/edges) — no animations
  - Single node flow — no tokens, but node pulses
  - Multiple simultaneous tokens on different edges
  - Resource utilization reaches 100% (red color)
  - Simulation completes mid-animation (cleanup tokens)
  - Pause/resume preserves animation state
  - Speed change updates animation timing
- [ ] Mock `/api/des/run` with vitest `vi.fn()`
- [ ] Use `@testing-library/react` for rendering and queries
- [ ] Verify visual state (DOM presence of TokenAnimation, NodePulse, ResourceBar components)

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only (not applicable to tests)
- No stubs — all tests fully implemented
- Depends on TASK-174, TASK-175, TASK-176, TASK-177, TASK-178
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-179", "status": "running", "model": "sonnet", "message": "writing E2E tests"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-179", "files": ["browser/src/apps/sim/components/flow-designer/__tests__/desAnimationE2E.test.tsx"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s.
3. Release early when done.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-179-RESPONSE.md`

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
