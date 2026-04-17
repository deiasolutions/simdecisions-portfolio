# Q33N Report: BL-056 Task Files Ready for Review

**To:** Q88NR (Dave)
**From:** Q33N (Bot ID: QUEEN-2026-03-18-BRIEFING-BL-056-BUI)
**Date:** 2026-03-18
**Status:** AWAITING REVIEW

---

## Summary

I have analyzed the briefing for BL-056 (Automated overnight build pipeline improvements) and created **3 task files** for bee dispatch. All task files are ready for your review.

## Analysis

The briefing correctly identified the gap:
- **ALREADY IMPLEMENTED:** Stale process detection (watchdog), morning report, result aggregation
- **MISSING:** Retry with backoff for transient dispatch failures, test coverage for watchdog and overnight orchestration

The queue runner is robust. This spec adds missing pieces:
1. **Retry backoff** — Reduces false-negative failures from transient network/filesystem errors
2. **Test coverage** — Locks in existing behavior with regression tests

## Task Files Created

### TASK-BL-056-A: Retry with backoff on transient dispatch failures
- **File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BL-056-A-RETRY-WITH-BACKOFF.md`
- **Model:** haiku
- **Deliverables:**
  - New module: `dispatch_retry.py` with `retry_with_backoff()` function
  - Integration: Modify `dispatch_handler.py` to wrap subprocess calls
  - Transient error classification: `subprocess.TimeoutExpired`, `FileNotFoundError`, `ConnectionError`, `urllib.error.URLError`
  - Test file: `test_dispatch_retry.py` (12+ tests)
- **Test coverage:**
  - Immediate success, success on attempt 2/3, exhaust retries
  - Backoff timing verification (2s, 4s, 8s)
  - Custom backoff base and max attempts
  - Return value passthrough, exception passthrough
  - Multiple exception types, zero attempts edge case

### TASK-BL-056-B: Tests for watchdog stale detection
- **File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BL-056-B-WATCHDOG-TESTS.md`
- **Model:** haiku
- **Deliverables:**
  - Test file: `test_watchdog_stale_detection.py` (8+ tests)
  - Regression tests for existing watchdog implementation
- **Test coverage:**
  - Fresh heartbeat (< 480s), stale heartbeat (> 480s)
  - Fallback to last_seen, task not in monitor, monitor unreachable
  - Watchdog kills process, timeout heartbeat POST, restart recursion
- **Mock strategy:**
  - `unittest.mock.patch` for time, HTTP, subprocess
  - No real HTTP calls, no real subprocess spawns, no 8-minute waits

### TASK-BL-056-C: Integration tests for overnight queue processing
- **File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BL-056-C-OVERNIGHT-INTEGRATION-TESTS.md`
- **Model:** sonnet (complex orchestration logic)
- **Deliverables:**
  - Test file: `test_queue_overnight.py` (10+ tests)
  - Integration tests for watch mode, hot-reload, dependencies, backoff, budget, reports
- **Test coverage:**
  - Watch mode polling, hot-reload during processing
  - Dependency blocking (hold-until), Fibonacci backoff (adaptive=True)
  - Budget exhaustion, session report generation
  - Slot backfill, priority ordering (P0 > P1 > P2)
  - Fix cycle generation, max restart attempts (2)
- **Mock strategy:**
  - Mock `process_spec_no_verify()` for instant results
  - Mock `time.sleep()` to avoid waiting
  - Use `tmp_path` for filesystem isolation

## Files to Create (Summary)

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_retry.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_retry.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_watchdog_stale_detection.py`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_queue_overnight.py`

## Files to Modify (Summary)

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — Integrate retry wrapper in `call_dispatch()`

## Compliance Check

All task files comply with DEIA rules:
- [x] Absolute file paths (Windows format)
- [x] Test count specified (12+, 8+, 10+)
- [x] Integration points identified (dispatch_handler.py)
- [x] Response file template included (8-section format)
- [x] No file over 500 lines constraint specified
- [x] TDD requirement stated
- [x] No stubs constraint stated
- [x] Model assignment provided (haiku, haiku, sonnet)

## Recommendations

**Task dependencies:**
- TASK-BL-056-A and TASK-BL-056-B are independent — can dispatch in parallel (2 slots)
- TASK-BL-056-C is independent — can dispatch in parallel or sequentially

**Dispatch order suggestion:**
1. Dispatch TASK-BL-056-A and TASK-BL-056-B in parallel (both haiku, ~15 min each)
2. Dispatch TASK-BL-056-C after (sonnet, ~25 min) OR in parallel if 3 slots available

**Total estimated time:** ~40 minutes (parallel) or ~55 minutes (sequential)

## Next Steps

**Your turn (Q88NR):**
1. Review the 3 task files
2. Check for missing deliverables, imprecise acceptance criteria, or gaps vs briefing
3. If corrections needed: tell me what to fix, I'll revise and return
4. If approved: tell me to dispatch bees

I will NOT dispatch bees until you approve.

---

**Q33N-bot QUEEN-2026-03-18-BRIEFING-BL-056-BUI**
