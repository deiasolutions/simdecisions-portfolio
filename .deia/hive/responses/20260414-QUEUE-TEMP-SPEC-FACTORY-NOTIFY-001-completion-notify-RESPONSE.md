# QUEUE-TEMP-SPEC-FACTORY-NOTIFY-001-completion-notify — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\build_monitor.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\main.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\routes\test_build_monitor_notifications.py` (new file)

## What Was Done
- Added `notifications` list to BuildState for tracking spec completions/failures
- Added `notifications` field to persistence in `_load_from_disk()` and `_save_to_disk()`
- Created `record_notification()` method to log spec done/dead events with timestamp, spec_file, task_id, status, message
- Notifications limited to last 50 entries (auto-pruning)
- Added `GET /build/notifications` endpoint with optional `?since=TIMESTAMP` filter for polling
- Returns notifications in reverse chronological order (most recent first)
- Modified SSE `/build/stream` to broadcast `notification` events alongside heartbeats
- Wired queue watcher callback in `main.py` to call `record_notification()` on `queue.spec_done` and `queue.spec_dead` events
- For `spec_dead` events, reads rejection sidecar file (`*.rejection.md`) and includes reason in notification
- Created comprehensive test suite with 11 tests covering:
  - Notification creation and structure
  - Persistence across restarts
  - Pruning to 50 entries
  - GET endpoint with timestamp filtering
  - SSE broadcasting
  - Queue event integration
- All 11 new tests pass
- Smoke tested live endpoints: verified completion and failure notifications work correctly

## Tests Passed
- 11/11 new tests in `test_build_monitor_notifications.py` pass
- All existing build monitor integration tests pass (90 passed, 30 pre-existing slot test failures unrelated to this change)

## Smoke Test Results
✅ Moved spec to `_done/` → notification appears in `GET /build/notifications` with status="completed"
✅ Moved spec to `_needs_review/` with `.rejection.md` sidecar → notification appears with status="failed" and rejection message

## Notes
- Notifications persist in `monitor-state.json` so they survive server restarts
- SSE clients receive `event: notification` events in real-time
- Timestamp filtering allows clients to poll for new notifications since last check
- No external dependencies added (all in-process notification store + SSE)
- Queue watcher automatically triggers notifications when specs move to `_done/` or `_needs_review/`
