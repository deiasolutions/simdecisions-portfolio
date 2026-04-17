---
id: MCP-RELIABILITY-001
priority: P1
model: sonnet
depends_on: BEE-TELEMETRY-001
area_code: factory
---

# SPEC-MCP-RELIABILITY-001: MCP Autostart and Watchdog

## Priority
P1

## Depends On
SPEC-BEE-TELEMETRY-001 (watchdog emits kill events to bee_events)

## Model Assignment
sonnet

## Objective

The MCP server (port 8421) is not started by `restart-services.sh` and silently dies on reboot. The scheduler MCP (8422) and dispatcher MCP (8423) are permanently down. Stall detection exists but is advisory-only — it warns but never kills or re-queues. This spec fixes all three: autostart, watchdog, and automatic intervention.

## Files to Read First

- `_tools/restart-services.sh`
  Current service list — MCP servers are missing
- `hivenode/hive_mcp/local_server.py`
  Main MCP server entry point (port 8421)
- `hivenode/scheduler/scheduler_mcp_server.py`
  Scheduler MCP server (port 8422)
- `hivenode/scheduler/dispatcher_mcp_server.py`
  Dispatcher MCP server (port 8423)
- `hivenode/hive_mcp/tools/telemetry.py`
  Lines 109-134: `_get_advisory()` stall detection — currently advisory-only
- `hivenode/routes/build_monitor.py`
  BuildState class — task tracking and file claims
- `hivenode/telemetry/bee_events.py`
  Bee lifecycle events (from BEE-TELEMETRY-001) — emit kill events here

## Deliverables

### Part 1: Autostart

- [ ] Add MCP server (port 8421) to `_tools/restart-services.sh` service list
- [ ] Start command: `python -m hivenode.hive_mcp.local_server`
- [ ] Add health check: `curl -s http://127.0.0.1:8421/health`
- [ ] Scheduler MCP (8422) and dispatcher MCP (8423): add to restart script ONLY if they have working entry points. If they're broken/incomplete, log a warning and skip. Do NOT fix broken servers in this spec.

### Part 2: Watchdog

- [ ] Add a watchdog function to `run_queue.py` (or a new `_tools/bee_watchdog.py` if run_queue.py would exceed 500 lines)
- [ ] On every queue tick, check all active bees:
  1. Read last heartbeat timestamp from BuildState
  2. If no heartbeat for > 30 minutes AND bee subprocess is still alive → emit warning
  3. If no heartbeat for > 60 minutes AND bee subprocess is still alive → kill the bee process, emit `killed` event to bee_events, release file claims, log: `[WATCHDOG] Killed stale bee <bee_id> (no heartbeat for <N> minutes)`
  4. If bee subprocess has exited but no result was recorded → emit `error` event, release file claims, re-queue the spec
- [ ] Watchdog MUST NOT kill bees that are legitimately long-running (some SWE-bench tasks take 24 minutes). The 60-minute threshold is for truly hung processes, not slow ones.

### Part 3: Automatic re-queue on stall

- [ ] When watchdog kills a stale bee, move the spec back to backlog (not _done, not _needs_review)
- [ ] Add a `retry_count` field to the spec frontmatter. Increment on each re-queue.
- [ ] If `retry_count >= 3`, move to `_needs_review/` instead of re-queuing. Log: `[WATCHDOG] Spec <id> failed 3 times — moved to _needs_review`

### Part 4: MCP health in status endpoint

- [ ] Add MCP server health to `GET /build/status` response:
  ```json
  {
    "mcp_server": {"port": 8421, "healthy": true},
    "scheduler_mcp": {"port": 8422, "healthy": false},
    "dispatcher_mcp": {"port": 8423, "healthy": false}
  }
  ```
- [ ] Health check: HTTP GET to each server's `/health` endpoint, timeout 2s

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Unit test: watchdog detects stale bee (mock heartbeat timestamp > 60 min ago)
- [ ] Unit test: watchdog does NOT kill bee with recent heartbeat
- [ ] Unit test: watchdog re-queues spec after kill
- [ ] Unit test: watchdog moves to _needs_review after 3 retries
- [ ] Unit test: MCP health check returns correct status
- [ ] Integration test: restart-services.sh starts MCP server
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- 60-minute kill threshold is a constant, not configurable. Change the constant if we need to adjust later.
- Do NOT fix broken MCP servers (8422, 8423) in this spec — just detect and report their status
