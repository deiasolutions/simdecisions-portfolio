# BRIEFING: Wire DES Simulation Events to Canvas Animation Components

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Model:** Sonnet
**Spec:** `.deia/hive/queue/2026-03-16-1500-SPEC-w2-05-animation-event-wiring.md`

---

## Objective

Wire the `useSimulation()` hook's event emissions to the six animation components (NodePulse, TokenAnimation, ResourceBar, SimClock, QueueBadge, CheckpointFlash) in FlowDesigner. All animation components are already ported from platform — they just need to subscribe to simulation events via the bus.

---

## Context from Q88N

This is a P1 spec from the Wave 2 queue. All animation components exist and have been ported in TASK-147. The simulation hook (`useSimulation.ts`) emits events (lines 264-354), but nothing is consuming them yet. We need to wire up event subscribers so that when a simulation runs, the canvas shows visual feedback: nodes pulse, tokens move, resource bars fill, clock ticks, etc.

---

## Key Files to Read

**Simulation hook (event emitter):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts` (lines 264-354 emit events)

**Animation components (event consumers):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\QueueBadge.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\CheckpointFlash.tsx`

**Integration point:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`

**Backend client:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desClient.ts`

---

## Acceptance Criteria (from spec)

- [ ] FlowDesigner has an event subscriber that listens to useSimulation() state changes
- [ ] When simulation runs, NodePulse highlights active nodes (nodes currently processing tokens)
- [ ] TokenAnimation shows tokens moving along edges during simulation
- [ ] ResourceBar updates fill level based on resource utilization from simulation events
- [ ] SimClock displays current simulation time
- [ ] QueueBadge shows queue length on resource nodes
- [ ] Animation state resets when simulation stops or resets
- [ ] CSS uses var(--sd-*) only
- [ ] 5+ tests for event → animation state mapping
- [ ] No file over 500 lines

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-16-1500-SPEC-w2-05-animation-event-wiring", "status": "running", "model": "sonnet", "message": "working"}
  ```
- File claims required: POST http://localhost:8420/build/claim before modifying files

---

## Smoke Test Requirements

- Run simulation → nodes pulse, tokens animate, resource bars fill, clock ticks
- Stop simulation → all animations reset to idle state
- `cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/`
- No new test failures

---

## What Q33N Must Do

1. **Read the 7 files listed above** to understand the current event emission and component structure
2. **Break down the wiring work into bee-sized tasks**:
   - Event subscriber setup in FlowDesigner
   - Wiring each animation component (NodePulse, TokenAnimation, ResourceBar, SimClock, QueueBadge, CheckpointFlash)
   - Animation state reset logic
   - Tests for event → animation state mapping
3. **Write task files** to `.deia/hive/tasks/` with:
   - Absolute file paths
   - Specific event names and payloads to subscribe to
   - Clear test requirements (min 5 tests for event mapping)
   - Constraints (500 lines, CSS vars, TDD, no stubs)
4. **Return to Q33NR** for review before dispatching bees

---

## Notes

- All animation components were ported in TASK-147, so they exist and have the right structure
- The simulation hook emits events via bus, but we need to verify the event names and payloads
- FlowDesigner is the integration point — it likely needs a top-level subscriber that passes data down to animation components
- Tests should mock simulation events and verify animation state updates

---

## Model Assignment

Sonnet (this is integration work requiring context understanding)
