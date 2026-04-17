# TASK-BUG-045-A: Wrap watch loop in exception handler

## Objective
Add top-level exception handling to the watch loop in `run_queue()` so that any uncaught exception during a tick logs an error and continues running instead of killing the entire queue runner.

## Context
The queue runner's watch mode (`run_queue()` at line 928) contains a `while watch` loop that polls for new specs every N seconds. Currently, if any exception occurs during a polling tick (network error, file I/O error, malformed spec, etc.), the entire runner exits and the queue stalls.

This task wraps the watch loop's iteration body in a broad try/except that catches `Exception` (NOT `BaseException` — let KeyboardInterrupt through) and logs the error with full traceback before continuing to the next tick.

**Architecture:** The watch loop starts at line 1045 and contains several operations:
- Cleanup stale reservations (line 1047)
- Load queue from disk (line 1058)
- Check for active hive tasks (line 1061)
- Sleep (line 1088)
- Rescan queue (line 1091)
- Process specs via pool (line 1112)

ALL of these must be protected by the exception handler.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (lines 1045-1119, the watch loop)

## Deliverables
- [ ] Watch loop (while watch:) wrapped in try/except Exception
- [ ] Exception handler logs `[QUEUE] ERROR:` prefix + traceback via `import traceback; traceback.print_exc()`
- [ ] Exception handler logs spec ID (if available) or "watch-tick" as context
- [ ] Exception does NOT propagate (queue continues running)
- [ ] KeyboardInterrupt is NOT caught (let Ctrl-C stop the queue)
- [ ] Test: raise exception mid-tick, verify queue continues after logging error

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass (run_queue.py tests)
- [ ] New test: mock `load_queue()` to raise `FileNotFoundError`, verify runner continues
- [ ] New test: mock `_cleanup_stale_reservations()` to raise `ConnectionError`, verify runner continues
- [ ] New test: mock `_process_queue_pool()` to raise `ValueError`, verify runner continues
- [ ] New test: raise `KeyboardInterrupt`, verify runner exits (not caught)
- [ ] Edge case: verify error message includes spec context when available

## Constraints
- No file over 500 lines
- Do not change queue logic or dispatch behavior
- Only add error handling and resilience
- Log everything — silent failures are worse than crashes
- All file paths must be absolute in task files
- TDD: Write tests first, then implementation
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-045-A-RESPONSE.md`

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
