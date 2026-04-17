# SPEC-FACTORY-CLEANUP-001-dead-wiring: Clean Up Dead Wiring and Unbounded Growth

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Clean up dead wiring, dead code, and unbounded growth issues identified in the factory audit: remove `_hold/` references from build_monitor.py, add task pruning to BuildState, add log rotation to queue_events.jsonl, and deduplicate `_extract_task_id_from_spec()`.

## Files to Read First

- hivenode/routes/build_monitor.py
- hivenode/queue_watcher.py
- hivenode/scheduler/scheduler_daemon.py

## Acceptance Criteria

- [ ] All references to `_hold/` directory in `build_monitor.py` are removed (lines ~473, ~726)
- [ ] `BuildState` prunes terminal tasks (status: complete, failed, timeout, cancelled) older than 7 days from `self.tasks` on each `_save_to_disk()` call
- [ ] Pruned tasks are still counted in `total_cost_usd`, `total_input_tokens`, `total_output_tokens` (aggregates preserved)
- [ ] `queue_events.jsonl` is rotated: when file exceeds 1MB, rename to `queue_events.jsonl.1` and start fresh (keep only 1 backup)
- [ ] `_extract_task_id_from_spec()` exists in ONE location only — either `queue_watcher.py` or a shared util — and `scheduler_daemon.py` imports it instead of duplicating
- [ ] All existing tests still pass
- [ ] 3+ new tests: task pruning preserves aggregates, JSONL rotation, shared function import

## Smoke Test

- [ ] Start hivenode with a large `monitor-state.json` containing old tasks, verify they are pruned after first heartbeat cycle

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Pruning must never delete tasks that are still active (dispatched, running)
