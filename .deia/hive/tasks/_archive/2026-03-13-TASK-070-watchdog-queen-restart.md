# TASK-070: Watchdog Queen Restart Logic

## Objective
Implement automatic queen restart when watchdog detects stale heartbeat. New queen resumes work by polling build status.

## Context
Currently, when a queen goes stale (no heartbeat for 15 minutes), the watchdog kills the process and returns TIMEOUT. The queue runner treats this as a failure and may retry the entire spec.

This is wasteful. If a queen was 80% done when it stalled, we want to restart it and let it finish the remaining 20%, not start from scratch.

**Solution:** When watchdog kills a stale queen, automatically relaunch a NEW queen with:
1. Same spec/task content
2. Instruction to poll /build/status to see completed tasks
3. Max 2 restart attempts per queen session

If 2 restarts both timeout, return TIMEOUT and let run_queue.py flag NEEDS_DAVE.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — watchdog, call_dispatch
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — dispatch_bee function
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — BuildState, /build/status endpoint
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — how timeout is handled

## Deliverables

### Watchdog Restart Logic
- [ ] In dispatch_handler.py: when watchdog kills a stale queen, implement restart logic
- [ ] On timeout: kill process, POST timeout heartbeat, then relaunch a NEW queen
- [ ] Add `restart_count` parameter to call_dispatch() (defaults to 0)
- [ ] On first timeout: increment restart_count, prepend resume instruction to task content, relaunch queen
- [ ] On second timeout: increment restart_count again, prepend resume instruction, relaunch queen
- [ ] On third timeout: return (False, None, "TIMEOUT") without relaunch

### Resume Instruction
- [ ] Create helper function: `create_resume_instruction(restart_attempt: int) -> str`
- [ ] Resume instruction tells queen: "Poll http://localhost:8420/build/status to see what tasks are already completed. Only process remaining work."
- [ ] Include restart attempt number in instruction: "This is restart attempt 1/2" or "This is restart attempt 2/2"
- [ ] Prepend resume instruction to original task content before relaunching

### Restart Tracking
- [ ] Add `restart_count` field to call_dispatch signature: `call_dispatch(..., restart_count: int = 0)`
- [ ] Pass restart_count through recursive calls
- [ ] Max 2 restarts total (attempts 1 and 2)
- [ ] After 2 restarts, return TIMEOUT

### Heartbeat Integration
- [ ] After killing stale process, POST timeout heartbeat (already exists)
- [ ] After relaunching queen, POST new "dispatched" heartbeat with message="restart_attempt={N}"
- [ ] Use same task_id for restarted queen (so build monitor shows continuation)

## Test Requirements

### Test File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_handler.py`
Create new test file with test cases:
- [ ] `test_watchdog_detects_stale_heartbeat` — Mock stale heartbeat, verify _is_heartbeat_stale returns True
- [ ] `test_watchdog_kills_process_on_timeout` — Mock stale heartbeat, verify process.kill() is called
- [ ] `test_watchdog_restart_attempt_1` — Mock first timeout, verify queen is relaunched with resume instruction
- [ ] `test_watchdog_restart_attempt_2` — Mock second timeout, verify queen is relaunched again
- [ ] `test_watchdog_max_retries` — Mock third timeout, verify TIMEOUT is returned without relaunch
- [ ] `test_resume_instruction_format` — Verify resume instruction includes build status URL and attempt number

### Edge Cases
- [ ] First restart: restart_count=0, after timeout restart_count=1, relaunch
- [ ] Second restart: restart_count=1, after timeout restart_count=2, relaunch
- [ ] Third timeout: restart_count=2, no relaunch, return TIMEOUT
- [ ] Resume instruction is prepended to task content, not appended
- [ ] Same task_id is used for all restart attempts

## Constraints
- **No file over 500 lines** — dispatch_handler.py is currently 237 lines, should stay under 500
- **Do NOT break existing watchdog** — if restart logic fails, fallback to current behavior (kill + TIMEOUT)
- **CSS: var(--sd-*) only** — not applicable (backend only)
- **No stubs** — all functions fully implemented
- **Conservative error handling** — if relaunch fails, log error and return TIMEOUT

## Acceptance Criteria

### Fix 11: Watchdog queen restart
- [ ] In dispatch_handler.py: when watchdog kills a stale queen (no heartbeat for 15 min), instead of just returning TIMEOUT, implement restart logic
- [ ] On timeout: kill process, POST timeout heartbeat, then relaunch a NEW queen with the same queue directory
- [ ] New queen's task includes instruction: "Poll http://localhost:8420/build/status to see what tasks are already completed. Only process remaining work."
- [ ] Max 2 restart attempts per queen session. After 2 restarts, return TIMEOUT and let run_queue.py flag NEEDS_DAVE
- [ ] Add `restart_count` tracking in call_dispatch
- [ ] Test: mock stale heartbeat, verify process is killed and relaunched (mock the relaunch)

### General
- [ ] All existing tests still pass
- [ ] 5+ new tests for restart logic
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-070-RESPONSE.md`

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

## Model Assignment
sonnet

## Test Commands
```bash
# Dispatch handler tests
cd .deia/hive/scripts/queue && python -m pytest tests/test_dispatch_handler.py -v

# Queue runner integration tests (verify no regressions)
cd .deia/hive/scripts/queue && python -m pytest tests/ -v
```

## Implementation Notes

### Current Behavior
```python
# dispatch_handler.py:141
if timed_out:
    return False, None, "TIMEOUT"
```

### New Behavior
```python
# dispatch_handler.py (after changes)
if timed_out:
    if restart_count < 2:
        # Create resume instruction
        resume_inst = create_resume_instruction(restart_count + 1)
        # Read original task content
        original_task = temp_task_path.read_text(encoding="utf-8")
        # Prepend resume instruction
        resumed_task = resume_inst + "\n\n---\n\n" + original_task
        # Write back to temp file
        temp_task_path.write_text(resumed_task, encoding="utf-8")
        # POST restart heartbeat
        send_heartbeat(task_id, "dispatched", model=regent_model, message=f"restart_attempt={restart_count + 1}")
        # Recursive call with incremented restart_count
        return self.call_dispatch(temp_task_path, regent_model, timeout, spec_id, restart_count=restart_count + 1)
    else:
        # Max retries exhausted
        return False, None, "TIMEOUT"
```

### Resume Instruction Template
```python
def create_resume_instruction(restart_attempt: int) -> str:
    return f"""## WATCHDOG RESTART — Attempt {restart_attempt}/2

A previous queen timed out on this task. You are the restart queen.

**Your job:**
1. Poll http://localhost:8420/build/status to see what tasks are already completed
2. Review the completed work
3. Finish any remaining tasks
4. Do NOT redo work that is already done

This is restart attempt {restart_attempt}/2.

---
"""
```
