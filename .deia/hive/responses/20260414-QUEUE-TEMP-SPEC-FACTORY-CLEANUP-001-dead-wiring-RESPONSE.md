# SPEC-FACTORY-CLEANUP-001: Clean Up Dead Wiring and Unbounded Growth -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-14

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\build_monitor.py
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\queue_watcher.py
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\scheduler_daemon.py
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\spec_utils.py (created)
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\test_factory_cleanup_001.py (created)
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\routes\test_build_pipeline_counts.py

## What Was Done

### 1. Removed `_hold/` Directory References
- Removed `_hold/` reference from `get_status()` method (line 473: `feeder_queue` key removed)
- Removed `_hold/` from `retry_task()` spec file search paths (line 727)
- Removed `_hold/` from `get_pipeline_counts()` directory scanning (line 792)
- Updated corresponding tests in `test_build_pipeline_counts.py` to remove `hold` key assertions

### 2. Added Task Pruning to BuildState
- Modified `_save_to_disk()` method to prune terminal tasks (complete, failed, timeout) older than 7 days
- Pruning logic:
  - Keeps all active tasks (dispatched, running) regardless of age
  - Keeps terminal tasks younger than 7 days
  - Removes terminal tasks older than 7 days from state file
- **Aggregates preserved:** `total_cost_usd`, `total_input_tokens`, `total_output_tokens` remain unchanged
- Pruned tasks still contribute to cost/token aggregates (no data loss)

### 3. Added Log Rotation for queue_events.jsonl
- Created `_rotate_log_if_needed()` method in `QueueEventHandler` class
- Rotation trigger: file size exceeds 1MB
- Rotation behavior:
  - Renames current log to `queue_events.jsonl.1`
  - Discards old `.1` backup if exists (keeps only 1 backup)
  - New log file created on next write
- Called before each event write in `_emit_event()` method

### 4. Deduplicated `_extract_task_id_from_spec()` Function
- Created new shared module: `hivenode/spec_utils.py`
- Moved `_extract_task_id_from_spec()` function to `spec_utils.py` as `extract_task_id_from_spec()`
- Updated `queue_watcher.py`:
  - Added import: `from hivenode.spec_utils import extract_task_id_from_spec`
  - Removed duplicate function definition (lines 24-79)
  - Updated function call from `_extract_task_id_from_spec()` to `extract_task_id_from_spec()`
- Updated `scheduler_daemon.py`:
  - Added import: `from hivenode.spec_utils import extract_task_id_from_spec`
  - Removed duplicate method definition (lines 519-574)
  - Updated all calls from `self._extract_task_id_from_spec()` to `extract_task_id_from_spec()` (4 occurrences)

## Tests Written

Created comprehensive test suite in `tests/hivenode/test_factory_cleanup_001.py`:

### Task Pruning Tests (4 tests)
1. `test_prunes_old_terminal_tasks` - Verifies old terminal tasks (>7 days) are removed
2. `test_pruning_preserves_aggregates` - Confirms cost/token aggregates remain unchanged after pruning
3. `test_does_not_prune_active_tasks` - Ensures active tasks are never pruned, even if old
4. `test_prunes_all_terminal_statuses` - Verifies pruning works for complete, failed, and timeout statuses

### Log Rotation Tests (3 tests)
1. `test_rotates_when_exceeds_1mb` - Confirms rotation when file exceeds 1MB
2. `test_does_not_rotate_when_under_1mb` - Verifies no rotation for files under 1MB
3. `test_discards_old_backup_on_rotation` - Ensures old `.1` backup is discarded

### Shared Function Import Tests (4 tests)
1. `test_imports_from_spec_utils` - Verifies function can be imported from spec_utils
2. `test_queue_watcher_uses_shared_function` - Confirms queue_watcher imports shared function
3. `test_scheduler_daemon_uses_shared_function` - Confirms scheduler_daemon imports shared function
4. `test_extract_task_id_formats` - Tests function handles various spec filename formats

## Test Results

**New tests:** 11/11 passed (100%)
**Existing tests:**
- `test_build_monitor_integration.py`: 16/16 passed
- `test_scheduler_daemon.py`: 28/28 passed
- `test_build_pipeline_counts.py`: 12/12 passed (after fixing `_hold/` references)
- `test_scheduler_backlog_scanning.py`: 27/27 passed

**Total:** 94/94 tests passed

## Acceptance Criteria

- [x] All references to `_hold/` directory in `build_monitor.py` are removed (lines ~473, ~726, ~792)
- [x] `BuildState` prunes terminal tasks (status: complete, failed, timeout) older than 7 days from `self.tasks` on each `_save_to_disk()` call
- [x] Pruned tasks are still counted in `total_cost_usd`, `total_input_tokens`, `total_output_tokens` (aggregates preserved)
- [x] `queue_events.jsonl` is rotated: when file exceeds 1MB, rename to `queue_events.jsonl.1` and start fresh (keep only 1 backup)
- [x] `_extract_task_id_from_spec()` exists in ONE location only — `hivenode/spec_utils.py` — and both `queue_watcher.py` and `scheduler_daemon.py` import it
- [x] All existing tests still pass
- [x] 11 new tests written: task pruning preserves aggregates (4 tests), JSONL rotation (3 tests), shared function import (4 tests)

## Smoke Test

Not run (requires live hivenode instance with large monitor-state.json). Manual smoke test recommended:
1. Start hivenode with existing `monitor-state.json` containing old terminal tasks
2. Wait for first heartbeat cycle (or manually trigger `_save_to_disk()`)
3. Verify old terminal tasks (>7 days) are pruned from state file
4. Verify aggregates (`total_cost_usd`, `total_input_tokens`, `total_output_tokens`) remain unchanged

## Notes

- Task pruning prevents unbounded growth of monitor-state.json while preserving cost/token tracking
- Log rotation prevents unbounded growth of queue_events.jsonl (1MB threshold chosen as reasonable size for manual review)
- Shared function eliminates duplication and ensures consistent task ID extraction across modules
- All changes are backward-compatible (existing state files load correctly, old logs remain accessible)
