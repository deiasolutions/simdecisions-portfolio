# SPEC-DISPATCH-001-watchdog-restart-fix: Fix watchdog restart stale temp file bug

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Fix the watchdog restart logic in dispatch_handler.py that crashes with FileNotFoundError when restarting a timed-out bee. Line 187 reads `temp_task_path` but the temp file has already been cleaned up by the time the watchdog triggers a restart. This bug caused false-positive fix specs for HYG-003, HYG-004, and HYG-005 — wasting 6 bee dispatches on work that was already complete.

## Files to Read First

- .deia/hive/scripts/queue/dispatch_handler.py
- .deia/hive/responses/20260413-QUEUE-TEMP-2026-04-13-0549-SPEC-fix-HYG-005-ts-node-types-RESPONSE.md
- .deia/hive/responses/20260413-0115-QUEUE-TEMP-2026-04-13-0106-SPEC-fix-HYG-004-python-dead-code-RESPONSE.md

## Acceptance Criteria

- [ ] `dispatch_handler.py` line 187 no longer crashes when temp file is missing during watchdog restart
- [ ] When the temp file is missing at restart time, the handler either (a) caches the content before dispatch so it's available for restart, or (b) gracefully skips the restart and reports TIMEOUT without creating a broken fix spec
- [ ] The handler checks if the original spec already exists in `_done/` before creating a fix spec — if it does, skip fix spec creation
- [ ] No fix spec is created when the failure is a FileNotFoundError on the temp task path (infrastructure error, not code error)
- [ ] A new test covers the scenario: watchdog timeout -> temp file missing -> graceful handling (no crash, no false fix spec)
- [ ] All existing queue runner tests still pass

## Smoke Test

- [ ] Run `python -m pytest tests/ -k "dispatch" -v` and all tests pass
- [ ] Manually verify: if `temp_task_path` does not exist at line 187, the handler logs a warning and returns `(False, None, "TIMEOUT")` instead of crashing

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Only modify .deia/hive/scripts/queue/dispatch_handler.py and its test file
- Do not change the watchdog timeout value or heartbeat logic
- The fix must handle both restart scenarios: (a) temp file deleted early, (b) temp file never created
