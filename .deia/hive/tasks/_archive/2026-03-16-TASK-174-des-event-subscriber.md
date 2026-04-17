# TASK-174: DES Event Subscriber Service

## Objective
Create event subscriber service that connects to DES simulation backend, receives events via polling, parses them, and emits them to canvas animation system.

## Context
The DES backend exposes `/api/des/run` endpoint that returns simulation statistics. We need a real-time event stream for animation. This task creates a polling-based event subscriber that:
1. Polls the DES backend for simulation state changes
2. Parses event data from the response
3. Emits parsed events to a local event bus for animation components to consume

The DES routes return a `RunResponse` with:
- `run_id`, `status`, `sim_time`
- `events_processed`, `tokens_created`, `tokens_completed`
- `statistics` dict with node/edge/resource metrics

Animation components (TokenAnimation, NodePulse, ResourceBar, SimClock) are already built and accept props. This service bridges the backend to the components.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`

## Deliverables
- [ ] Create `browser/src/apps/sim/services/desEventSubscriber.ts` (max 500 lines)
- [ ] Event subscriber polls `/api/des/run` endpoint
- [ ] Parse `RunResponse` statistics into typed events
- [ ] Event types: `TokenMoveEvent`, `NodeActivateEvent`, `ResourceUtilizationEvent`, `SimClockTickEvent`
- [ ] Emit events via EventEmitter or pub/sub pattern
- [ ] Support start/stop/pause controls
- [ ] Handle network errors gracefully
- [ ] Configurable poll interval (default 100ms)
- [ ] Create `browser/src/apps/sim/services/__tests__/desEventSubscriber.test.ts` (TDD)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Network failure during poll
  - Empty simulation response
  - Invalid JSON response
  - Stop during active poll
  - Rapid start/stop cycles
  - Event emission order (tokens before nodes)
- [ ] Mock fetch with vitest `vi.fn()`
- [ ] Test event emission with spy listeners
- [ ] Verify poll interval timing with fake timers

## Constraints
- Max 500 lines per file
- CSS: var(--sd-*) only (not applicable to this task)
- No stubs — all functions fully implemented
- TDD — tests first
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "TASK-174", "status": "running", "model": "sonnet", "message": "working on event subscriber"}`

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts:
1. POST http://localhost:8420/build/claim with JSON:
   `{"task_id": "TASK-174", "files": ["browser/src/apps/sim/services/desEventSubscriber.ts", "browser/src/apps/sim/services/__tests__/desEventSubscriber.test.ts"]}`
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until files are yours.
3. Release early: POST http://localhost:8420/build/release with JSON when done.
4. On heartbeat complete/failed, claims auto-release. Claims expire after 10 minutes.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-174-RESPONSE.md`

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
