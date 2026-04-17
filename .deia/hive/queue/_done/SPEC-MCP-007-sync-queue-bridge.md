---
id: MCP-007
priority: P2
model: sonnet
role: bee
depends_on: [MCP-002]
---
# SPEC-MCP-007: Sync Queue Bridge + SSE Events Stream

## Priority
P2

## Model Assignment
sonnet

## Depends On
MCP-002

## Intent
Wire the existing sync queue (`~/.shiftcenter/sync_queue/`) into the MCP server as a `/mcp/events` SSE stream. Frontend can subscribe to get real-time build events. Event format matches Event Ledger schema.

## Files to Read First
- `hivenode/hive_mcp/sync.py` — existing SyncQueueWriter, reads/writes to sync_queue
- `hivenode/hive_mcp/local_server.py` — MCP server, add SSE endpoint here
- `hivenode/ledger/schema.py` — Event Ledger schema for event format

## Acceptance Criteria
- [ ] `/mcp/events` SSE endpoint added to MCP server
- [ ] Reads files from `~/.shiftcenter/sync_queue/` directory
- [ ] Emits events in Event Ledger format: `{"event_type": "...", "timestamp": "...", "payload": {...}}`
- [ ] Events are consumed (files deleted from sync_queue after emission)
- [ ] Polling interval configurable (default 2 seconds)
- [ ] Graceful handling if sync_queue directory doesn't exist
- [ ] Tests: SSE stream connection, event emission, empty queue, directory missing

## Smoke Test
```bash
curl -s -N http://localhost:8421/mcp/events &
# Trigger a heartbeat, verify event appears in stream
```

## Constraints
- No file over 500 lines
- TDD: tests first
- Do NOT modify existing `sync.py` write path
- Event format MUST match Event Ledger schema
