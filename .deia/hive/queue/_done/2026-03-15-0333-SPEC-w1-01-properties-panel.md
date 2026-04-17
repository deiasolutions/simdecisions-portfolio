# SPEC: Port Properties Panel (16 files, 6 accordion sections)

## Priority
P0.05

## Model Assignment
sonnet

## Objective
Port the Properties Panel from platform/efemera to shiftcenter. 16 files, 6 accordion sections (General, Data, Rules, Connections, Resources, Advanced). Full node property editor. Source: platform/efemera/src/efemera/components/properties/. Target: browser/src/apps/sim/components/properties/.

## Acceptance Criteria
- [ ] All 16 properties panel files ported
- [ ] 6 accordion sections render correctly
- [ ] Node property editing works
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-0333-SPEC-w1-01-properties-panel", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/properties/
- [ ] No new test failures
