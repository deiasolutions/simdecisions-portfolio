# BRIEFING: TASK-223 — Validation Ledger Events (W1-B)

**Date:** 2026-03-16
**From:** Q33NR (Regent Queue Bot)
**To:** Q33N (Queen Coordinator)
**Source Spec:** SPEC-PIPELINE-001 (Unified Build Pipeline), Section 3.1
**Priority:** P1
**Model Assignment:** Haiku

---

## Objective

Add two new event types to the Event Ledger system:
1. `phase_validation` — emitted by fidelity gates (Gate 0, Phase 0–2)
2. `bee_execution` — emitted by bee dispatch/completion code paths

Create helper functions for emitting these events. Wire them into existing queue runner code paths.

---

## Context

Part of SPEC-PIPELINE-001 (Unified Build Pipeline). The spec requires every pipeline stage to emit structured events to the Event Ledger for later statistical analysis. This task (W1-B) is one of the initial Wave 1 tasks with no dependencies.

The Event Ledger will accumulate data over 50–100 specs to answer the question: **"Does the IR fidelity gate reduce bee failure rate enough to justify its token cost?"**

This task is purely additive. It does NOT modify existing queue runner behavior — it adds instrumentation for future analysis.

---

## What Q33N Must Deliver

One task file for one bee. The bee must:

1. **Create** `.deia/hive/scripts/queue/ledger_events.py` with:
   - `emit_validation_event(...)` — 10 parameters matching schema in Section 3.1
   - `emit_execution_event(...)` — 16 parameters matching schema in Section 3.1
   - Both functions POST to hivenode `/build/heartbeat` or a new `/build/event` endpoint
   - Use `httpx` for HTTP calls
   - Schema must match SPEC-PIPELINE-001 Section 3.1 exactly

2. **Wire** `emit_execution_event` into existing bee dispatch code paths:
   - Likely in `.deia/hive/scripts/queue/dispatch_handler.py` (bee completion)
   - Or in `run_queue.py` where bee results are processed
   - Q33N must read these files and determine the correct insertion point

3. **Write tests FIRST** (TDD):
   - File: `.deia/hive/scripts/queue/tests/test_ledger_events.py`
   - Minimum 8 tests:
     - Schema validation (correct field names, types)
     - HTTP POST with mock endpoint
     - Error handling (timeout, connection error)
     - Emission from dispatch path (integration test)
   - All tests must pass

---

## Files Q33N Should Read Before Writing the Task File

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1 (event schemas)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — existing dispatch/completion code paths
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — bee dispatch logic (if exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — existing heartbeat/event infrastructure

---

## Schema Reference (from SPEC-PIPELINE-001 Section 3.1)

### Event: `phase_validation`

```yaml
event_type: phase_validation
spec_id: SPEC-XXX
phase: gate_0 | phase_0 | phase_1 | phase_2
fidelity_score: 0.91        # null for gate_0
tokens_in: 1200
tokens_out: 800
model: haiku
cost_usd: 0.002
attempt: 1                   # 1 = first try, 2+ = healing retry
result: PASS | FAIL | HEALED
healing_attempts: 0
wall_time_seconds: 12
```

### Event: `bee_execution`

```yaml
event_type: bee_execution
spec_id: SPEC-XXX
task_id: TASK-XXX
bee_id: BEE-HAIKU-1
model: haiku-4.5
session_id: ses_abc123
tokens_in: 45000
tokens_out: 12000
cost_usd: 0.08
wall_time_seconds: 180
result: CLEAN | TIMEOUT | NEEDS_DAVE | CRASH
tests_before: 185
tests_after: 197
tests_new_passing: 12
tests_new_failing: 0
features_delivered: [SHELL-042, SHELL-043]
features_broken: []
```

---

## Constraints (from BOOT.md)

- **No file over 500 lines.** If `run_queue.py` is approaching 1,000 lines, extract helpers to a separate file.
- **TDD.** Tests first, then implementation.
- **NO STUBS.** Every function fully implemented.
- **Absolute file paths** in task file.
- **8-section response file** required.
- **No hardcoded colors** (not applicable here).

---

## What Q33N Should NOT Do

- Do NOT modify the queue runner's core logic (pickup, dispatch, completion handling). Only add event emission.
- Do NOT create a new hivenode endpoint if `/build/heartbeat` already accepts arbitrary event types. Q33N must read `build_monitor.py` and determine if a new endpoint is needed or if heartbeat is sufficient.
- Do NOT skip tests. TDD is mandatory.
- Do NOT write vague acceptance criteria. Every deliverable must be concrete and verifiable.

---

## Success Criteria for Q33N's Task File

The task file Q33N writes must pass the mechanical review checklist:

- [ ] Deliverables match the briefing (ledger_events.py created, wired into dispatch path, tests written)
- [ ] File paths are absolute
- [ ] Test requirements are specific (minimum 8 tests, scenarios listed)
- [ ] No file over 500 lines (check if ledger_events.py + tests fits within this)
- [ ] NO STUBS (functions fully implemented, or task explicitly says "cannot finish — reason")
- [ ] Response file template requirement included

---

## Next Steps

1. Q33N reads this briefing
2. Q33N reads the files listed above
3. Q33N writes ONE task file: `2026-03-16-TASK-223-VALIDATION-LEDGER-EVENTS.md`
4. Q33N returns the task file to Q33NR for review
5. Q33NR reviews against the mechanical checklist
6. Q33NR approves or requests corrections (max 2 cycles)
7. Q33NR dispatches bee (Haiku model)

---

**End of briefing.**
