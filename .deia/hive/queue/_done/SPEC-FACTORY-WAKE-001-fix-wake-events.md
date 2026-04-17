# SPEC-FACTORY-WAKE-001-fix-wake-events: Fix Wake Event Filtering and Dead Code

## Priority
P1

## Depends On
None

## Model Assignment
haiku

## Objective

Fix three quick-win issues in the factory wake/notify system: (1) the queue watcher callback in main.py only wakes the runner on `spec_backlog` events but not `spec_queued`, so specs moved by the dispatcher daemon don't trigger a wake; (2) `send_liveness_ping()` in run_queue.py is defined but never called — either wire it or remove it; (3) the watchdog timeout message in dispatch_handler.py says "15 minutes" but the actual constant is 480 seconds (8 minutes).

## Files to Read First

- hivenode/main.py
- .deia/hive/scripts/queue/run_queue.py
- .deia/hive/scripts/queue/dispatch_handler.py

## Acceptance Criteria

- [ ] `_on_queue_event` callback in `main.py` checks for both `"queue.spec_backlog"` and `"queue.spec_queued"` event types
- [ ] `send_liveness_ping()` in `run_queue.py` is either called on a 30s interval from the watch loop OR removed entirely (choose whichever is cleaner)
- [ ] Timeout message in `dispatch_handler.py` matches `WATCHDOG_STALE_SECONDS` value (either fix the message or fix the constant — they must agree)
- [ ] All existing tests still pass

## Smoke Test

- [ ] Drop a spec in queue root (not backlog) — verify queue runner wakes (check logs for wake message)

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- These are small targeted fixes — do not refactor surrounding code
