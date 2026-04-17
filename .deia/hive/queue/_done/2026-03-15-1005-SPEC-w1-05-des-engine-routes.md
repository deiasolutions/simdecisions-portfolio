# SPEC: Port DES engine_routes.py

## Priority
P0.25

## Model Assignment
haiku

## Objective
Port DES engine routes from platform (~265 lines). Provides API endpoints for simulation execution: /sim/start, /sim/step, /sim/status, /sim/results. Source: platform engine_routes.py. Target: hivenode/routes/des_routes.py. Register in routes/__init__.py.

## Acceptance Criteria
- [ ] DES engine routes ported
- [ ] Endpoints /sim/start /sim/step /sim/status /sim/results
- [ ] Routes registered in hivenode
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1005-SPEC-w1-05-des-engine-routes", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] python -m pytest tests/hivenode/test_des_routes.py -v
- [ ] No new test failures
