# SPEC: Port canvas animation system (6 components)

## Priority
P0.35

## Model Assignment
haiku

## Objective
Port 6 canvas animation components from platform (~749 lines): TokenAnimation, NodePulse, EdgeFlow, ResourceMeter, SimClock, AnimationController. Source: platform canvas/animation/. Target: browser/src/apps/sim/components/flow-designer/animation/.

## Acceptance Criteria
- [ ] All 6 animation components ported
- [ ] Animation controller manages playback state
- [ ] Token animations follow edges
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1036-SPEC-w1-07-canvas-animation", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/
- [ ] No new test failures
