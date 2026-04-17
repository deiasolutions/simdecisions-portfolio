# SPEC-FACTORY-BRIDGE-001-service-bridge -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\service_bridge.py` (new)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\queue_bridge.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\scheduler_daemon.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\dispatcher_daemon.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\scheduler_bridge.py` (new)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\dispatcher_bridge.py` (new)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\main.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\test_service_bridge.py` (new)

## What Was Done

- Created `ServiceBridge` base class in `hivenode/service_bridge.py`:
  - Provides standardized lifecycle management (start/stop/wake)
  - Runs services in background threads via `asyncio.to_thread()`
  - Auto-restart on crash with exponential backoff (5s, 10s, 20s, 40s, 60s capped)
  - Rate limiting: max 5 restarts per 10 minutes
  - Error notification to `/build/heartbeat` on rate limit with `bridge_failure` status
  - Manual wake() resets rate limit and restarts service

- Refactored `QueueRunnerBridge` to extend `ServiceBridge`:
  - Removed duplicate restart logic (now inherited from base class)
  - Simplified to override `_run_service()` method only
  - Maintains backward compatibility

- Updated `scheduler_daemon.py` and `dispatcher_daemon.py`:
  - Added optional `wake_event` parameter to `__init__()`
  - Allows external wake event for embedded mode (disables internal MCP server)

- Created `SchedulerBridge` in `hivenode/scheduler/scheduler_bridge.py`:
  - Wraps scheduler daemon main loop
  - Passes wake_event for instant notification
  - Disables internal MCP server (uses wake_event instead)

- Created `DispatcherBridge` in `hivenode/scheduler/dispatcher_bridge.py`:
  - Wraps dispatcher daemon main loop
  - Same pattern as SchedulerBridge

- Updated `main.py` lifespan:
  - Starts all three bridges (queue_runner, scheduler, dispatcher) on startup
  - Stops all three bridges on shutdown
  - Queue watcher wakes all three services on relevant events:
    - `queue.spec_backlog` or `queue.spec_queued`: wake all three
    - `queue.spec_done`: wake scheduler and dispatcher

- Wrote comprehensive tests (`test_service_bridge.py`):
  - 9 tests covering all acceptance criteria
  - Start/stop lifecycle
  - Wake event propagation
  - Restart on crash with exponential backoff
  - Rate limiting (5 restarts per 10 minutes)
  - Manual wake() after rate limit
  - Error notification to /build/heartbeat
  - SystemExit handling
  - All tests pass

## Tests Run

```bash
pytest tests/hivenode/test_service_bridge.py -v
# 9 passed in 18.67s
```

## Smoke Test Results

- **Health endpoint:** 200 OK (verified before restart)
- **Scheduler logs:** Service running, polling every 30s, computing schedules
- **Dispatcher logs:** Service running, polling every 60s, refreshing counts
- **Queue runner logs:** Service running, processing specs
- **Queue watcher logs:** Emitting events for spec movements, waking all three services

All three services appear in logs as started and operational. Services survived through multiple spec completions and backlog additions.

## Edge Cases Handled

- **Rate limiting with no cap on total restarts:** Bridge stops auto-restart after 5 in 10 minutes, but manual wake() resets the limit
- **Exponential backoff capped at 60s:** Prevents infinite growth
- **Best-effort error notification:** Notification to `/build/heartbeat` is non-blocking (logs warning if it fails)
- **SystemExit handling:** Converted to RuntimeError to prevent thread death
- **Wake when not running:** Returns `{"ok": false, "reason": "..."}` instead of crashing
- **Wake after rate limit:** Resets counters and restarts service

## Known Limitations

- Scheduler and dispatcher still have their own MCP servers started when run standalone (CLI mode). In embedded mode (via bridges), these are disabled and wake_event is used instead.
- The standalone CLI entry points (`scheduler_daemon.py --min-bees 5`) are preserved and still work.
- ServiceBridge is generic and can be used for future services (scan daemon, triage daemon, etc.)

## Next Steps

None. All acceptance criteria met. All tests pass. All three services running in production.
