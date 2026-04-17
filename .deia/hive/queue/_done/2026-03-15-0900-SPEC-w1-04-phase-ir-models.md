# SPEC: Port PHASE-IR models + schema_routes + validate_schema

## Priority
P0.20

## Model Assignment
haiku

## Objective
Port remaining PHASE-IR files: models.py (~82 lines), schema_routes.py, validate_schema.py (~140 lines). Rewrite models.py as SQLite store (follow hivenode/efemera/store.py pattern). Add jsonschema>=4.0 to pyproject.toml if not present.

## Acceptance Criteria
- [ ] models.py ported as SQLite store
- [ ] validate_schema.py ported with correct schema path
- [ ] schema_routes registered in hivenode
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-0900-SPEC-w1-04-phase-ir-models", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] python -m pytest tests/engine/phase_ir/ -v
- [ ] No new test failures
