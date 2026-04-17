# TASK-MCP-QUEUE-04: Refactor Dispatcher for Event-Driven Slot Management

## Objective

Modify `dispatcher_daemon.py` to update slot counts via MCP events instead of direct file counting, enabling instant dispatch when slots free up.

## Context

Currently dispatcher counts specs in `_active/` and `queue/` every 10s. With MCP events, it should update counters instantly and wake when slots free, reducing dispatch latency from 10s → <1s.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` (section: Dispatcher Refactor Plan)

## Files to Read First

- `hivenode/scheduler/dispatcher_daemon.py` (lines 40-402)
  - Current daemon loop and slot counting logic
- `hivenode/scheduler/dispatcher_mcp_server.py` (created by TASK-MCP-QUEUE-02)
  - MCP event receiver endpoint
- `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
  - Event-driven architecture section

## Deliverables

- [ ] Modify `hivenode/scheduler/dispatcher_daemon.py`:
  - Add in-memory counters: `active_count`, `queued_count` (thread-safe with lock)
  - Add `wake_event` (threading.Event)
  - Add `mcp_enabled` constructor parameter (default True)
  - Implement `on_mcp_event(event: dict)` method (updates counters, wakes on slot freed)
  - Implement `_refresh_counts()` fallback (re-count from disk)
  - Modify `_daemon_loop()` to use `wake_event.wait(timeout=60)` instead of `time.sleep(10)`
  - Remove direct file counting from hot path (use in-memory counters)
  - Add MCP server startup logic (run dispatcher_mcp_server in background thread)
  - Add `--mcp-enabled` CLI flag
- [ ] Modify `hivenode/scheduler/dispatcher_mcp_server.py`:
  - Connect `POST /mcp/event` handler to daemon.on_mcp_event()
  - Handle `queue.spec_active`, `queue.spec_done`, `queue.spec_queued` events
  - Log received events
- [ ] E2E test: `tests/scheduler/test_dispatcher_mcp_e2e.py`
  - Start dispatcher daemon with MCP enabled
  - Send `queue.spec_done` event
  - Verify dispatcher wakes and dispatches from backlog within 2s
  - Verify counters updated correctly
  - Verify fallback refresh works (60s timeout)
- [ ] Unit tests: `tests/scheduler/test_dispatcher_mcp_unit.py`
  - Test `on_mcp_event()` updates counters correctly
  - Test counter thread safety (concurrent events)
  - Test fallback `_refresh_counts()` syncs from disk
  - Test MCP disabled mode (polling only)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (including existing dispatcher tests)
- [ ] Edge cases:
  - Counter underflow (active_count goes negative)
  - MCP server down on startup
  - Multiple events within 1s (counters stay accurate)
  - Daemon stopped while waiting

## Acceptance Criteria

- [ ] Dispatcher updates counters on MCP events (`spec_active`, `spec_done`, `spec_queued`)
- [ ] Dispatcher wakes on `queue.spec_done` with <1s latency
- [ ] Fallback polling works if MCP unavailable (60s refresh)
- [ ] All existing dispatcher tests pass (no regressions)
- [ ] MCP can be disabled via `--mcp-enabled=false` flag
- [ ] Counter underflow protection (never go below 0)
- [ ] `dispatcher_log.jsonl` includes event source (mcp_event vs fallback_poll)
- [ ] E2E test verifies end-to-end flow
- [ ] Unit tests: 8+ tests, all passing
- [ ] No file over 500 lines

## Implementation Notes

### In-Memory Counters

```python
class DispatcherDaemon:
    def __init__(self, max_bees, schedule_dir, queue_dir, dry_run=False, mcp_enabled=True):
        # ... existing init ...
        self.mcp_enabled = mcp_enabled
        self.wake_event = threading.Event()

        # In-memory counters (updated by MCP events)
        self.active_count = 0
        self.queued_count = 0
        self._counter_lock = threading.Lock()

        # Start MCP server if enabled
        if self.mcp_enabled:
            self._start_mcp_server()

    def _start_mcp_server(self):
        """Start MCP event receiver server in background thread."""
        from hivenode.scheduler import dispatcher_mcp_server
        mcp_thread = threading.Thread(
            target=dispatcher_mcp_server.run_server,
            args=(self, 8423),
            daemon=True
        )
        mcp_thread.start()
        logger.info("MCP server started on port 8423")
```

### Event Handler

```python
def on_mcp_event(self, event: dict):
    """Handle MCP events (spec_done, spec_active, spec_queued)."""
    event_type = event.get("event")

    with self._counter_lock:
        if event_type == "queue.spec_active":
            self.active_count += 1
            logger.info(f"MCP: spec active, count={self.active_count}")

        elif event_type == "queue.spec_done":
            self.active_count = max(0, self.active_count - 1)  # Prevent underflow
            logger.info(f"MCP: spec done, count={self.active_count}")
            # Wake to check if slots freed
            self.wake_event.set()

        elif event_type == "queue.spec_queued":
            self.queued_count += 1
            logger.info(f"MCP: spec queued, count={self.queued_count}")
```

### Fallback Refresh

```python
def _refresh_counts(self):
    """Fallback: count specs on disk (used on startup and fallback polls)."""
    with self._counter_lock:
        old_active = self.active_count
        old_queued = self.queued_count

        self.active_count = self._count_specs_in(
            self.active_dir,
            stale_threshold_minutes=30  # Existing logic
        )
        self.queued_count = self._count_specs_in(
            self.queue_dir,
            pattern="SPEC-*.md"
        )

        if old_active != self.active_count or old_queued != self.queued_count:
            logger.info(
                f"Fallback refresh: active {old_active}→{self.active_count}, "
                f"queued {old_queued}→{self.queued_count}"
            )
```

### Event-Driven Loop

```python
def _daemon_loop(self):
    """Daemon background loop (event-driven with fallback)."""
    logger.info("Daemon loop started")

    # Initial count on startup
    self._refresh_counts()

    while self.running:
        try:
            # Wait for wake event or timeout
            woken = self.wake_event.wait(timeout=60)  # 60s fallback

            if woken:
                logger.info("Woken by MCP event, checking slots")
                self.wake_event.clear()
            else:
                logger.info("Fallback poll, refreshing counts")
                self._refresh_counts()  # Re-sync from disk

            # Run dispatch cycle
            self._dispatch_cycle()

        except Exception as e:
            logger.error(f"Error in daemon loop: {e}", exc_info=True)
            self._log_event({
                "ts": datetime.now(UTC).isoformat(),
                "event": "error",
                "error": str(e)
            })
            time.sleep(10)

    logger.info("Daemon loop exited")
```

### Dispatch Cycle (Use Counters)

```python
def _dispatch_cycle(self):
    """Run one dispatch cycle (uses in-memory counters)."""
    with self._counter_lock:
        active_count = self.active_count
        queued_count = self.queued_count

    available_slots = self.max_bees - active_count - queued_count

    self._log_event({
        "ts": datetime.now(UTC).isoformat(),
        "event": "cycle_start",
        "active": active_count,
        "queued": queued_count,
        "slots": available_slots,
        "max_bees": self.max_bees,
        "source": "mcp_counters" if self.mcp_enabled else "disk_scan"
    })

    # ... rest of dispatch cycle (unchanged) ...
```

### CLI Flag

```python
parser.add_argument("--mcp-enabled", action="store_true", default=True,
                    help="Enable MCP event-driven mode (default: True)")
```

## Constraints

- No file over 500 lines
- Preserve existing CLI interface (all flags still work)
- No breaking changes to `dispatched.jsonl` or `dispatcher_log.jsonl` formats
- Thread-safe counter updates (use lock)
- Counter underflow protection (never below 0)
- No stubs — fully implemented
- All existing tests must pass

## Dependencies

**Depends on:** TASK-MCP-QUEUE-02 (HTTP endpoints must exist)

**Can run in parallel with:** TASK-MCP-QUEUE-03 (scheduler refactor is independent)

## Estimated Duration

1.5-2 hours (Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-04-RESPONSE.md`

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
