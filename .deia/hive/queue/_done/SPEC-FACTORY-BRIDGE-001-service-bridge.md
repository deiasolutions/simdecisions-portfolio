# SPEC-FACTORY-BRIDGE-001-service-bridge: Generic ServiceBridge + Embed Scheduler and Dispatcher

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Create a reusable `ServiceBridge` base class that standardizes how external services (daemons) are embedded in hivenode's lifespan. Then refactor `QueueRunnerBridge` to use it, and create `SchedulerBridge` and `DispatcherBridge` to embed the scheduler and dispatcher daemons. All three services get wake_event support, auto-restart with rate limiting, and error notification.

## Files to Read First

- hivenode/queue_bridge.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/scheduler/dispatcher_daemon.py
- hivenode/main.py
- hivenode/queue_watcher.py

## Acceptance Criteria

- [ ] New file `hivenode/service_bridge.py` contains a `ServiceBridge` base class
- [ ] `ServiceBridge` provides: `start()`, `stop()`, `wake()`, `is_running` property
- [ ] `ServiceBridge` runs the service in a background thread via `asyncio.to_thread()`
- [ ] `ServiceBridge` passes a `threading.Event` (wake_event) to the service
- [ ] `ServiceBridge` auto-restarts on crash with NO cap on total restart count
- [ ] Restart rate is limited: if more than 5 restarts occur within 10 minutes, stop retrying, log an ERROR with full context, and POST a notification to `/build/heartbeat` with status `"bridge_failure"` and a message naming the failed service
- [ ] After a rate-limit pause, the bridge can be manually restarted via `wake()` or the `/build/queue-wake` pattern
- [ ] Exponential backoff between restarts: 5s, 10s, 20s, 40s, 60s (capped at 60s)
- [ ] `QueueRunnerBridge` in `hivenode/queue_bridge.py` is refactored to extend `ServiceBridge`
- [ ] New `SchedulerBridge` created (can live in `hivenode/scheduler/scheduler_bridge.py` or in `service_bridge.py`)
- [ ] New `DispatcherBridge` created (same location pattern)
- [ ] `SchedulerBridge` wraps `scheduler_daemon.py`'s main run loop, passing `wake_event`
- [ ] `DispatcherBridge` wraps `dispatcher_daemon.py`'s main run loop, passing `wake_event`
- [ ] `hivenode/main.py` lifespan starts all three bridges: queue_runner, scheduler, dispatcher
- [ ] `hivenode/main.py` lifespan stops all three bridges on shutdown
- [ ] Queue watcher `_on_queue_event` callback in `main.py` wakes the scheduler and dispatcher bridges on relevant events (not just the queue runner)
- [ ] All existing tests still pass
- [ ] 5+ new tests covering: ServiceBridge restart logic, rate limiting, wake propagation

## Smoke Test

- [ ] `curl -s http://127.0.0.1:8420/health` returns 200 after restart
- [ ] All three services appear in hivenode logs as started
- [ ] Dropping a spec in backlog/ wakes all three services (check logs for wake messages)

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- ServiceBridge must be generic enough for future services (e.g. scan daemon, triage daemon)
- scheduler_daemon.py and dispatcher_daemon.py need their run loops refactored to accept a `wake_event` parameter (like run_queue.py already does)
- Do NOT remove the standalone CLI entry points from scheduler_daemon.py and dispatcher_daemon.py — they must still work as standalone processes
