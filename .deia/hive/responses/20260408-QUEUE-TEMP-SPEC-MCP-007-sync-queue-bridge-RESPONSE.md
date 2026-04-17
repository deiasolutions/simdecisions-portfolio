# SPEC-MCP-007: Sync Queue Bridge + SSE Events Stream -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

## Files Modified

### New Files Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\events_sse.py` (124 lines)
  - SSE stream reader for sync queue
  - Converts sync queue events to Event Ledger format
  - Configurable polling interval (default 2s)
  - One-shot mode for testing

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_events_sse.py` (351 lines)
  - 10 comprehensive tests for SSE functionality
  - Tests cover: format conversion, event consumption, empty queue, missing directory, multiple events, all event types, corrupted file handling, timestamp generation

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\manual_sse_smoke_test.py` (73 lines)
  - Manual smoke test script for endpoint verification

### Modified Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` (991 lines, +38 lines)
  - Added import for `SyncQueueSSE`
  - Initialized `sync_queue_sse` instance
  - Added `events_sse_endpoint()` async handler
  - Registered `/mcp/events` route

## What Was Done

### Core Implementation
1. **Created `SyncQueueSSE` class** (`events_sse.py`)
   - Reads events from `~/.shiftcenter/sync_queue/` directory
   - Emits events as Server-Sent Events (SSE) format: `data: {...}\n\n`
   - Converts sync queue format to Event Ledger format:
     - `event_type`: From `type` field
     - `timestamp`: Preserved or auto-generated
     - `payload`: All fields except metadata (type, timestamp, synced, synced_at)
   - Consumes events by deleting files after emission
   - Gracefully handles missing directory and corrupted files
   - Configurable polling interval (default 2 seconds)
   - One-shot mode for testing (emit available events and exit)

2. **Integrated SSE endpoint into MCP server**
   - Added `/mcp/events` route to FastMCP app
   - Returns `text/event-stream` with proper headers (Cache-Control, Connection)
   - Streams events continuously via async generator

3. **Event Format Conversion**
   - Heartbeat events: Preserves bee_id, task_id, status, model, tokens, cost_usd, message
   - Claim events: Preserves task_id, claimed_by, claimed_at, status
   - Tool log events: Preserves tool_name, actor, parameters, result, cost_usd
   - Generates timestamps for events missing them (using timezone-aware UTC)

### Tests Created
10 tests covering all requirements:
- ✓ SSE stream format (Event Ledger schema compliance)
- ✓ Event consumption (files deleted after emission)
- ✓ Empty queue handling
- ✓ Missing directory handling
- ✓ Multiple events in chronological order
- ✓ Claim event format conversion
- ✓ Tool log event format conversion
- ✓ Corrupted file graceful skip
- ✓ Timestamp auto-generation
- ✓ Payload metadata exclusion

All 10 tests pass.

## Tests Run

```bash
pytest hivenode/hive_mcp/tests/test_events_sse.py -v
```

**Results:** 10/10 passed (100%)

## Acceptance Criteria

- [x] `/mcp/events` SSE endpoint added to MCP server
- [x] Reads files from `~/.shiftcenter/sync_queue/` directory
- [x] Emits events in Event Ledger format: `{"event_type": "...", "timestamp": "...", "payload": {...}}`
- [x] Events are consumed (files deleted from sync_queue after emission)
- [x] Polling interval configurable (default 2 seconds)
- [x] Graceful handling if sync_queue directory doesn't exist
- [x] Tests: SSE stream connection, event emission, empty queue, directory missing

## Smoke Test

The smoke test from the spec requires a running MCP server. Since the server at port 8421 is running old code (before today's changes), I created a manual smoke test script:

```bash
# Terminal 1: Restart MCP server with new code
python -m hivenode.hive_mcp.local_server

# Terminal 2: Run smoke test
python hivenode/hive_mcp/tests/manual_sse_smoke_test.py
```

**Note:** The production server needs to be restarted for the `/mcp/events` endpoint to become available. The current running instance (port 8421) was started before these changes were made.

## Blockers

None.

## Notes

1. **Deprecated API Fixed:** Replaced `datetime.utcnow()` with `datetime.now(timezone.utc)` to avoid deprecation warning.

2. **File Size Compliance:**
   - `events_sse.py`: 124 lines (well under 500)
   - `test_events_sse.py`: 351 lines (under 500)
   - `local_server.py`: 991 lines (under 1000 hard limit)

3. **Existing Infrastructure:**
   - The `SyncQueueWriter` was already implemented in `sync.py`
   - The Event Ledger schema was already defined in `ledger/schema.py`
   - This spec only needed to bridge them via SSE

4. **Design Choices:**
   - Events are consumed (deleted) immediately after emission to prevent duplicate delivery
   - Corrupted files are deleted after logging error (prevents queue blockage)
   - Keepalive comments (`: keepalive\n\n`) sent when no events available
   - Graceful degradation if sync_queue directory missing

5. **Future Enhancement:**
   - Consider adding event IDs for idempotency tracking
   - Consider adding event filtering by type or bee_id
   - Consider adding reconnection token for resuming from last event
