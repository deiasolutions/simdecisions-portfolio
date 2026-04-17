# TASK-MCP-QUEUE-03: Refactor Scheduler for Event-Driven Operation

## Objective

Modify `scheduler_daemon.py` to wake instantly on MCP `queue.spec_done` events instead of polling every 30s, with 60s fallback polling for resilience.

## Context

Currently scheduler polls `_done/` every 30s. With MCP events, it should wake instantly when specs complete, reducing detection latency from 30s → <1s.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` (section: Scheduler Refactor Plan)

## Files to Read First

- `hivenode/scheduler/scheduler_daemon.py` (lines 164-442)
  - Current daemon loop structure
- `hivenode/scheduler/scheduler_mcp_server.py` (created by TASK-MCP-QUEUE-02)
  - MCP event receiver endpoint
- `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
  - Event-driven architecture section

## Deliverables

- [ ] Modify `hivenode/scheduler/scheduler_daemon.py`:
  - Add `wake_event` (threading.Event) to SchedulerDaemon
  - Add `mcp_enabled` constructor parameter (default True)
  - Implement `on_mcp_event(event: dict)` method
  - Modify `_daemon_loop()` to use `wake_event.wait(timeout=60)` instead of `time.sleep(30)`
  - Add MCP server startup logic (run scheduler_mcp_server in background thread)
  - Add `--mcp-enabled` CLI flag
- [ ] Modify `hivenode/scheduler/scheduler_mcp_server.py`:
  - Connect `POST /mcp/event` handler to daemon.on_mcp_event()
  - Handle `queue.spec_done` events
  - Log received events
- [ ] E2E test: `tests/scheduler/test_scheduler_mcp_e2e.py`
  - Start scheduler daemon with MCP enabled
  - Move spec to `_done/`
  - Send MCP event via POST
  - Verify schedule recalculated within 2s
  - Verify fallback polling works if no events (60s timeout)
- [ ] Unit tests: `tests/scheduler/test_scheduler_mcp_unit.py`
  - Test `on_mcp_event()` sets wake_event
  - Test fallback timeout (60s)
  - Test MCP disabled mode (polling only)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (including existing scheduler tests)
- [ ] Edge cases:
  - MCP server down on startup
  - MCP event malformed (missing fields)
  - Multiple events within 1s (only one wake)
  - Daemon stopped while waiting

## Acceptance Criteria

- [ ] Scheduler wakes on `queue.spec_done` event with <1s latency
- [ ] Fallback polling works if MCP unavailable (60s interval)
- [ ] All existing scheduler tests pass (no regressions)
- [ ] MCP can be disabled via `--mcp-enabled=false` flag
- [ ] Scheduler recalculates schedule on every wake (event or timeout)
- [ ] `schedule_log.jsonl` includes event source (mcp_event vs fallback_poll)
- [ ] E2E test verifies end-to-end flow
- [ ] Unit tests: 6+ tests, all passing
- [ ] No file over 500 lines

## Implementation Notes

### Event-Driven Daemon Loop

```python
class SchedulerDaemon:
    def __init__(self, tasks, min_bees, max_bees, schedule_dir, queue_dir,
                 interval_seconds=30, mcp_enabled=True):
        # ... existing init ...
        self.mcp_enabled = mcp_enabled
        self.wake_event = threading.Event()

        # Start MCP server if enabled
        if self.mcp_enabled:
            self._start_mcp_server()

    def _start_mcp_server(self):
        """Start MCP event receiver server in background thread."""
        from hivenode.scheduler import scheduler_mcp_server
        mcp_thread = threading.Thread(
            target=scheduler_mcp_server.run_server,
            args=(self, 8422),
            daemon=True
        )
        mcp_thread.start()
        logger.info("MCP server started on port 8422")

    def on_mcp_event(self, event: dict):
        """Handle MCP queue.spec_done event."""
        if event.get("event") == "queue.spec_done":
            logger.info(f"MCP event: spec completed: {event['spec_file']}")
            self.wake_event.set()  # Wake daemon immediately

    def _daemon_loop(self):
        """Daemon background loop (event-driven with fallback)."""
        logger.info("Daemon loop started")

        while self.running:
            try:
                # Wait for wake event or timeout
                woken = self.wake_event.wait(timeout=60)  # 60s fallback

                if woken:
                    logger.info("Woken by MCP event, recalculating schedule")
                    self.wake_event.clear()
                else:
                    logger.info("Fallback poll (60s timeout)")

                # Always recalculate on wake (event or timeout)
                self._daemon_loop_once()

            except Exception as e:
                logger.error(f"Error in daemon loop: {e}", exc_info=True)
                time.sleep(60)  # Sleep on error

        logger.info("Daemon loop exited")
```

### Schedule Log Entry (Track Event Source)

Modify `write_schedule_log()` to include source:

```python
write_schedule_log(log_file, {
    "event": "schedule_computed",
    "source": "mcp_event" if woken else "fallback_poll",
    "makespan_hours": schedule["makespan_hours"],
    "velocity": schedule["velocity"],
    "task_count": len(schedule["tasks"]),
})
```

### CLI Flag

```python
parser.add_argument("--mcp-enabled", action="store_true", default=True,
                    help="Enable MCP event-driven mode (default: True)")
```

### Fallback Behavior

If MCP server fails to start, log warning and continue with polling:

```python
def _start_mcp_server(self):
    try:
        # ... start server ...
    except Exception as e:
        logger.warning(f"MCP server failed to start: {e}, falling back to polling")
        self.mcp_enabled = False
```

## Constraints

- No file over 500 lines
- Preserve existing CLI interface (all flags still work)
- No breaking changes to `schedule.json` format
- Thread-safe wake_event handling
- No stubs — fully implemented
- All existing tests must pass

## Dependencies

**Depends on:** TASK-MCP-QUEUE-02 (HTTP endpoints must exist)

## Estimated Duration

1.5-2 hours (Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-03-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
