# QUEUE-TEMP-SPEC-MCP-003: Queue State Tool (Grouped Format) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\queue.py` — Added `queue_state()` function (70 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` — Registered `queue_state` tool in MCP server (2 locations)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_queue.py` — Added 7 comprehensive tests + fixture (175 lines)

## What Was Done

- Created `queue_state(include_done: bool = False)` function in `tools/queue.py`
- Function scans three queue directories:
  - `_active/` → returns as "active" list
  - `backlog/` → returns as "pending" list
  - `_done/` → returns as "done" list (only when include_done=true)
- Each entry includes: file_name, priority, area_code, created (ISO timestamp)
- Registered tool in MCP server `handle_list_tools()` with schema
- Added handler in `handle_call_tool()` to route requests to `queue.queue_state()`
- Added FastMCP decorator function `@fast_mcp.tool() async def queue_state()`
- Existing `queue_list()` tool unchanged (backward compatibility preserved)
- Handles missing directories gracefully (returns empty lists)
- Ignores non-markdown files (.gitkeep, .txt, .json, etc.)
- Created 7 comprehensive pytest tests:
  1. `test_queue_state_empty_queue` — empty queue returns empty lists
  2. `test_queue_state_without_include_done` — default behavior excludes done
  3. `test_queue_state_with_include_done` — include_done=true returns done specs
  4. `test_queue_state_mixed_states` — all 5 specs across states
  5. `test_queue_state_directory_missing_gracefully` — missing _active/_done OK
  6. `test_queue_state_ignores_non_md_files` — ignores .gitkeep, .txt, .json
  7. `test_queue_state_preserves_queue_list_behavior` — backward compat check
- All 19 queue tool tests pass (12 existing + 7 new)

## Tests Run

```bash
cd hivenode && python -m pytest hive_mcp/tests/test_tools_queue.py -v
```

**Result:** 19 passed in 0.57s

All acceptance criteria met:
- ✅ New `queue_state` tool registered in MCP server
- ✅ Parameters: `include_done` (optional bool, default false)
- ✅ Returns grouped format: `{"active": [...], "pending": [...], "done": [...]}`
- ✅ `active` scans `_active/` directory
- ✅ `pending` scans `backlog/` directory
- ✅ `done` scans `_done/` directory (only when include_done=true)
- ✅ Each entry includes: file_name, priority, area_code, created
- ✅ Existing `queue_list` tool unchanged
- ✅ Tests cover: empty queue, mixed states, include_done flag, missing directories

## Smoke Test

```bash
cd hivenode && python -m pytest hive_mcp/tests/test_tools_queue.py -k queue_state -v
```

**Result:** 7 passed in 0.65s ✅

## Notes

- Tool follows same pattern as existing queue tools (queue_list, queue_peek)
- Uses existing `_extract_metadata()` and `_find_repo_root()` helpers
- MCP server must be restarted to pick up new tool registration
- No file over 500 lines (queue.py is 383 lines total)
- TDD followed: tests written first, then implementation
- Grouped format provides clearer view of queue state than flat list
- Backward compatible: queue_list continues to work for legacy callers

## Dependencies

Depends on MCP-001 (health endpoint) — satisfied ✅
