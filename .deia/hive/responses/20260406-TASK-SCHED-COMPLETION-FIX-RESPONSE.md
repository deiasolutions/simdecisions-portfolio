# TASK-SCHED-COMPLETION-FIX: Fix scheduler completion detection -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-06

## Files Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_scheduler_completion_detection.py` (248 lines, 12 tests)

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py` (added 64-line `_extract_task_id_from_spec()` method, updated completion detection logic in `compute_schedule()`)

## What Was Done

- Added `_extract_task_id_from_spec()` method to `SchedulerDaemon` class (lines 236-291)
  - Supports 3 naming conventions: exact, prefixed, dated
  - Extracts task ID from spec filenames (e.g., `SPEC-MW-031-menu-bar-drawer.md` → `MW-031`)
  - Case-insensitive matching, returns uppercase task ID
  - Logs warnings for malformed filenames
- Updated `compute_schedule()` method (lines 304-320) to use new extraction logic
  - Replaced naive `f.stem.replace("SPEC-", "")` with proper extraction
  - Iterates through `_done/` and `_active/` specs, extracts task IDs correctly
  - Builds `done_specs` and `active_specs` sets with extracted task IDs
- Created comprehensive test suite with 12 tests (9 unit + 3 integration)
  - Tests all 3 filename formats
  - Tests case-insensitivity, complex descriptions, malformed files
  - Integration tests verify completion detection and schedule recalculation
- Verified against real `_done/` directory with 18 MW specs
  - All 18 specs correctly detected and excluded from schedule
  - Task count reduced from 66 → 48 (18 completed)
  - Makespan recalculated correctly

## Test Results

**Test file:** `tests/hivenode/scheduler/test_scheduler_completion_detection.py`
- 12 tests written (TDD approach — tests written first, implementation second)
- All 12 tests pass

**Full scheduler test suite:**
- 64 total tests (52 existing + 12 new)
- All 64 tests pass
- No regressions introduced

**Real-world verification:**
- Tested against 18 MW specs in `.deia/hive/queue/_done/`
- All 18 task IDs extracted correctly
- All 18 tasks excluded from schedule
- Schedule recalculated: 66 tasks → 48 tasks, makespan = 92 hours

## Build Verification

```
$ pytest tests/hivenode/scheduler/test_scheduler_completion_detection.py -v
============================= test session starts =============================
collected 12 items

test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_from_prefixed_filename PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_from_exact_filename PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_from_dated_filename PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_case_insensitive PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_with_complex_description PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_malformed_filename_no_spec_prefix PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_malformed_filename_invalid_format PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_without_extension PASSED
test_scheduler_completion_detection.py::TestExtractTaskIdFromSpec::test_extract_with_path_object PASSED
test_scheduler_completion_detection.py::TestSchedulerCompletionDetection::test_detect_completed_specs_in_done_dir PASSED
test_scheduler_completion_detection.py::TestSchedulerCompletionDetection::test_scheduler_handles_no_completed_specs PASSED
test_scheduler_completion_detection.py::TestSchedulerCompletionDetection::test_scheduler_recalculates_with_reduced_task_count PASSED

============================== 12 passed in 0.31s =============================
```

```
$ pytest tests/hivenode/scheduler/ -v
============================= test session starts =============================
collected 64 items

[... 52 existing tests ...]
[... 12 new tests ...]

============================== 64 passed in 52.63s ==============================
```

**Real-world test:**
- Scheduler daemon correctly detects 18 completed MW specs
- Schedule output shows 48 remaining tasks (down from 66)
- All completed tasks excluded from schedule
- Makespan recalculated to 92 hours

## Acceptance Criteria

- [x] Add `_extract_task_id_from_spec()` method to `SchedulerDaemon` class
- [x] Input: spec filename (e.g., `SPEC-MW-031-menu-bar-drawer.md`)
- [x] Output: task ID (e.g., `MW-031`)
- [x] Support three formats:
  - [x] `SPEC-{ID}.md` → `{ID}`
  - [x] `SPEC-{ID}-{description}.md` → `{ID}` (extract prefix before second dash)
  - [x] Dated format: `{date}-SPEC-{ID}-{description}.md` → `{ID}`
- [x] Handle edge cases like `MW-S01` (letter in ID) and `MW-033` (numeric)
- [x] Update line 252 to use `_extract_task_id_from_spec()`
- [x] After fix, scheduler detects all 18 completed MW tasks in `_done/`
- [x] Scheduler recalculates schedule with reduced task count (66 → 48) and makespan (92h)
- [x] All scheduler tests pass (64/64)
- [x] Tests written FIRST (TDD)
- [x] Test file: `tests/hivenode/scheduler/test_scheduler_completion_detection.py`
- [x] Test cases cover all 3 filename formats, edge cases, integration scenarios
- [x] All tests pass (12/12 new, 64/64 total)

## Clock / Cost / Carbon

**Clock:** 14 minutes (TDD cycle: write tests, implement, verify, real-world test)
**Cost:** $0.11 USD (Sonnet 4.5 — 58k tokens in, 2.5k tokens out)
**Carbon:** ~0.8g CO₂e (estimated for API + compute)

## Issues / Follow-ups

**None.** Implementation complete and tested.

### Implementation Notes

The `_extract_task_id_from_spec()` method uses a simple algorithm:
1. Remove file extension (`.md`)
2. Remove date prefix if present (`YYYY-MM-DD-`)
3. Remove `SPEC-` prefix (case-insensitive)
4. Split on dashes and take first two parts (`PREFIX-ID`)
5. Return uppercase

This works correctly for all MW task IDs in the current schedule:
- `MW-S01`, `MW-S02`, ..., `MW-S08` (spec tasks)
- `MW-T01`, `MW-T02`, ..., `MW-T08` (test tasks)
- `MW-001`, `MW-002`, ..., `MW-042` (build tasks)
- `MW-V01`, `MW-V02`, ..., `MW-V08` (verify tasks)
- `MW-023`, `MW-024`, ..., `MW-036` (mobile CSS tasks)

The algorithm is backward compatible and handles all three naming conventions used in the project.

### Real-World Impact

Before fix:
- Scheduler reported 66 tasks with unchanged makespan after 18 completions
- No completion detection due to ID mismatch (`MW-031-menu-bar-drawer` vs `MW-031`)

After fix:
- Scheduler correctly detects 18 completed tasks
- Schedule shows 48 remaining tasks (66 - 18 = 48)
- Makespan recalculated to 92 hours
- Completion detection working as designed

The dispatcher daemon already had correct spec-finding logic (`_find_spec_file()` in `dispatcher_daemon.py` lines 260-330). The scheduler now has the inverse operation (`_extract_task_id_from_spec()`) to correctly identify completions.
