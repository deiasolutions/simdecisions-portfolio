# TASK-178: Wire Playback Controls to Animation

## Objective
Connect SimClock component and playback controls (play/pause/speed) to DES event subscriber, allowing users to control animation speed and pause/resume simulation.

## Context
TASK-174 creates the DES event subscriber with start/stop/pause methods. This task:
1. Creates playback control UI (play/pause button, speed slider, reset button)
2. Wires controls to event subscriber start/pause/resume methods
3. Renders SimClock component that updates with simulation time
4. Subscribes to `SimClockTickEvent` from event subscriber
5. Updates SimClock with current sim time, speed ratio, paused state

The SimClock component already exists and accepts:
- `currentTime`, `startTime` (milliseconds)
- `paused`, `targetSpeedRatio`, `actualSpeedRatio`
- `precision`, `size`, `showTargetSpeed`

This task creates the playback control UI and wires it to the subscriber + SimClock.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desEventSubscriber.ts` (from TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowToolbar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`

## Deliverables
- [ ] Create `browser/src/apps/sim/components/flow-designer/PlaybackControls.tsx` (max 500 lines)
- [ ] Playback control UI: play/pause button, speed selector (0.5x, 1x, 2x, 5x), reset button
- [ ] Wire play button to `desEventSubscriber.start()`
- [ ] Wire pause button to `desEventSubscriber.pause()`
- [ ] Wire resume to `desEventSubscriber.resume()`
- [ ] Wire speed selector to update subscriber poll interval (e.g., 1x = 100ms, 2x = 50ms)
- [ ] Subscribe to `SimClockTickEvent` from event subscriber
- [ ] Update SimClock component with currentTime, paused state, speed ratio
- [ ] Render SimClock component in FlowCanvas corner or FlowToolbar
- [ ] Create `browser/src/apps/sim/components/flow-designer/__tests__/PlaybackControls.test.tsx` (TDD)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Play when already playing (no-op)
  - Pause when already paused (no-op)
  - Resume when not started (no-op or start)
  - Speed change during playback (update poll interval)
  - Reset clears simulation state and resets clock
  - Component unmounts while playing (cleanup, stop subscriber)
  - SimClock receives tick events and updates display
- [ ] Mock event subscriber with vitest
- [ ] Verify button state (play → pause icon transition)
- [ ] Verify speed selector changes poll interval
- [ ] Verify cleanup on unmount

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only
- No stubs — all functions fully implemented
- TDD — tests first
- Depends on TASK-174 (event subscriber must exist)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-178", "status": "running", "model": "sonnet", "message": "wiring playback controls"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-178", "files": ["browser/src/apps/sim/components/flow-designer/PlaybackControls.tsx", "browser/src/apps/sim/components/flow-designer/__tests__/PlaybackControls.test.tsx", "browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx", "browser/src/apps/sim/components/flow-designer/FlowToolbar.tsx"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s.
3. Release early when done.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-178-RESPONSE.md`

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
