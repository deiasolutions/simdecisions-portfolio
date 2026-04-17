# SPEC: Port canvas lasso selection + zoom controls + annotation badge

## Priority
P0.40

## Model Assignment
haiku

## Objective
Port 3 canvas interaction components (~435 lines): LassoSelection (multi-select by drawing rectangle), ZoomControls (fit, zoom in/out, reset), AnnotationBadge (comment count indicator on nodes). Source: platform canvas/. Target: browser/src/apps/sim/components/flow-designer/.

## Acceptance Criteria
- [ ] Lasso selection component ported
- [ ] Zoom controls component ported
- [ ] Annotation badge component ported
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1124-SPEC-w1-08-canvas-lasso-zoom", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/
- [ ] No new test failures
