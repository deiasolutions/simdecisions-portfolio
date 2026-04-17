# BUG-045: Queue Runner Crash Resilience — Task Files Ready

**Date:** 2026-03-18
**From:** Q33N
**To:** Q33NR
**Status:** READY FOR REVIEW

---

## Summary

I have broken down BUG-045 (Queue Runner Crash Resilience) into 5 task files, following the TDD approach. All tasks focus on adding exception handling to critical sections of the queue runner without changing any queue logic or dispatch behavior.

## Task Breakdown

### TASK-BUG-045-A: Watch loop resilience
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-045-A-watch-loop-resilience.md`
**Objective:** Wrap the watch loop (while watch:) in run_queue.py with broad exception handling so that any tick failure logs an error and continues instead of killing the runner.
**Model:** sonnet (complex integration work)
**Tests:** 6 tests (mock failures in load_queue, cleanup_stale, process_pool, plus KeyboardInterrupt passthrough)

### TASK-BUG-045-B: Result handler resilience
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-045-B-result-handler-resilience.md`
**Objective:** Add exception handling to _handle_spec_result() around file moves, fix spec generation, and timeout resume creation so one bad spec doesn't kill the queue.
**Model:** sonnet (intricate state machine with 3 branches)
**Tests:** 5 tests (file move failures, fix spec generation failures, timeout resume failures)

### TASK-BUG-045-C: Fix cycle I/O resilience
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-045-C-fix-cycle-io-resilience.md`
**Objective:** Wrap file write operations in fix_cycle.py (generate_fix_spec, generate_q33n_fix_spec) with exception handlers, return None on failure instead of raising.
**Model:** haiku (straightforward file I/O wrapping)
**Tests:** 3 tests (disk full, permission denied, verify None return)

### TASK-BUG-045-D: Dispatch subprocess resilience
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-045-D-dispatch-subprocess-resilience.md`
**Objective:** Verify and enhance exception handling around handler.call_dispatch() in spec_processor.py to ensure all subprocess failures return SpecResult(NEEDS_DAVE) instead of propagating.
**Model:** haiku (verification + small enhancements)
**Tests:** 4 tests (OSError, TimeoutExpired, verify temp cleanup, verify error logging)

### TASK-BUG-045-E: Integration tests
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-045-E-integration-tests.md`
**Objective:** Write end-to-end integration tests that verify the queue runner survives common failure scenarios (malformed specs, network failures, file errors, KeyboardInterrupt).
**Model:** sonnet (complex integration test suite with subprocess management)
**Tests:** 6 integration tests (malformed spec, missing file, hivenode unreachable, rename failure, KeyboardInterrupt, cascading failures)

## Dependency Order

Suggested execution order:
1. **BUG-045-C** (fix_cycle.py) — isolated, no dependencies
2. **BUG-045-D** (spec_processor.py) — isolated, no dependencies
3. **BUG-045-B** (result handler) — depends on BUG-045-C changes (fix_cycle returns None)
4. **BUG-045-A** (watch loop) — depends on BUG-045-B changes (result handler resilience)
5. **BUG-045-E** (integration tests) — depends on ALL prior tasks

**Parallel execution:** BUG-045-C and BUG-045-D can run in parallel (different files, no conflicts).

## Test Count Estimate

- BUG-045-A: 6 unit tests
- BUG-045-B: 5 unit tests
- BUG-045-C: 3 unit tests
- BUG-045-D: 4 unit tests
- BUG-045-E: 6 integration tests
- **Total: 24 new tests**

All tests use pytest. All tests follow TDD (write tests first, then implementation).

## Files Modified (Projected)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (BUG-045-A, BUG-045-B)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (BUG-045-C)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (BUG-045-D)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue_resilience.py` (BUG-045-A, new)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_result_handler_resilience.py` (BUG-045-B, new)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_fix_cycle_resilience.py` (BUG-045-C, new)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_spec_processor_resilience.py` (BUG-045-D, new)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_queue_crash_resilience.py` (BUG-045-E, new)

## Smoke Test

After all tasks complete:
```bash
python -m pytest .deia/hive/scripts/queue/tests/ -v
```

Expected: 24 new tests pass, all existing queue tests still pass.

## Review Checklist for Q33NR

- [ ] All 5 task files include absolute file paths
- [ ] All tasks specify TDD (tests first)
- [ ] No task allows stubs or incomplete implementations
- [ ] All tasks constrain changes to error handling only (no logic changes)
- [ ] All tasks require logging with `[QUEUE] ERROR:` prefix
- [ ] All tasks require 8-section response files
- [ ] Dependency order is clear (C+D parallel → B → A → E)
- [ ] Test count estimate is realistic (24 tests total)
- [ ] KeyboardInterrupt handling is explicitly called out (NOT caught)

## Next Steps

Awaiting Q33NR approval to dispatch bees.

Once approved:
1. Dispatch BUG-045-C and BUG-045-D in parallel (haiku, independent)
2. After both complete, dispatch BUG-045-B (sonnet, depends on C)
3. After BUG-045-B completes, dispatch BUG-045-A (sonnet, depends on B)
4. After BUG-045-A completes, dispatch BUG-045-E (sonnet, integration tests for all)
5. Run full test suite, verify 24 new tests pass
6. Report completion to Q33NR

---

**Q33N Note:** This is a critical infrastructure fix. Every exception must be caught and logged. The queue runner is the automation backbone — it MUST be bulletproof. No shortcuts.
