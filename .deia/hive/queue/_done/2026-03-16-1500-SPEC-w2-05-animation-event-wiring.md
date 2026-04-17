# SPEC: Wire DES Simulation Events to Canvas Animation Components

## Priority
P1

## Objective
Wire useSimulation event emissions to NodePulse, TokenAnimation, ResourceBar, SimClock in FlowDesigner. All animation components already exist and are ported — they just need to consume simulation events via bus event subscribers.

## Context
Files to read first:
- `browser/src/apps/sim/components/flow-designer/simulation/useSimulation.ts` (emits events, lines 264-354)
- `browser/src/apps/sim/components/flow-designer/animation/TokenAnimation.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/NodePulse.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/ResourceBar.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/SimClock.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/QueueBadge.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/CheckpointFlash.tsx`
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`
- `browser/src/apps/sim/services/desClient.ts`

## Acceptance Criteria
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

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-16-1500-SPEC-w2-05-animation-event-wiring", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-16-1500-SPEC-w2-05-animation-event-wiring", "files": ["path/to/file1.ts"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done, release early: POST http://localhost:8420/build/release

## Smoke Test
- [ ] Run simulation → nodes pulse, tokens animate, resource bars fill, clock ticks
- [ ] Stop simulation → all animations reset to idle state
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/
- [ ] No new test failures

## Model Assignment
sonnet
