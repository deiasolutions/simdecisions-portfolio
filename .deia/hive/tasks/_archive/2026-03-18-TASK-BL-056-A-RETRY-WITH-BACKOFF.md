# TASK-BL-056-A: Retry with backoff on transient dispatch failures

## Objective
Create a retry wrapper with exponential backoff for transient dispatch failures in the queue runner, reducing false-negative failures from temporary network/filesystem issues.

## Context
The queue runner currently has two error recovery paths:
1. **Timeout retry** — If a bee times out (watchdog kills it after 8 minutes of no heartbeat), the queue runner automatically restarts the bee up to 2 times with resume instruction
2. **Fix cycle** — If a bee fails (non-timeout error), the queue runner generates a fix spec for Q33N to diagnose and fix

**Gap:** Transient failures (subprocess crash, file I/O race, network error) immediately trigger fix cycle even though they might succeed on retry. This wastes Q33N cycles on transient issues.

**Solution:** Add exponential backoff retry for transient errors in `call_dispatch()` before falling back to fix cycle.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` (508 lines) — Integration point: `call_dispatch()` method wraps dispatch.py subprocess
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_handler.py` — Existing test patterns

## Deliverables

### Module: dispatch_retry.py
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_retry.py`
- [ ] Function: `retry_with_backoff(fn: callable, max_attempts: int = 3, backoff_base: float = 2.0) -> tuple[bool, any, Optional[str]]`
  - Wraps callable `fn` with retry logic
  - Returns `(success: bool, result: any, error_msg: Optional[str])`
  - On success: `(True, result, None)`
  - On exhausted retries: `(False, None, last_error_msg)`
- [ ] Exponential backoff: 2s, 4s, 8s (configurable via `backoff_base`)
- [ ] Sleep between attempts: `time.sleep(backoff_base ** (attempt - 1))`
- [ ] Attempt logging: Print attempt number and error before each retry
- [ ] Final error: Return last exception message on exhaustion

### Integration: dispatch_handler.py
- [ ] Modify `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py`
- [ ] Import `retry_with_backoff` from `.dispatch_retry`
- [ ] Wrap subprocess call in `call_dispatch()` with retry wrapper
- [ ] Classify errors as transient vs non-transient:
  - **Transient** (retry-eligible): `subprocess.TimeoutExpired`, `FileNotFoundError` (temp task cleanup race), `ConnectionError`, `urllib.error.URLError`
  - **Non-transient** (no retry): Response file parse failure, dispatch exit code != 0 (bee returned failure)
- [ ] Only wrap transient failures — if dispatch returns non-zero exit code but no exception, don't retry (bee intentionally failed)

## Test Requirements

### Test file: test_dispatch_retry.py
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_retry.py`
- [ ] **TDD:** Write tests FIRST, then implementation
- [ ] Test count: **12 minimum**

### Test scenarios:
1. **Immediate success** — Callable succeeds on first attempt, no retry
2. **Success on attempt 2** — Callable fails once, succeeds on second attempt
3. **Success on attempt 3** — Callable fails twice, succeeds on third attempt
4. **Exhaust retries** — Callable fails 3 times, returns `(False, None, error_msg)`
5. **Backoff timing** — Verify sleep durations (2s, 4s, 8s) using `time.time()` or mock
6. **Custom backoff base** — Test with `backoff_base=3.0` (3s, 9s, 27s)
7. **Custom max attempts** — Test with `max_attempts=2` (only 2 attempts)
8. **Return value passthrough** — Verify successful result is returned unchanged
9. **Exception passthrough** — Verify final exception message is returned
10. **Multiple exception types** — Test different exception types on different attempts
11. **Zero attempts edge case** — `max_attempts=1` should run once, no retry
12. **Callable with args/kwargs** — Verify callable receives arguments correctly

### Mock strategy:
- Use `unittest.mock.Mock` to create controllable callables
- Use `side_effect` to simulate failure sequences: `[Exception("err1"), Exception("err2"), "success"]`
- Use `unittest.mock.patch("time.sleep")` to verify backoff timing without waiting

## Constraints
- No file over 500 lines
- No stubs — all functions fully implemented
- TDD — tests written first
- No hardcoded colors (N/A for Python)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-056-A-RESPONSE.md`

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

## Acceptance Criteria
- [ ] `dispatch_retry.py` created with `retry_with_backoff()` function
- [ ] Exponential backoff implemented (2s, 4s, 8s default)
- [ ] `dispatch_handler.py` integrated with retry wrapper
- [ ] Transient vs non-transient error classification implemented
- [ ] 12+ tests written and passing
- [ ] All tests pass
- [ ] No file over 500 lines
- [ ] No stubs shipped

## Model Assignment
**haiku** — straightforward retry logic, clear test patterns
