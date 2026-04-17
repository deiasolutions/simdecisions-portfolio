# SPEC-INFRA-01: Investigate and Fix Embedded Queue Runner Crash

## Priority
P1

## Model Assignment
sonnet

## Depends On
None

## Intent

The embedded queue runner (`QueueRunnerBridge` in `hivenode/queue_bridge.py`) dies silently — both during long-running sessions (48h+ uptime) and on fresh boot. The `/build/queue-runner-status` MCP endpoint reports `running: false` immediately after hivenode starts. The `/build/queue-wake` POST endpoint returns `queue runner not running` and cannot restart it.

This means specs placed in `queue/` are never picked up unless a standalone runner is manually started. This defeats the purpose of the embedded runner.

## Files to Read First

- hivenode/queue_bridge.py
- hivenode/main.py
- .deia/hive/scripts/queue/run_queue.py
- hivenode/routes/build_monitor.py

## Investigation Questions

1. Why does `QueueRunnerBridge` report `running: false` on fresh boot? Does it fail during `lifespan` startup? Is there an uncaught exception?
2. What exception or error kills the runner? Add logging if none exists.
3. Why can't `/build/queue-wake` restart it? What's the restart path supposed to be?
4. Is the runner thread crashing on import, on first poll, or on first dispatch?
5. Does the runner depend on state (files, dirs, configs) that may not exist on clean startup?

## Acceptance Criteria

- [ ] Root cause identified and documented
- [ ] Queue runner starts reliably on hivenode boot
- [ ] Queue runner recovers from transient errors without dying permanently
- [ ] `/build/queue-wake` can restart a dead runner
- [ ] `/build/queue-runner-status` accurately reflects runner state
- [ ] Add structured logging for runner lifecycle events (start, stop, crash, restart)
- [ ] Tests cover: runner starts on boot, runner recovers from error, wake endpoint restarts dead runner

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- 8-section response file on completion

## Smoke Test

Start hivenode fresh. Within 30 seconds, `/build/queue-runner-status` returns `running: true`. Place a SPEC file in `queue/`. Runner picks it up within one poll cycle.
