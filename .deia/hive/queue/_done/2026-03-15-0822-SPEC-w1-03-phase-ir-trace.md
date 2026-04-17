# SPEC: Port PHASE-IR trace system (25 event types, JSONL export)

## Priority
P0.15

## Model Assignment
haiku

## Objective
Port trace system from platform. 25 event types, JSONL export/import, trace routes. Source: platform trace.py (~420 lines). Target: engine/phase_ir/trace.py + hivenode/routes/phase_ir_trace.py. Follow store.py pattern already in engine/phase_ir/store.py.

## Acceptance Criteria
- [ ] Trace module with 25 event types
- [ ] JSONL export and import working
- [ ] Trace API routes registered
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-0822-SPEC-w1-03-phase-ir-trace", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] python -m pytest tests/engine/phase_ir/ -v
- [ ] No new test failures
