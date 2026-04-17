# SPEC: Port RAG entity vectors + Voyage AI + BOK services

## Priority
P0.55

## Model Assignment
sonnet

## Objective
Port RAG entity vectors, Voyage AI adapter, and BOK (Body of Knowledge) services (~1,497 lines). Entity extraction, named entity vectors, BOK document management. Source: platform/rag/. Target: hivenode/rag/.

## Acceptance Criteria
- [ ] Entity vector extraction ported
- [ ] Voyage AI adapter ported
- [ ] BOK service ported
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1305-SPEC-w1-11-rag-entity-vectors", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] python -m pytest tests/hivenode/test_rag*.py -v
- [ ] No new test failures
