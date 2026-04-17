# TASK-223: Validation Ledger Events — Schema + Emission (W1-B)

## Objective
Add `phase_validation` and `bee_execution` event types to the Event Ledger with helper functions for emitting these events, and wire into existing code paths.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). Every pipeline stage must emit to the Event Ledger. This task defines the event schemas and wires emission into existing fidelity check and bee dispatch code paths.

The Event Ledger tracks two categories of events:
1. **Validation events** (`phase_validation`) — emitted during Gate 0, Phase 0, Phase 1, Phase 2 (IR fidelity checks)
2. **Execution events** (`bee_execution`) — emitted when bees complete their work

These events enable analysis like: "Does the IR round-trip actually reduce bee failure rate enough to justify its token cost?"

## Source Spec
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 3.1 (event schemas)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — existing dispatch/completion code paths
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — bee dispatch logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — existing heartbeat/event infrastructure

## Deliverables

### 1. Event Emission Module
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\ledger_events.py`

**Functions:**
- [ ] `emit_validation_event(spec_id, phase, fidelity_score, tokens_in, tokens_out, model, cost_usd, attempt, result, healing_attempts, wall_time_seconds)`
  - POST to `http://127.0.0.1:8420/build/heartbeat` with event schema from Section 3.1
  - Schema fields (exact match required):
    - `event_type`: "phase_validation"
    - `spec_id`: str
    - `phase`: "gate_0" | "phase_0" | "phase_1" | "phase_2"
    - `fidelity_score`: float (null for gate_0)
    - `tokens_in`: int
    - `tokens_out`: int
    - `model`: str
    - `cost_usd`: float
    - `attempt`: int (1 = first try, 2+ = healing retry)
    - `result`: "PASS" | "FAIL" | "HEALED"
    - `healing_attempts`: int
    - `wall_time_seconds`: int

- [ ] `emit_execution_event(spec_id, task_id, bee_id, model, session_id, tokens_in, tokens_out, cost_usd, wall_time_seconds, result, tests_before, tests_after, tests_new_passing, tests_new_failing, features_delivered, features_broken)`
  - POST to `http://127.0.0.1:8420/build/heartbeat` with event schema from Section 3.1
  - Schema fields (exact match required):
    - `event_type`: "bee_execution"
    - `spec_id`: str
    - `task_id`: str
    - `bee_id`: str
    - `model`: str
    - `session_id`: str
    - `tokens_in`: int
    - `tokens_out`: int
    - `cost_usd`: float
    - `wall_time_seconds`: int
    - `result`: "CLEAN" | "TIMEOUT" | "NEEDS_DAVE" | "CRASH"
    - `tests_before`: int
    - `tests_after`: int
    - `tests_new_passing`: int
    - `tests_new_failing`: int
    - `features_delivered`: list[str]
    - `features_broken`: list[str]

**Implementation Requirements:**
- Use `urllib.request` for HTTP POST (no external dependencies)
- Graceful failure: log errors but never crash caller
- Timeout: 5 seconds max per POST
- Return True on success, False on failure

### 2. Wire Execution Events into Dispatch Handler
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py`

- [ ] Import `emit_execution_event` from `ledger_events.py`
- [ ] In `parse_response_header()` method: extract test counts from response file
  - Look for patterns: `Tests: XX passed` or `tests_before: XX`, `tests_after: YY`
- [ ] After successful bee completion (when response file is parsed):
  - Call `emit_execution_event()` with all required fields
  - Compute deltas: `tests_new_passing = max(0, tests_after - tests_before)`
  - For now, pass empty lists for `features_delivered` and `features_broken` (TODO for Wave 2)

### 3. Test Suite
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_ledger_events.py`

**Tests (minimum 8):**
- [ ] `test_emit_validation_event_success` — mock HTTP POST, verify payload schema
- [ ] `test_emit_validation_event_null_fidelity_gate0` — gate_0 allows null fidelity_score
- [ ] `test_emit_validation_event_network_error` — returns False on timeout
- [ ] `test_emit_execution_event_success` — mock HTTP POST, verify payload schema
- [ ] `test_emit_execution_event_all_fields` — verify all 16 fields present
- [ ] `test_emit_execution_event_empty_features` — empty lists for features_delivered/broken
- [ ] `test_emit_execution_event_timeout` — returns False on timeout
- [ ] `test_event_emission_does_not_crash_caller` — exceptions handled gracefully

**Test Infrastructure:**
- Use `unittest.mock.patch` to mock `urllib.request.urlopen`
- Verify JSON payload structure matches SPEC-PIPELINE-001 Section 3.1
- Verify HTTP headers: `Content-Type: application/json`
- Verify URL: `http://127.0.0.1:8420/build/heartbeat`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Null fidelity_score for gate_0
  - Network timeouts
  - Empty feature lists
  - Very long spec_id strings
  - Zero test counts

## Constraints
- **No stubs.** Every function must be fully implemented.
- **No file over 500 lines.** If `ledger_events.py` exceeds 500 lines, modularize.
- **No hardcoded colors.** (N/A for this task — backend only)
- **Absolute paths only** in this doc and in code comments
- **TDD required** — write tests first, then implementation

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-223-RESPONSE.md`

The response MUST contain these 8 sections:

### 1. Header
Task ID, title, status (COMPLETE/FAILED), model, date

### 2. Files Modified
Every file created/modified/deleted, full absolute paths

### 3. What Was Done
Bullet list of concrete changes (not intent)

### 4. Test Results
- Test files run
- Pass/fail counts
- If no tests, state why

### 5. Build Verification
- Did tests pass? Include summary line.
- Did build pass? Include last 5 lines.

### 6. Acceptance Criteria
Copy from task, mark [x] done or [ ] not done with explanation

### 7. Clock / Cost / Carbon
- **Clock:** wall time
- **Cost:** estimated USD
- **Carbon:** estimated CO2e

### 8. Issues / Follow-ups
Anything that didn't work, edge cases, recommended next tasks

DO NOT skip any section.

## Priority
P1

## Model Assignment
haiku
