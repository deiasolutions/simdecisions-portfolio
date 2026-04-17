# TASK-223: Validation Ledger Events — Schema + Emission (W1-B)

## Objective
Add `phase_validation` and `bee_execution` event types to the Event Ledger. Add helper functions for emitting these events. Wire into existing code paths.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). Every pipeline stage must emit to the Event Ledger. This task defines the event schemas and wires emission into existing fidelity check and bee dispatch code paths.

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1

## Files to Read First
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1 (event schemas)
- `.deia/hive/scripts/queue/run_queue.py` — existing dispatch/completion code paths
- `.deia/hive/scripts/queue/dispatch_handler.py` — bee dispatch logic
- `hivenode/routes/build_monitor.py` — existing heartbeat/event infrastructure

## Deliverables
- [ ] Create `.deia/hive/scripts/queue/ledger_events.py`
  - `emit_validation_event(spec_id, phase, fidelity_score, tokens_in, tokens_out, model, cost_usd, attempt, result, healing_attempts, wall_time_seconds)`
  - `emit_execution_event(spec_id, task_id, bee_id, model, session_id, tokens_in, tokens_out, cost_usd, wall_time_seconds, result, tests_before, tests_after, tests_new_passing, tests_new_failing, features_delivered, features_broken)`
  - Events POST to hivenode `/build/heartbeat` or a new `/build/event` endpoint
  - Schema matches Section 3.1 of the spec exactly
- [ ] Wire `emit_execution_event` into `dispatch_handler.py` bee completion path
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_ledger_events.py`
  - Test event schema validation
  - Test emission with mock HTTP endpoint
  - ~8 tests minimum

## Priority
P1

## Model
haiku
