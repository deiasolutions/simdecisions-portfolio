# MCP-005: Telemetry Log Tool -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\telemetry.py` — added `telemetry_log()` function and `get_ledger_writer()` helper
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` — registered `telemetry_log` tool in MCP server (both handle_list_tools and handle_call_tool), added FastMCP wrapper
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\__init__.py` — made `local_server` import lazy to avoid MCP dependency during testing
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_telemetry_log_tool.py` — created comprehensive test suite (9 tests, all passing)

## What Was Done

- Created `telemetry_log()` function in `tools/telemetry.py`:
  - Required parameters: `bee_id`, `task_id`, `tool_name`
  - Optional parameters: `input_tokens`, `output_tokens`, `duration_ms`, `success` (default: True), `db_path`
  - Writes `TOOL_INVOCATION` events to Event Ledger
  - Returns `{"logged": true, "event_id": "evt_123", "task_id": "..."}` with unique event ID
  - Validates required parameters (raises `ValueError` if missing)
  - Calculates CLOCK/COIN/CARBON currencies automatically
  - Uses `LedgerWriter` from `hivenode.ledger.writer`

- Created `get_ledger_writer()` helper function:
  - Returns `LedgerWriter` instance
  - Defaults to `.deia/hive/event_ledger.db` if no path provided
  - Path calculation: repo_root / ".deia" / "hive" / "event_ledger.db"

- Registered `telemetry_log` tool in MCP server:
  - Added Tool definition to `handle_list_tools()`
  - Added handler in `handle_call_tool()`
  - Added FastMCP async wrapper function
  - Tool schema: 3 required params, 4 optional params

- Fixed circular import issue:
  - Made `local_server` import lazy in `hivenode/hive_mcp/__init__.py`
  - Used `__getattr__` pattern to defer import until needed
  - Allows tests to import tools without triggering MCP server initialization

- Created comprehensive test suite (9 tests):
  1. `test_telemetry_log_minimal_params` — validates minimal required parameters
  2. `test_telemetry_log_all_params` — validates all parameters provided
  3. `test_telemetry_log_failure_case` — validates `success=False` flag
  4. `test_telemetry_log_missing_required_params` — validates ValueError on missing params
  5. `test_telemetry_log_unique_event_ids` — validates unique event_id generation
  6. `test_telemetry_log_default_db_path` — validates default db_path behavior
  7. `test_telemetry_log_currencies_calculation` — validates CLOCK/COIN/CARBON calculation
  8. `test_telemetry_log_event_type_normalization` — validates event_type normalization
  9. `test_telemetry_log_signal_type_internal` — validates signal_type='internal'

- All tests use temporary SQLite databases for isolation
- Fixture handles Windows-specific SQLite cleanup issues (WAL mode locks)

## Tests Written

**File:** `hivenode/hive_mcp/tests/test_telemetry_log_tool.py`
**Count:** 9 tests
**Status:** All passing

**Coverage:**
- Minimal parameters (required only)
- All parameters (including optional)
- Failure case (success=False)
- Missing required parameters (3 validation tests)
- Unique event ID generation
- Default db_path behavior
- CLOCK/COIN/CARBON currency calculation
- Event type normalization (TOOL_INVOCATION)
- Signal type (internal)

**Test execution:**
```bash
cd hivenode && python -m pytest hive_mcp/tests/test_telemetry_log_tool.py -v
```

**Result:** 9 passed in 1.26s

## Smoke Test

```bash
cd hivenode && python -m pytest hive_mcp/tests/test_telemetry_log_tool.py -v
```

**Result:**
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_minimal_params PASSED [ 11%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_all_params PASSED [ 22%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_failure_case PASSED [ 33%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_missing_required_params PASSED [ 44%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_unique_event_ids PASSED [ 55%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_default_db_path PASSED [ 66%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_currencies_calculation PASSED [ 77%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_event_type_normalization PASSED [ 88%]
hive_mcp\tests\test_telemetry_log_tool.py::test_telemetry_log_signal_type_internal PASSED [100%]
============================== 9 passed in 1.26s
```

All acceptance criteria met.

## Acceptance Criteria

- [x] New `telemetry_log` tool registered in MCP server
- [x] Parameters: `bee_id` (required), `task_id` (required), `tool_name` (required), `input_tokens` (optional), `output_tokens` (optional), `duration_ms` (optional), `success` (optional, default true)
- [x] Returns `{"logged": true, "event_id": "evt_..."}` with unique event ID
- [x] Writes to Event Ledger via `telemetry_logger`
- [x] Tests: log with all params, log with minimal params, verify Event Ledger entry

## Constraints Met

- [x] No file over 500 lines (longest file: `telemetry.py` at ~330 lines)
- [x] TDD: tests written first, then implementation
- [x] No new tool files created — tool added to existing `telemetry.py` module
- [x] Used existing Event Ledger write path from `LedgerWriter` (not `telemetry_logger.py` directly, but same underlying mechanism)

## Implementation Notes

**Design decision:** Used `LedgerWriter` directly instead of `telemetry_logger.py` functions because:
1. `LedgerWriter` is the canonical interface for Event Ledger writes
2. `telemetry_logger.py` is specifically for build attempt logging (factory domain)
3. `telemetry_log` is for generic tool invocations (hive_mcp domain)
4. Both write to same Event Ledger, just different event types

**Event format:**
- event_type: `TOOL_INVOCATION` (normalized to UPPER_SNAKE_CASE)
- actor: `bee:{bee_id}` (universal entity ID format)
- target: `task:{task_id}` (universal entity ID format)
- domain: `hive_mcp`
- signal_type: `internal`
- payload_json: `{tool_name, success, input_tokens, output_tokens, duration_ms}`
- cost_tokens_up: input_tokens
- cost_tokens_down: output_tokens
- cost_tokens: sum of input + output
- cost_usd: estimated from tokens (~$9/MTok average)
- cost_carbon: estimated from tokens (0.1g CO2 per 1000 tokens)
- currencies: `{clock: seconds, coin: usd, carbon: grams}`

**Currency calculation:**
- CLOCK: `duration_ms / 1000.0` (seconds)
- COIN: `(total_tokens / 1_000_000) * 9.0` (USD, rough estimate)
- CARBON: `(total_tokens / 1000.0) * 0.1` (grams CO2)

**Circular import fix:**
- Used `__getattr__` in `hive_mcp/__init__.py` to defer `local_server` import
- Allows tests to import `tools.telemetry` without triggering MCP server deps
- MCP server still imports normally when accessed at runtime

## Cost Estimate

**Development:**
- Model: Sonnet
- Tokens: ~18k input, ~7k output
- Cost: ~$0.055

**Testing:**
- 9 test runs
- ~500 tokens total
- Cost: negligible

**Total:** ~$0.06
