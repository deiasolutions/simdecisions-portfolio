---
id: MCP-005
priority: P1
model: sonnet
role: bee
depends_on: [MCP-002]
---
# SPEC-MCP-005: Telemetry Log Tool

## Priority
P1

## Model Assignment
sonnet

## Depends On
MCP-002

## Intent
Create a `telemetry_log` tool for bees to log individual tool invocations. Writes to Event Ledger for the surrogate training pipeline.

## Files to Modify
- `hivenode/hive_mcp/tools/telemetry.py` — add new tool here

## Files to Read (Context Only)
- `.deia/hive/scripts/queue/telemetry_logger.py` — Event Ledger write functions
- `hivenode/ledger/schema.py` — Event Ledger schema

## Acceptance Criteria
- [ ] New `telemetry_log` tool registered in MCP server
- [ ] Parameters: `bee_id` (required), `task_id` (required), `tool_name` (required), `input_tokens` (optional), `output_tokens` (optional), `duration_ms` (optional), `success` (optional, default true)
- [ ] Returns `{"logged": true, "event_id": "evt_..."}` with unique event ID
- [ ] Writes to Event Ledger via `telemetry_logger`
- [ ] Tests: log with all params, log with minimal params, verify Event Ledger entry

## Smoke Test
```bash
cd hivenode && python -m pytest tests/hivenode/test_mcp_tools.py -k telemetry_log -v
```

## Constraints
- No file over 500 lines
- TDD: tests first
- Do not create new tool files — this tool belongs in the existing telemetry module
- Use existing Event Ledger write path from `telemetry_logger.py`
