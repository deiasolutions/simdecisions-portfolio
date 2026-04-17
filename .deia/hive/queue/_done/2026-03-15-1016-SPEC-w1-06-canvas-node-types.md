# SPEC: Port canvas missing node types (13 BPMN + annotation types)

## Priority
P0.30

## Model Assignment
sonnet

## Objective
Port 13 missing canvas node type components from platform: BPMN gateway types (exclusive, parallel, inclusive, event-based, complex), BPMN event types (intermediate, boundary, signal, timer, error, compensation, escalation), and annotation node. ~1,110 lines total. Source: platform canvas/nodes/. Target: browser/src/apps/sim/components/flow-designer/nodes/.

## Acceptance Criteria
- [ ] All 13 node type components ported
- [ ] Each node renders correctly in canvas
- [ ] Node type registry updated
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1016-SPEC-w1-06-canvas-node-types", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/
- [ ] No new test failures
