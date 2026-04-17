# SPEC-FACTORY-MCP-HEARTBEAT-001-forward: Forward MCP Heartbeats to BuildState

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

The MCP heartbeat tool in `hive_mcp/local_server.py` writes to its own `StateManager` but does NOT forward heartbeats to hivenode's `BuildState` at `/build/heartbeat`. This means bees using MCP heartbeats are invisible to the build monitor. Fix this by forwarding MCP heartbeats to hivenode's HTTP endpoint so both state stores stay in sync.

## Files to Read First

- hivenode/hive_mcp/local_server.py
- hivenode/routes/build_monitor.py
- .deia/hive/scripts/queue/run_queue.py

## Acceptance Criteria

- [ ] MCP `heartbeat` tool in `local_server.py` forwards heartbeat data to `http://127.0.0.1:8420/build/heartbeat` after writing to StateManager
- [ ] Forwarding is best-effort (swallow errors silently, do not block the MCP response)
- [ ] Forwarded payload matches the schema expected by `/build/heartbeat` (task_id, status, model, role, message)
- [ ] Bees using MCP heartbeat appear in `/build/status` response
- [ ] Existing MCP StateManager behavior is unchanged (dual-write, not replace)
- [ ] All existing tests still pass
- [ ] 3+ new tests covering: forwarding success, forwarding failure (connection refused), payload mapping

## Smoke Test

- [ ] Start hivenode, send a heartbeat via MCP tool, verify task appears in `curl -s http://127.0.0.1:8420/build/status`

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Do not modify build_monitor.py — only change the MCP side
