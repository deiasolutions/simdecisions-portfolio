---
id: BEE-TELEMETRY-001
priority: P0
model: sonnet
depends_on: RATELIMIT-001
area_code: factory
---

# SPEC-BEE-TELEMETRY-001: Bee Lifecycle Telemetry

## Priority
P0

## Depends On
SPEC-RATELIMIT-001 (uses the rate_limited flag it introduces)

## Model Assignment
sonnet

## Objective

Every bee must have a queryable lifecycle record with discrete timestamped events: launched, first-heartbeat, result-produced, rate-limited, error, killed, timed-out. Currently bee timing data is scattered across RAW filenames, file contents, and MCP heartbeats with no single source of truth. After this spec, one query returns the full timeline for any bee or any benchmark run.

## Background

During the SWE-bench benchmark (731 tasks), answering "what was the concurrency profile?" required parsing 726 filenames, reading duration fields from each file, and reconstructing timelines manually. This took 20+ minutes of agent research. It should take one command.

## Files to Read First

- `hivenode/routes/build_monitor.py`
  BuildState class, monitor-state.json persistence — understand existing state tracking
- `hivenode/routes/build_monitor_liveness.py`
  Liveness ping system — understand existing heartbeat flow
- `hivenode/hive_mcp/tools/telemetry.py`
  MCP heartbeat tool, stall detection — understand existing telemetry
- `.deia/hive/scripts/dispatch/dispatch.py`
  `dispatch_bee()` — where launch events should be emitted
- `.deia/hive/scripts/queue/run_queue.py`
  Queue loop — where completion/kill/timeout events should be emitted
- `.deia/hive/queue/monitor-state.json`
  Current state format — understand what's already persisted

## Deliverables

### Part 1: Event schema

- [ ] Define a `BeeLifecycleEvent` dataclass or TypedDict:
  ```python
  {
    "bee_id": str,          # unique per dispatch
    "task_id": str,         # spec or task file name
    "event": str,           # launched | heartbeat | result | rate_limited | error | killed | timeout
    "timestamp_utc": str,   # ISO 8601
    "model": str,           # sonnet | haiku | opus | gemini-2.0-flash | etc
    "metadata": dict        # event-specific: cost_usd, duration_s, tokens, error_message, etc
  }
  ```

### Part 2: Event log storage

- [ ] Create `hivenode/telemetry/bee_events.py` — append-only event log
- [ ] Store events in a local SQLite database at `.deia/hive/bee_events.db`
- [ ] Table: `bee_events(id INTEGER PRIMARY KEY, bee_id TEXT, task_id TEXT, event TEXT, timestamp_utc TEXT, model TEXT, metadata JSON)`
- [ ] Index on `bee_id`, `task_id`, `timestamp_utc`
- [ ] Provide functions: `log_event(...)`, `get_bee_timeline(bee_id)`, `get_run_summary(start_utc, end_utc)`, `get_concurrency_profile(start_utc, end_utc)`

### Part 3: Event emission points

- [ ] `dispatch.py:dispatch_bee()` — emit `launched` event when bee subprocess starts
- [ ] `dispatch.py:dispatch_bee()` — emit `result` event when bee returns (include cost, duration, success)
- [ ] `dispatch.py:dispatch_bee()` — emit `rate_limited` event when bee returns rate-limited (from RATELIMIT-001)
- [ ] `dispatch.py:dispatch_bee()` — emit `error` event on adapter exceptions
- [ ] `dispatch.py:dispatch_bee()` — emit `timeout` event if bee exceeds timeout
- [ ] `run_queue.py` — emit `killed` event if queue runner terminates a bee
- [ ] MCP heartbeat tool — emit `heartbeat` event (sampling: every 5th heartbeat, not every one)

### Part 4: Query CLI

- [ ] Add subcommand to an existing CLI (or create `_tools/bee_telemetry.py`):
  - `bee-telemetry timeline <bee_id>` — full event list for one bee
  - `bee-telemetry run-summary --start <iso> --end <iso>` — summary stats for a time window
  - `bee-telemetry concurrency --start <iso> --end <iso>` — minute-by-minute concurrent bee count with mean/median/mode
  - `bee-telemetry cost --start <iso> --end <iso>` — total cost, cost/task, cost/hour
- [ ] Output as formatted table to stdout

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Unit test: `log_event()` writes to SQLite correctly
- [ ] Unit test: `get_bee_timeline()` returns events in chronological order
- [ ] Unit test: `get_concurrency_profile()` correctly calculates overlapping bee windows
- [ ] Unit test: `get_run_summary()` returns accurate counts and stats
- [ ] Integration test: dispatch emits launched + result events
- [ ] Integration test: rate_limited event emitted when adapter returns rate_limited
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- SQLite for local storage — NOT Railway PG. This is local-only operational data.
- Do NOT log every MCP heartbeat — sample every 5th to avoid bloat
- bee_events.db is .gitignored (operational, not source)
