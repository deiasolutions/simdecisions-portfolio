# SPEC: Wire Process 13 quality gates into dispatch pipeline

## Priority
P0.85

## Model Assignment
sonnet

## Objective
Wire Process 13 quality gates (spec validation then build then test then review) into the dispatch pipeline. Read .deia/processes/PROCESS-LIBRARY-V2.md for P-13 definition. Implement gates in spec_processor.py: validate spec format, run tests before/after, check for regressions, flag for review if tests fail.

## Acceptance Criteria
- [ ] Quality gates implemented in spec_processor.py
- [ ] Spec format validation before dispatch
- [ ] Pre/post test comparison
- [ ] Regression detection flags NEEDS_DAVE
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1519-SPEC-w2-01-process13-quality-gates", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] python -m pytest .deia/hive/scripts/queue/tests/ -v
- [ ] No new test failures
