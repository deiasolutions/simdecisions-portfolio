# TASK-SD-FIX-02: Fix Scheduler UTF-8 Encoding — COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-05

---

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py`
   - Line 130: Changed `spec_file.read_text()` to `spec_file.read_text(encoding='utf-8', errors='replace')`

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_scheduler_daemon.py`
   - Added 3 new test methods to `TestVelocityUpdates` class:
     - `test_velocity_from_unicode_spec_content()`
     - `test_velocity_with_mixed_ascii_and_unicode()`
     - `test_velocity_with_utf8_emoji_bytes()`

---

## What Was Done

### Implementation Fix
- **Minimal one-line change** at line 130 in `scheduler_daemon.py`
- Changed: `content = spec_file.read_text()`
- To: `content = spec_file.read_text(encoding='utf-8', errors='replace')`
- This ensures UTF-8 encoding is explicitly used with error handling to replace undecodable bytes

### Test Implementation (TDD)
Created three comprehensive tests covering:
1. **test_velocity_from_unicode_spec_content()** — Specs with emoji (✅🎉) and special chars (→•…) parse correctly
2. **test_velocity_with_mixed_ascii_and_unicode()** — Multiple specs with mixed ASCII and UTF-8 content compute velocity accurately
3. **test_velocity_with_utf8_emoji_bytes()** — Direct UTF-8 byte writing with emoji doesn't raise codec errors

All tests verify:
- No 'charmap' codec errors when parsing unicode content
- Telemetry regex still extracts estimated/actual hours correctly
- Velocity computation returns accurate values (e.g., 0.9 for 1.8/2.0)

---

## Acceptance Criteria

- [x] Add `encoding='utf-8', errors='replace'` to `spec_file.read_text()` call in `load_velocity_from_done()` (line 130)
- [x] Add new test: `test_velocity_from_unicode_spec_content()`
  - [x] Test that specs with emoji/unicode characters are parsed without error
  - [x] Test that velocity computation still works correctly
- [x] Add test: `test_velocity_with_mixed_ascii_and_unicode()`
  - [x] Spec with emoji in title and content
- [x] Add test: `test_velocity_with_utf8_emoji_bytes()`
  - [x] UTF-8 encoded bytes with emoji
- [x] Verify all existing scheduler tests still pass

---

## Test Results

**Test File:** `tests/hivenode/scheduler/test_scheduler_daemon.py`

**Summary:** 28/28 PASSED ✓

**Test Breakdown:**
- TestDaemonLifecycle: 3/3 passed
- TestDryRunFlag: 1/1 passed
- TestTimeWindowComputation: 4/4 passed
- TestVelocityUpdates: 6/6 passed (3 existing + 3 new)
- TestTaskStatusTracking: 6/6 passed
- TestScheduleOutput: 3/3 passed
- TestSignalHandling: 1/1 passed
- TestEdgeCases: 4/4 passed

**New Unicode Tests:**
- `test_velocity_from_unicode_spec_content` — PASSED ✓
- `test_velocity_with_mixed_ascii_and_unicode` — PASSED ✓
- `test_velocity_with_utf8_emoji_bytes` — PASSED ✓

---

## Build Verification

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
collected 28 items

tests/hivenode/scheduler/test_scheduler_daemon.py::TestDaemonLifecycle::... PASSED [  3%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestDaemonLifecycle::... PASSED [  7%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestDaemonLifecycle::... PASSED [ 10%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestDryRunFlag::... PASSED [ 14%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTimeWindowComputation::... PASSED [ 17%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTimeWindowComputation::... PASSED [ 21%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTimeWindowComputation::... PASSED [ 25%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTimeWindowComputation::... PASSED [ 28%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_from_empty_done_dir PASSED [ 32%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_from_completed_specs_with_telemetry PASSED [ 35%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_ignores_specs_without_telemetry PASSED [ 39%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_from_unicode_spec_content PASSED [ 42%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_with_mixed_ascii_and_unicode PASSED [ 46%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestVelocityUpdates::test_velocity_with_utf8_emoji_bytes PASSED [ 50%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_starts_as_pending PASSED [ 53%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_becomes_ready_when_deps_satisfied PASSED [ 57%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_becomes_blocked_when_deps_not_satisfied PASSED [ 60%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_reads_dispatched_status_from_jsonl PASSED [ 64%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_in_active_dir_is_in_progress PASSED [ 67%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestTaskStatusTracking::test_task_in_done_dir_is_done PASSED [ 71%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestScheduleOutput::test_schedule_json_written_with_correct_format PASSED [ 75%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestScheduleOutput::test_schedule_log_appends_events PASSED [ 78%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestScheduleOutput::test_velocity_update_logged PASSED [ 82%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestSignalHandling::test_sigint_triggers_graceful_shutdown PASSED [ 85%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestEdgeCases::test_no_dispatched_jsonl_starts_fresh PASSED [ 89%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestEdgeCases::test_empty_done_dir_uses_default_velocity PASSED [ 92%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestEdgeCases::test_all_tasks_complete_daemon_idles PASSED [ 96%]
tests/hivenode/scheduler/test_scheduler_daemon.py::TestEdgeCases::test_circular_dependencies_detected PASSED [100%]

======================= 28 passed, 2 warnings in 32.02s =======================
```

---

## Clock / Cost / Carbon

*(Populated from build monitor telemetry)*

- **Execution Time:** ~5 minutes (TDD cycle: write tests, fix implementation, verify)
- **Tests Executed:** 28 total (6 velocity tests, 28 total suite)
- **Cost:** Haiku model, small test suite
- **Carbon:** Minimal (no large builds)

---

## Issues / Follow-ups

**None.** The fix is:
- ✓ Minimal (one-line change)
- ✓ Fully tested (3 new unicode tests + 25 existing tests all pass)
- ✓ Backward compatible (utf-8 is superincident, errors='replace' handles edge cases)
- ✓ Addresses root cause (explicit UTF-8 encoding prevents 'charmap' codec errors)

The `errors='replace'` parameter ensures undecodable bytes are replaced with U+FFFD (replacement character) rather than raising an exception, which is safe for telemetry parsing since regex patterns only look for ASCII numeric patterns that won't be affected by replacement characters.

---

**Task Complete.** Scheduler daemon now handles unicode content in specs without codec errors.
