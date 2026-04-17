# TASK-BUG-045-E: Write integration tests for crash resilience

## Objective
Write end-to-end integration tests that verify the queue runner survives common failure scenarios and continues processing specs instead of exiting.

## Context
After TASK-BUG-045-A through BUG-045-D add exception handling to critical sections, this task verifies the queue runner's crash resilience end-to-end.

Integration tests should:
1. Start a real queue runner in watch mode
2. Inject a failure (bad spec file, missing directory, network timeout)
3. Verify the runner logs the error and continues (doesn't exit)
4. Verify subsequent specs are still processed

**Test approach:**
- Use temporary queue directories
- Write malformed spec files (invalid YAML, missing fields)
- Mock network failures (hivenode unreachable)
- Mock file system errors (PermissionError during rename)
- Check runner stdout/stderr for `[QUEUE] ERROR:` messages
- Verify runner process is still alive after error
- Verify subsequent specs in queue are picked up and processed

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (entire file, to understand watch mode)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue.py` (if exists, for existing test patterns)

## Deliverables
- [ ] New test file: `.deia/hive/scripts/queue/tests/test_queue_crash_resilience.py`
- [ ] Test: malformed spec file (invalid YAML) → runner logs error, continues
- [ ] Test: spec file disappears mid-processing → runner logs error, continues
- [ ] Test: hivenode unreachable (mock urllib failure) → runner logs error, continues
- [ ] Test: file rename fails (PermissionError) → runner logs error, continues
- [ ] Test: KeyboardInterrupt → runner exits cleanly (not caught as generic exception)
- [ ] Test: multiple failures in sequence → runner processes all, logs all errors
- [ ] All error messages contain `[QUEUE] ERROR:` prefix
- [ ] All tests pass: `python -m pytest .deia/hive/scripts/queue/tests/test_queue_crash_resilience.py -v`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Use temporary directories for queue, config, repo root
- [ ] Mock hivenode HTTP endpoints (urllib.request.urlopen)
- [ ] Use subprocess.Popen to start queue runner, send SIGINT for KeyboardInterrupt test
- [ ] Verify runner process still alive after non-fatal errors
- [ ] Clean up all temporary files and processes in teardown
- [ ] Edge case: verify runner survives cascading failures (multiple specs fail in parallel)

## Constraints
- No file over 500 lines
- Use pytest fixtures for temp directories and process management
- All mocks must be cleaned up in teardown
- Log everything — capture runner stdout/stderr for debugging failures
- TDD: Write tests first, then run against BUG-045-A/B/C/D implementations
- No stubs — every test fully implemented
- Tests must be runnable in CI (no hardcoded paths, no manual intervention)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-045-E-RESPONSE.md`

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
