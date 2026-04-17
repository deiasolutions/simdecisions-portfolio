# TASK-223: Validation Ledger Events (W1-B)

**Date:** 2026-03-16
**Source:** SPEC-PIPELINE-001 (Unified Build Pipeline), Wave 1, Task B
**Priority:** P1
**Model Assignment:** Haiku
**Estimated Lines:** ~40 (module) + ~120 (tests)

---

## Objective

Create a ledger events module with two helper functions (`emit_validation_event`, `emit_execution_event`) to send structured event data to the Event Ledger. Wire `emit_execution_event` into existing bee dispatch completion code paths. This is purely instrumentation — no behavior changes to the queue runner.

---

## Context

SPEC-PIPELINE-001 requires all pipeline stages to emit structured events to an Event Ledger for statistical analysis. After 50–100 specs, the data will answer: **"Does the IR fidelity gate reduce bee failure rate enough to justify its token cost?"**

This task (W1-B) is Wave 1 and has no dependencies. It adds instrumentation only — existing queue runner behavior is unchanged.

The Event Ledger currently accepts heartbeat events via `POST /build/heartbeat`. You will create a new module that emits `phase_validation` and `bee_execution` events using the same endpoint.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1 (event schemas)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — heartbeat endpoint (line 546–549)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — bee completion handling (lines 462–496)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — dispatch result parsing (lines 313–331)

---

## Deliverables

### 1. Create `.deia/hive/scripts/queue/ledger_events.py`

**Function 1: `emit_validation_event(...)`**

Parameters (10 total, matching SPEC-PIPELINE-001 Section 3.1):
- `spec_id: str`
- `phase: str` — one of: `"gate_0"`, `"phase_0"`, `"phase_1"`, `"phase_2"`
- `fidelity_score: Optional[float]` — null for gate_0
- `tokens_in: int`
- `tokens_out: int`
- `model: str`
- `cost_usd: float`
- `attempt: int` — 1 = first try, 2+ = healing retry
- `result: str` — one of: `"PASS"`, `"FAIL"`, `"HEALED"`
- `wall_time_seconds: int`
- `healing_attempts: int` — default 0

**Function 2: `emit_execution_event(...)`**

Parameters (16 total, matching SPEC-PIPELINE-001 Section 3.1):
- `spec_id: str`
- `task_id: str`
- `bee_id: str`
- `model: str`
- `session_id: str`
- `tokens_in: int`
- `tokens_out: int`
- `cost_usd: float`
- `wall_time_seconds: int`
- `result: str` — one of: `"CLEAN"`, `"TIMEOUT"`, `"NEEDS_DAVE"`, `"CRASH"`
- `tests_before: int`
- `tests_after: int`
- `tests_new_passing: int`
- `tests_new_failing: int`
- `features_delivered: list[str]`
- `features_broken: list[str]`

**Implementation requirements:**
- Both functions POST to `http://127.0.0.1:8420/build/heartbeat` using `urllib.request` (no external deps)
- Use `HeartbeatPayload` schema from `build_monitor.py` as reference — add new fields to payload dict
- Payload must include:
  - `task_id` = spec_id (required by heartbeat endpoint)
  - `status` = "ledger_event" (new status type)
  - `message` = JSON dump of the full event dict
  - `role` = "LEDGER"
- Silent failure on HTTP errors (log to stderr, don't crash)
- Timeout: 5 seconds
- Return True on success, False on failure

### 2. Wire `emit_execution_event` into bee completion code

**Location:** `run_queue.py`, function `_handle_spec_result` (lines 207–381)

**Insertion point:** After line 243 (`session_cost += result.cost_usd`), before status routing logic.

**What to emit:**
```python
# Extract from SpecResult and spec metadata
emit_execution_event(
    spec_id=spec.path.stem,
    task_id=spec.path.stem,
    bee_id=f"BEE-{spec.model.upper()}-{datetime.now().strftime('%H%M%S')}",
    model=spec.model or "unknown",
    session_id="unknown",  # Not tracked yet — acceptable stub
    tokens_in=0,  # Not tracked yet — acceptable stub
    tokens_out=0,  # Not tracked yet — acceptable stub
    cost_usd=result.cost_usd,
    wall_time_seconds=int(result.duration_ms / 1000),
    result=result.status,
    tests_before=0,  # Not tracked yet — acceptable stub
    tests_after=0,  # Not tracked yet — acceptable stub
    tests_new_passing=0,  # Not tracked yet — acceptable stub
    tests_new_failing=0,  # Not tracked yet — acceptable stub
    features_delivered=[],  # Not tracked yet — acceptable stub
    features_broken=[],  # Not tracked yet — acceptable stub
)
```

**Notes:**
- Several fields are stubbed with 0/empty because the queue runner doesn't track them yet
- This is acceptable per SPEC-PIPELINE-001 — full instrumentation comes later
- The important fields (spec_id, model, cost_usd, wall_time, result) are accurate

### 3. Write tests FIRST (TDD)

**File:** `.deia/hive/scripts/queue/tests/test_ledger_events.py`

**Minimum 8 tests:**

1. `test_emit_validation_event_gate_0_success` — POST with null fidelity_score
2. `test_emit_validation_event_phase_1_pass` — POST with fidelity_score 0.91
3. `test_emit_validation_event_schema` — Verify payload has correct keys/types
4. `test_emit_execution_event_clean_success` — POST with CLEAN result
5. `test_emit_execution_event_timeout` — POST with TIMEOUT result
6. `test_emit_execution_event_schema` — Verify payload has correct keys/types
7. `test_emit_event_http_error` — Mock 500 error, verify silent failure
8. `test_emit_event_timeout` — Mock timeout, verify silent failure

**Test infrastructure:**
- Use `unittest.mock` to mock `urllib.request.urlopen`
- Capture POST payload and verify schema
- No real HTTP calls in tests

---

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All 8 tests pass
- [ ] Edge cases covered:
  - [ ] Null fidelity_score for gate_0
  - [ ] HTTP 500 error handling
  - [ ] Connection timeout handling
  - [ ] Schema validation (all required fields present)
  - [ ] Correct JSON encoding of event data

---

## Acceptance Criteria

- [ ] `ledger_events.py` created with 2 functions, no stubs
- [ ] `emit_validation_event` has 11 parameters, all type-hinted
- [ ] `emit_execution_event` has 16 parameters, all type-hinted
- [ ] Both functions POST to heartbeat endpoint with `status="ledger_event"`
- [ ] Both functions return True/False (success/failure)
- [ ] `emit_execution_event` wired into `run_queue.py` line ~244
- [ ] Import added to `run_queue.py`: `from .ledger_events import emit_execution_event`
- [ ] 8 tests written, all passing
- [ ] No file over 500 lines (ledger_events.py ~40, tests ~120)
- [ ] No hardcoded colors (N/A for this task)
- [ ] Tests run via: `cd .deia/hive/scripts/queue && python -m pytest tests/test_ledger_events.py -v`

---

## Constraints

- **No external dependencies.** Use `urllib.request` from stdlib.
- **No stubs.** All functions fully implemented.
- **File size:** ledger_events.py must be under 500 lines (target ~40).
- **TDD.** Tests first, implementation second.
- **Silent failures.** HTTP errors must not crash the queue runner — log to stderr and return False.
- **No behavior changes.** Queue runner logic is unchanged — this is pure instrumentation.

---

## Event Schema Reference (from SPEC-PIPELINE-001)

### `phase_validation` event

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

### `bee_execution` event

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

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-223-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Notes

- This task is Wave 1-B — no dependencies, can start immediately
- Wave 1-A (PipelineStore protocol) runs in parallel — don't wait for it
- Full instrumentation (tracking tests_before, tests_after, session_id) comes in later waves
- For now, stubbing these fields with 0/empty is acceptable — the critical fields (cost, duration, result) are accurate
- The heartbeat endpoint already accepts arbitrary payloads — no backend changes needed
