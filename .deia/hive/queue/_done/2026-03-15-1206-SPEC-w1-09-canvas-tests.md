# SPEC: Port canvas test files (10 test files)

## Priority
P0.45

## Model Assignment
haiku

## Objective
Port 10 canvas test files from platform (~2,348 lines). Fix imports to use shiftcenter paths. Update mocks to match current component structure. Source: platform canvas/__tests__/. Target: browser/src/apps/sim/components/flow-designer/__tests__/.

## Acceptance Criteria
- [ ] All 10 test files ported
- [ ] Imports updated to shiftcenter paths
- [ ] All tests pass
- [ ] No regressions in existing tests

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1206-SPEC-w1-09-canvas-tests", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/
- [ ] No new test failures
