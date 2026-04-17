# TASK-BL-056-B: Tests for watchdog stale detection

## Objective
Add comprehensive test coverage for the queue runner's watchdog stale detection mechanism, which kills bees that stop heartbeating for 15 minutes (currently at 8 minutes via `WATCHDOG_STALE_SECONDS = 480`).

## Context
The watchdog is ALREADY IMPLEMENTED in `dispatch_handler.py`:
- `call_dispatch()` polls heartbeat freshness every 30 seconds (`WATCHDOG_POLL_SECONDS`)
- `_is_heartbeat_stale()` checks if last heartbeat is older than 480 seconds (8 minutes)
- If stale, watchdog kills the process, POSTs timeout heartbeat, and auto-restarts up to 2 times

**Gap:** No test coverage for this critical mechanism. If the watchdog breaks, bees can hang forever.

**Solution:** Add comprehensive test suite that mocks `time.time()` and `urllib.request.urlopen()` to simulate heartbeat gaps without waiting 8 minutes.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` (508 lines) — Implementation: `_is_heartbeat_stale()`, `call_dispatch()` watchdog loop
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_handler.py` — Existing test patterns

## Deliverables

### Test file: test_watchdog_stale_detection.py
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_watchdog_stale_detection.py`
- [ ] **TDD approach:** Since implementation exists, these are regression tests to lock in behavior
- [ ] Test count: **8 minimum**

### Test scenarios:
1. **Fresh heartbeat** — `_is_heartbeat_stale()` returns `False` when last_heartbeat is recent (< 480s ago)
2. **Stale heartbeat** — `_is_heartbeat_stale()` returns `True` when last_heartbeat is 481+ seconds ago
3. **Fallback to last_seen** — `_is_heartbeat_stale()` uses `last_seen` timestamp when `last_heartbeat` is missing (backward compat)
4. **Task not in monitor** — `_is_heartbeat_stale()` returns `False` when task_id not found in build monitor response (task hasn't started yet)
5. **Monitor unreachable** — `_is_heartbeat_stale()` returns `False` when HTTP request fails (don't kill on monitor failure)
6. **Watchdog kills process** — Integration test: Mock stale heartbeat, verify `proc.kill()` called
7. **Timeout heartbeat sent** — Verify `_send_timeout_heartbeat()` POSTs correct payload after kill
8. **Restart on timeout** — Verify `call_dispatch()` recursively calls itself after timeout with `restart_count + 1`

### Mock strategy:
- **Time mocking:** Use `unittest.mock.patch("time.time")` to simulate elapsed time without waiting
- **HTTP mocking:** Use `unittest.mock.patch("urllib.request.urlopen")` to mock build monitor responses
- **Process mocking:** Use `unittest.mock.patch("subprocess.Popen")` to mock dispatch.py subprocess
- **Build monitor response:** Mock JSON payloads with `last_heartbeat`, `last_seen`, `task_id` fields

### Example test structure:
```python
def test_is_heartbeat_stale_recent():
    """Heartbeat within 480s is not stale."""
    handler = DispatchHandler(repo_root)
    now = datetime.now()
    recent = (now - timedelta(seconds=300)).isoformat()  # 5 minutes ago

    mock_response = {
        "active": [{"task_id": "TEST-001", "last_heartbeat": recent}]
    }

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(mock_response).encode()
        result = handler._is_heartbeat_stale("TEST-001")

    assert result is False
```

## Test Requirements
- [ ] **TDD approach:** Write tests to verify existing behavior (regression lock-in)
- [ ] All tests pass
- [ ] Edge cases covered: missing fields, HTTP errors, subprocess errors
- [ ] Mock strategy: No actual HTTP calls, no real subprocess spawns, no 8-minute waits

## Constraints
- No file over 500 lines
- No stubs — all test assertions fully implemented
- No hardcoded colors (N/A for Python)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-056-B-RESPONSE.md`

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
- [ ] `test_watchdog_stale_detection.py` created
- [ ] 8+ tests written and passing
- [ ] Fresh heartbeat test passes
- [ ] Stale heartbeat test passes
- [ ] Fallback to last_seen test passes
- [ ] Task not in monitor test passes
- [ ] Monitor unreachable test passes
- [ ] Watchdog kill integration test passes
- [ ] Timeout heartbeat POST test passes
- [ ] Restart recursion test passes
- [ ] All tests use mocks (no real HTTP, no real subprocess)
- [ ] No file over 500 lines
- [ ] No stubs shipped

## Model Assignment
**haiku** — straightforward test patterns, existing implementation to verify
