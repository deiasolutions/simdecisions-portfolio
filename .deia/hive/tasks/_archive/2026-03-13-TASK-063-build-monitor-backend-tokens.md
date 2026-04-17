# TASK-063: Build Monitor Backend Token Tracking

**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Model:** sonnet
**Priority:** P0

---

## Objective

Add token tracking to the build monitor backend: update HeartbeatPayload model, BuildState accumulation, and dispatch.py to pass token data from adapter results.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — HeartbeatPayload model, BuildState class
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — send_heartbeat function, adapter result parsing

---

## Deliverables (absolute paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — MODIFIED
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — MODIFIED
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_build_monitor.py` — MODIFIED

---

## Acceptance Criteria

### HeartbeatPayload (build_monitor.py)
- [ ] Add `input_tokens: Optional[int] = None` field
- [ ] Add `output_tokens: Optional[int] = None` field

### BuildState.record_heartbeat (build_monitor.py)
- [ ] Accumulate `input_tokens` per task (sum all heartbeats for that task)
- [ ] Accumulate `output_tokens` per task (sum all heartbeats for that task)
- [ ] Add `total_input_tokens` instance var (defaults to 0)
- [ ] Add `total_output_tokens` instance var (defaults to 0)
- [ ] Update `total_input_tokens` and `total_output_tokens` when heartbeat includes tokens
- [ ] Store `input_tokens` and `output_tokens` in task dict under keys `input_tokens` and `output_tokens`

### BuildState.get_status (build_monitor.py)
- [ ] Include `total_input_tokens` and `total_output_tokens` in returned dict

### dispatch.py send_heartbeat function
- [ ] Add `input_tokens: int = None` parameter
- [ ] Add `output_tokens: int = None` parameter
- [ ] Include both fields in the POST payload dict

### dispatch.py completion heartbeat (dispatch_bee function)
- [ ] After `adapter.send_task()` returns, parse `input_tokens` and `output_tokens` from `result.get("usage") or {}` dict
- [ ] Pass both to the completion heartbeat via `send_heartbeat(..., input_tokens=..., output_tokens=...)`

---

## Tests (test_build_monitor.py)

Add 4+ tests:
- [ ] Test HeartbeatPayload accepts `input_tokens` and `output_tokens` fields
- [ ] Test BuildState.record_heartbeat accumulates tokens per task
- [ ] Test BuildState.record_heartbeat accumulates total tokens across all tasks
- [ ] Test BuildState.get_status returns `total_input_tokens` and `total_output_tokens`

Run existing tests to ensure no regressions:
- [ ] All existing build_monitor tests pass

---

## Constraints

- Do NOT change the heartbeat API contract in a breaking way — new fields are optional
- Do NOT change the SSE event format — same event types, richer payloads
- Keep build_monitor.py under 250 lines

---

## TDD Protocol

1. Write tests first (4+ tests in test_build_monitor.py)
2. Run tests (should fail)
3. Implement changes in build_monitor.py
4. Implement changes in dispatch.py
5. Run tests (should pass)
6. Run full hivenode test suite to ensure no regressions

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 4+ new tests written and passing
- [ ] All existing build_monitor tests passing
- [ ] No hardcoded colors (not applicable to backend)
- [ ] Response file written to `.deia/hive/responses/`
