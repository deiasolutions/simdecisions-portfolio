# Q33N Coordination Report: DES Canvas Visual Wiring

**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-des-canvas-visual
**Status:** TASK FILES READY FOR REVIEW
**Q33N Model:** sonnet

---

## Summary

I have created 6 task files that break down the DES canvas visual wiring work into bee-sized units. All tasks follow TDD, respect the 500-line limit, and include comprehensive test requirements.

---

## Task Breakdown

### TASK-174: DES Event Subscriber Service
**Assignee:** Sonnet BEE
**Dependencies:** None
**Files:**
- `browser/src/apps/sim/services/desEventSubscriber.ts` (create)
- `browser/src/apps/sim/services/__tests__/desEventSubscriber.test.ts` (create)

**What it does:**
Polling-based event subscriber that connects to `/api/des/run`, parses `RunResponse` statistics, and emits typed events (`TokenMoveEvent`, `NodeActivateEvent`, `ResourceUtilizationEvent`, `SimClockTickEvent`) via EventEmitter pattern. Supports start/stop/pause controls and configurable poll interval (default 100ms).

**Key design decisions:**
- Polling approach (not WebSocket) — simpler, works with existing REST API
- Event types mirror animation component needs (tokens, nodes, resources, clock)
- EventEmitter pattern for pub/sub (standard React pattern)

---

### TASK-175: Wire Token Movement to Canvas
**Assignee:** Sonnet BEE
**Dependencies:** TASK-174
**Files:**
- `browser/src/apps/sim/components/flow-designer/TokenAnimationLayer.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/__tests__/TokenAnimationLayer.test.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx` (modify — add TokenAnimationLayer child)

**What it does:**
React component that subscribes to `TokenMoveEvent`, manages token animation state (Map<tokenId, {startPos, endPos, startTime}>), renders TokenAnimation components overlaid on FlowCanvas, and removes completed tokens.

**Key design decisions:**
- Token state as Map (supports multiple simultaneous tokens)
- Edge positions calculated from ReactFlow nodes/edges
- TokenAnimation component already exists — just needs wiring

---

### TASK-176: Wire Node Highlighting to Canvas
**Assignee:** Sonnet BEE
**Dependencies:** TASK-174
**Files:**
- `browser/src/apps/sim/components/flow-designer/NodeHighlightLayer.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/__tests__/NodeHighlightLayer.test.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx` (modify — add NodeHighlightLayer child)

**What it does:**
React component that subscribes to `NodeActivateEvent`/`NodeDeactivateEvent`, manages active node set (Set<nodeId>), renders NodePulse components positioned over active nodes.

**Key design decisions:**
- Active state as Set (simple, efficient lookups)
- NodePulse component already exists — just needs positioning and state wiring

---

### TASK-177: Wire Resource Utilization Display
**Assignee:** Sonnet BEE
**Dependencies:** TASK-174
**Files:**
- `browser/src/apps/sim/components/flow-designer/ResourceUtilizationLayer.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/__tests__/ResourceUtilizationLayer.test.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx` (modify — add ResourceUtilizationLayer child)

**What it does:**
React component that subscribes to `ResourceUtilizationEvent`, manages resource utilization map (Map<resourceId, utilization>), renders ResourceBar components positioned over resource nodes.

**Key design decisions:**
- Utilization as 0-1 float (matches ResourceBar component API)
- Auto color-coding handled by ResourceBar component (green/orange/red thresholds)
- Smooth CSS transitions for utilization changes

---

### TASK-178: Wire Playback Controls to Animation
**Assignee:** Sonnet BEE
**Dependencies:** TASK-174
**Files:**
- `browser/src/apps/sim/components/flow-designer/PlaybackControls.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/__tests__/PlaybackControls.test.tsx` (create)
- `browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx` (modify — add SimClock and PlaybackControls)
- `browser/src/apps/sim/components/flow-designer/FlowToolbar.tsx` (modify — integrate PlaybackControls)

**What it does:**
Playback control UI (play/pause button, speed selector, reset button) wired to DES event subscriber. Subscribes to `SimClockTickEvent` and updates SimClock component with current time, speed ratio, paused state.

**Key design decisions:**
- Speed selector maps to poll interval (1x = 100ms, 2x = 50ms, 0.5x = 200ms)
- SimClock component already exists — just needs event wiring
- Controls rendered in FlowToolbar for consistent UI placement

---

### TASK-179: DES Animation Integration E2E Test
**Assignee:** Sonnet BEE
**Dependencies:** TASK-174, TASK-175, TASK-176, TASK-177, TASK-178
**Files:**
- `browser/src/apps/sim/components/flow-designer/__tests__/desAnimationE2E.test.tsx` (create)

**What it does:**
Black-box integration test that verifies the entire animation system responds correctly to real DES simulation responses. Mocks `/api/des/run`, runs simulation, verifies tokens move, nodes pulse, resources update, clock ticks, and playback controls work.

**Key design decisions:**
- E2E test written AFTER components exist (not strict TDD for integration tests)
- Realistic mock DES responses (matches `RunResponse` schema from `des_routes.py`)
- Tests visual state via DOM queries (presence of TokenAnimation, NodePulse, ResourceBar components)

---

## Parallelization Strategy

**Parallel group 1 (independent, can run simultaneously):**
- TASK-174 (event subscriber — no dependencies)

**Parallel group 2 (depend on TASK-174, can run simultaneously):**
- TASK-175 (token movement)
- TASK-176 (node highlighting)
- TASK-177 (resource utilization)
- TASK-178 (playback controls)

**Sequential (depends on all prior tasks):**
- TASK-179 (E2E test)

**Recommended dispatch order:**
1. Dispatch TASK-174 solo
2. Wait for TASK-174 completion
3. Dispatch TASK-175, TASK-176, TASK-177, TASK-178 in parallel (4 bees)
4. Wait for all 4 to complete
5. Dispatch TASK-179 solo

---

## File Claim Conflicts Anticipated

**FlowCanvas.tsx will be modified by TASK-175, TASK-176, TASK-177, TASK-178.**

File claim system will serialize these modifications. Recommended dispatch order within parallel group 2:
1. TASK-175 claims FlowCanvas first (adds TokenAnimationLayer)
2. TASK-176 claims FlowCanvas second (adds NodeHighlightLayer)
3. TASK-177 claims FlowCanvas third (adds ResourceUtilizationLayer)
4. TASK-178 claims FlowCanvas fourth (adds SimClock + PlaybackControls)

Each bee should release FlowCanvas claim as soon as their layer is added (do not hold claim while writing tests).

---

## Known Unknowns (Questions from Briefing)

### 1. What is the event schema from `/api/des/run`?
**Answer:** The `/api/des/run` endpoint returns a `RunResponse`:
```python
class RunResponse(BaseModel):
    run_id: str
    status: str
    sim_time: float
    events_processed: int
    tokens_created: int
    tokens_completed: int
    statistics: dict
```

The `statistics` dict contains node/edge/resource metrics. The exact schema is not documented in `des_routes.py`. **TASK-174 will need to investigate the `engine.des.engine.SimulationEngine.statistics()` method to determine the structure.**

**Risk:** If statistics schema is unclear, TASK-174 may need to define the event schema based on what animation components need (reverse-engineer from component APIs).

### 2. How do the 6 animation components currently receive props?
**Answer:** All 6 components accept props directly (no context/provider pattern). They are stateless presentational components. The wiring layers (TASK-175-178) will manage state and pass props down.

### 3. Is there an existing event bus in the canvas/flow-designer?
**Answer:** No. FlowCanvas uses ReactFlow's built-in event system for node/edge interactions, but there's no general-purpose event bus. TASK-174 will create a new EventEmitter-based pub/sub system.

### 4. What are the edge cases for token movement?
**Answer:** Identified in TASK-175:
- Multiple tokens on same edge (don't overwrite — use Map keyed by tokenId)
- Token events arrive out of order (timestamp tokens, sort if needed)
- Edge coordinates change mid-animation (recalculate on ReactFlow viewport change)
- Component unmounts while tokens are active (cleanup listeners in useEffect return)

### 5. What are the utilization thresholds for resource color changes?
**Answer:** Defined in `ResourceBar.tsx`:
- Green: utilization ≤ 60%
- Orange: 60% < utilization ≤ 80%
- Red: utilization > 80%

---

## Test Coverage

**Total tests:**
- TASK-174: ~12 tests (event subscriber)
- TASK-175: ~10 tests (token wiring)
- TASK-176: ~10 tests (node highlighting)
- TASK-177: ~10 tests (resource utilization)
- TASK-178: ~12 tests (playback controls)
- TASK-179: ~8 tests (E2E integration)

**Total: ~62 new tests**

---

## Smoke Test

After all tasks complete:
```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/desAnimationE2E.test.tsx
```

No new test failures expected. All 62 new tests should pass.

---

## Acceptance Criteria (from Spec)

- [ ] Token animations follow simulation events (TASK-175)
- [ ] Active nodes highlight during simulation (TASK-176)
- [ ] Resource nodes show utilization colors (TASK-177)
- [ ] Animation playback controls work (TASK-178)
- [ ] Tests written and passing (TASK-174, 175, 176, 177, 178, 179)

---

## Estimated Clock / Cost / Carbon

**Per task (average):**
- Clock: 45-60 minutes
- Cost: $2-3 (Sonnet)
- Carbon: ~10g CO2e

**Total (6 tasks):**
- Clock: 4.5-6 hours
- Cost: $12-18
- Carbon: ~60g CO2e

---

## Risks / Mitigation

### Risk 1: DES statistics schema unclear
**Mitigation:** TASK-174 should read `engine/des/engine.py` and `engine/des/core.py` to understand the statistics dict structure. If still unclear, define event schema based on animation component needs.

### Risk 2: FlowCanvas file claim conflicts
**Mitigation:** Use file claim system. Dispatch TASK-175-178 in sequence if conflicts cause long wait times. Bees should release FlowCanvas claim early (after adding their layer, before writing tests).

### Risk 3: Poll interval performance
**Mitigation:** Default 100ms poll interval may be too slow for smooth animation. TASK-174 should make interval configurable. TASK-178 can adjust based on speed selector (0.5x, 1x, 2x, 5x).

### Risk 4: Animation components incompatible with overlay approach
**Mitigation:** All 6 animation components use `position: absolute` and accept position props. They are designed for overlay rendering. No compatibility issues expected.

---

## Next Steps for Q33NR

1. **Review task files** (6 files in `.deia/hive/tasks/`)
2. **Approve or request corrections**
3. **Approve dispatch**

Once approved, Q33N will dispatch:
- TASK-174 (solo)
- TASK-175, TASK-176, TASK-177, TASK-178 (parallel, after TASK-174 completes)
- TASK-179 (solo, after all prior tasks complete)

---

**Q33N ready for Q33NR review.**
