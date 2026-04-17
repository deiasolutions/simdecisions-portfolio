# BRIEFING: BL-056 — Automated overnight build pipeline improvements

**To:** Q33N
**From:** Q88NR
**Date:** 2026-03-18
**Priority:** P0

---

## Objective

Improve the automated build pipeline so it can run overnight unattended, processing queued specs, dispatching bees, and reporting results.

## Current State Analysis

I've reviewed the queue runner infrastructure:

### What Exists
- **run_queue.py** (1179 lines) — Main queue orchestration with pool-based bee dispatch, hot-reload, dependency tracking, watch mode, Fibonacci backoff
- **spec_processor.py** (547 lines) — Dispatch integration via DispatchHandler, baseline capture, post-bee verification
- **spec_parser.py** (189 lines) — Spec file parsing with priority, hold-until, dependencies
- **morning_report.py** (249 lines) — Session report generation
- **dispatch_handler.py** — Regent prompt loading, temp task file creation, dispatch.py subprocess calls, response parsing
- **test_runner.py** — Full test suite execution for verification gates

### What Works Well
- Pool-based backfill processing — specs dispatch into available slots, not batch-wait
- Stale process detection — watchdog kills bees that don't heartbeat for 15 minutes (dispatch_handler.py)
- Hot-reload — rescan queue directory every completion, add new specs dynamically
- Dependency tracking — specs block until dependencies in _done/
- Fix cycle logic — auto-generate fix specs on failures (max 2 cycles per root spec)
- Timeout retry — auto-resume timed-out specs with resume instruction (max 2 retries)
- Morning report — aggregates session events into markdown summary

### What Needs Improvement (Per Spec)

The spec requests:
1. **Error recovery: retry failed dispatches with backoff**
2. **Stale process detection: kill bees that exceed timeout**
3. **Result aggregation: collect all response files per batch**
4. **Morning report: summary of overnight results**
5. **Tests for error recovery and stale detection**

**ANALYSIS:**
- **Stale process detection** — ALREADY IMPLEMENTED (dispatch_handler.py watchdog, 15-min heartbeat timeout)
- **Morning report** — ALREADY IMPLEMENTED (morning_report.py, called by run_queue.py)
- **Result aggregation** — ALREADY IMPLEMENTED (run_queue.py collects all SpecResults, logs to session JSON)

**WHAT'S MISSING:**
- **Retry with backoff on transient dispatch failures** — Currently, only timeout gets retry (2x). Non-timeout failures (subprocess crash, file I/O errors, network errors) go straight to fix cycle. Need exponential backoff retry for transient errors.
- **Tests for error recovery and stale detection** — No test coverage for watchdog timeout, retry backoff, or dispatch failure scenarios.

---

## Deliverables

Q33N, create task files for:

### TASK-BL-056-A: Retry with backoff on transient dispatch failures
- **File:** `.deia/hive/scripts/queue/dispatch_retry.py`
- **Function:** `retry_with_backoff(fn, max_attempts=3, backoff_base=2.0) -> tuple[bool, result, error]`
  - Wraps callable `fn`, retries on exception
  - Exponential backoff: 2s, 4s, 8s (configurable)
  - Returns (success, result, error_msg)
- **Integration:** Modify `dispatch_handler.py:call_dispatch()` to use retry wrapper
- **Transient errors:** Subprocess timeout, file not found (temp task cleanup race), network errors
- **Non-transient errors:** Response file parse failure, dispatch exit code != 0
- **Tests:** 12+ tests in `tests/test_dispatch_retry.py`
  - Retry on transient error (success on attempt 2)
  - Exhaust retries (3 attempts, all fail)
  - Immediate success (no retry)
  - Backoff timing verification (measure sleep durations)
  - Non-transient error (no retry)

### TASK-BL-056-B: Tests for watchdog stale detection
- **File:** `.deia/hive/scripts/queue/tests/test_watchdog_stale_detection.py`
- **Coverage:**
  - Watchdog kills bee after 15-min heartbeat gap
  - Watchdog respects heartbeat renewal
  - Watchdog cleanup on process termination
  - Response file marked as TIMEOUT when watchdog triggers
- **Tests:** 8+ tests
- **Mock strategy:** Use `time.time()` mock to simulate heartbeat gaps without 15-min wait

### TASK-BL-056-C: Integration tests for overnight queue processing
- **File:** `.deia/hive/scripts/queue/tests/test_queue_overnight.py`
- **Coverage:**
  - Queue drains, watch mode polls, finds new spec, processes it
  - Dependency blocking — spec B waits for spec A to reach _done/
  - Fibonacci backoff in watch mode (adaptive=True)
  - Hot-reload during active pool processing
  - Budget exhaustion stops new dispatches
  - Session report generated on empty queue
- **Tests:** 10+ tests
- **Mock strategy:** Mock `process_spec_no_verify()` to return instant SpecResult, no real bee dispatch

---

## Acceptance Criteria

- [ ] Transient dispatch failures retry up to 3 times with exponential backoff (2s, 4s, 8s)
- [ ] Watchdog stale detection has test coverage (8+ tests)
- [ ] Overnight queue processing has integration test coverage (10+ tests)
- [ ] All new tests pass
- [ ] No file over 500 lines
- [ ] No stubs

---

## Files to Create

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_retry.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_retry.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_watchdog_stale_detection.py`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_queue_overnight.py`

---

## Files to Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py`
   - Integrate `retry_with_backoff()` wrapper in `call_dispatch()`
   - Import from `dispatch_retry.py`

---

## Constraints

- No file over 500 lines
- No stubs — all functions fully implemented
- TDD — tests written first, then implementation

---

## Model Assignment

**sonnet** (complex integration, test design)

---

## Notes

The queue runner is already robust:
- Watchdog timeout detection works
- Morning report works
- Result aggregation works
- Hot-reload works
- Dependency tracking works

This spec adds missing pieces:
- **Retry backoff** for transient dispatch errors (currently missing)
- **Test coverage** for watchdog and overnight scenarios (currently missing)

The improvements are additive — no breaking changes to existing logic.

---

## Next Steps

Q33N, write 3 task files:
1. `TASK-BL-056-A-RETRY-WITH-BACKOFF.md`
2. `TASK-BL-056-B-WATCHDOG-TESTS.md`
3. `TASK-BL-056-C-OVERNIGHT-INTEGRATION-TESTS.md`

Each task file must include:
- Absolute file paths (Windows format)
- Test count and scenarios
- Integration points (which files to modify)
- Response file template (8-section format)

**Submit task files to `.deia/hive/tasks/` when ready for my review.**

---

**Q88NR-bot**
