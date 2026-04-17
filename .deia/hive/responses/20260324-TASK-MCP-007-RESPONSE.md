# TASK-MCP-007: Dispatch, Heartbeat, Telemetry, Sync Queue -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-24

## Files Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\dispatch.py` (110 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\telemetry.py` (165 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\sync.py` (212 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_dispatch.py` (100 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_telemetry.py` (171 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_sync.py` (238 lines)

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` (added dispatch_bee, heartbeat, status_report, cost_summary tools)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\__init__.py` (added dispatch, telemetry to exports)

## What Was Done

### Dispatch Tools (`dispatch.py`)
- Implemented `dispatch_bee()` function that wraps existing `dispatch.py` script
- Spawns bee as subprocess in background mode (non-blocking)
- Validates task file existence and role parameter
- Auto-detects repo root via `.deia/` marker
- Passes all args correctly: task_file, model, role, inject_boot
- Returns PID and dispatch confirmation with timestamp

### Telemetry Tools (`telemetry.py`)
- Implemented `heartbeat()` function that:
  - Stores heartbeat data in StateManager (bee_id, task_id, status, model, tokens, cost, message)
  - POSTs to existing `/build/heartbeat` endpoint (localhost:8420)
  - Handles optional fields (input_tokens, output_tokens, cost_usd, message)
  - Returns confirmation with timestamp and endpoint status
- Implemented `status_report()` function that:
  - Aggregates all active bees and their tasks from StateManager
  - Returns bee count, task count, and detailed bee/task lists
- Implemented `cost_summary()` function that:
  - Calculates total cost_usd, input_tokens, output_tokens from all heartbeats
  - Computes CLOCK (time estimate), COIN (USD cost), CARBON (CO2 estimate)
  - Returns aggregated three-currency summary

### Sync Queue (`sync.py`)
- Implemented `SyncQueueWriter` class for offline-first cloud sync
- Writes JSON messages to `~/.shiftcenter/sync_queue/` (outside OneDrive)
- Three message types: claim, heartbeat, tool_log
- Each message written as individual JSON file with timestamp-based naming
- Filename uniqueness guaranteed via microseconds + nanoseconds
- `write_claim()`, `write_heartbeat()`, `write_tool_log()` methods
- `list_pending()` returns unsynced messages (synced=False)
- `mark_synced()` updates message synced flag and timestamp
- Creates queue directory if it doesn't exist

### MCP Server Integration (`local_server.py`)
- Registered 4 new tools in tool list: dispatch_bee, heartbeat, status_report, cost_summary
- Added tool call handlers in `handle_call_tool()` function
- Added FastMCP wrapper handlers for all 4 tools
- Integrated sync queue writer: heartbeat tool writes to sync queue on every call
- Initialized `SyncQueueWriter` instance in server startup

### Tests
- **test_tools_dispatch.py**: 5 tests (subprocess spawning, arg passing, validation, background mode)
- **test_tools_telemetry.py**: 7 tests (state storage, endpoint POST, aggregation, optional fields)
- **test_sync.py**: 12 tests (directory creation, JSON writes, content validation, uniqueness, pending list, mark synced)
- All 24 tests passing with TDD approach (tests written first, then implementation)

## Test Results

```
hivenode/hive_mcp/tests/test_tools_dispatch.py: 5 passed
hivenode/hive_mcp/tests/test_tools_telemetry.py: 7 passed
hivenode/hive_mcp/tests/test_sync.py: 12 passed
====================== 24 passed, 35 warnings in 34.39s ======================
```

All tests green. Warnings are deprecation warnings for `datetime.utcnow()` (Python 3.12+ prefers `datetime.now(datetime.UTC)`), but functionality is correct.

## Build Verification

Tests run via pytest, all passing. No build errors. No import errors. All modules correctly integrated into MCP package structure.

Integration test: MCP server can be imported and tools are registered correctly (verified via tool list output).

## Acceptance Criteria

- [x] dispatch_bee runs dispatch.py as subprocess and returns PID
- [x] dispatch_bee passes all args correctly (task_file, model, role, inject_boot)
- [x] heartbeat stores data in state manager
- [x] heartbeat POSTs to /build/heartbeat endpoint
- [x] status_report returns all active bees and tasks from state
- [x] cost_summary returns aggregated CLOCK/COIN/CARBON
- [x] Sync queue writes JSON files to `~/.shiftcenter/sync_queue/`
- [x] Sync queue creates directory if it doesn't exist
- [x] 24 tests passing (exceeds 15+ minimum requirement)
- [x] No stubs (all functions fully implemented)

## Clock / Cost / Carbon

**CLOCK:** ~45 minutes (implementation + tests + debugging uniqueness issue)
**COIN:** ~$0.15 USD (Sonnet model, ~800 input tokens, ~4,500 output tokens per iteration, 3 iterations)
**CARBON:** ~0.5g CO2 (estimated based on token count)

## Issues / Follow-ups

### Resolved During Implementation
- **Filename uniqueness issue:** Initial implementation used only microseconds for uniqueness, which caused collisions in tight loops. Fixed by adding nanoseconds from `time.perf_counter_ns()` to ensure uniqueness even when writing multiple messages in rapid succession.

### Deprecation Warnings
- `datetime.utcnow()` is deprecated in Python 3.12+. Should be replaced with `datetime.now(datetime.UTC)` in future refactor. Not blocking, as functionality is correct.

### Future Phase 3 Work
- Sync queue flusher (consumer) not implemented yet — that's Phase 3 cloud sync
- Cloud-to-local pull mechanism not implemented yet — also Phase 3
- Tool log writing not yet integrated into all MCP tool calls — will be added as tools are expanded

### Architecture Notes
- Heartbeat is opt-in for bees (per spec). dispatch.py continues its own heartbeat as fallback. The MCP `heartbeat` tool enables bees to heartbeat directly, but adoption will be monitored in Phase 1.
- dispatch_bee wraps existing dispatch.py script rather than reimplementing — good reuse, no duplication
- Sync queue uses same pattern as Named Volume System sync queue (same directory, same JSON-per-message pattern)

### Next Tasks
- TASK-MCP-005: Write tools (coordination tools phase)
- TASK-MCP-006: Dispatch telemetry (extended logging for dispatch operations)
- Phase 3: Cloud sync flusher implementation
