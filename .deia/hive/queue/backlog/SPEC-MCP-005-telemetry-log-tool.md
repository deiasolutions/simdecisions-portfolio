## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

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
Create a `telemetry_log` tool for bees to log individual tool invocations. Writes to Event Ledger for the surrogate training pipeline. Added to existing `tools/telemetry.py`.

## Files to Read First
- `hivenode/hive_mcp/tools/telemetry.py` — existing heartbeat and status tools, add here
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
- Add to existing `tools/telemetry.py`, do NOT create new file
- Use existing Event Ledger write path, do NOT create new one

## Triage History
- 2026-04-09T15:50:45.769483Z — requeued (empty output)
- 2026-04-09T15:55:45.825615Z — requeued (empty output)
- 2026-04-10T05:41:49.975012Z — requeued (empty output)
