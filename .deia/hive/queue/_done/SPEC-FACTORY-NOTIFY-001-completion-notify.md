# SPEC-FACTORY-NOTIFY-001-completion-notify: Completion Notification System

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

There is no mechanism to notify Q33NR or Q88N when specs complete, fail, or exhaust retries. The only way to know work finished is manual polling of `/build/status` or checking logs. Add a notification callback system to the queue watcher that fires on `spec_done` and `spec_dead` events, logging completions and failures to a structured notification log that the build monitor can serve.

## Files to Read First

- hivenode/queue_watcher.py
- hivenode/main.py
- hivenode/routes/build_monitor.py
- hivenode/routes/queue_events.py

## Acceptance Criteria

- [ ] Queue watcher `_on_queue_event` callback in `main.py` handles `queue.spec_done` and `queue.spec_dead` events
- [ ] On `spec_done`: log completion to a notifications list in BuildState with timestamp, spec_file, task_id, status="completed"
- [ ] On `spec_dead`: log failure to notifications list with timestamp, spec_file, task_id, status="failed", and rejection reason if available
- [ ] New endpoint `GET /build/notifications` returns the last 50 notifications in reverse chronological order
- [ ] New endpoint `GET /build/notifications?since=YYYY-MM-DDTHH:MM:SS` returns only notifications after the given timestamp
- [ ] Notifications are persisted in `monitor-state.json` so they survive restarts
- [ ] SSE `/build/stream` broadcasts a `notification` event type when a notification is added
- [ ] All existing tests still pass
- [ ] 5+ new tests: notification on done, notification on dead, GET endpoint, since filter, SSE broadcast

## Smoke Test

- [ ] Move a spec to `_done/`, verify `curl -s http://127.0.0.1:8420/build/notifications` shows the completion
- [ ] Move a spec to `_needs_review/`, verify notification shows failure

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Do not add external dependencies (no email, SMS, or webhook for now — just in-process notification store + SSE)
- Keep the notification payload minimal: timestamp, spec_file, task_id, status, message
