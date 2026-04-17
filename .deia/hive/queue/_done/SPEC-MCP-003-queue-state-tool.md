---
id: MCP-003
priority: P1
model: sonnet
role: bee
depends_on: [MCP-001]
---
# SPEC-MCP-003: Queue State Tool (Grouped Format)

## Priority
P1

## Model Assignment
sonnet

## Depends On
MCP-001

## Intent
Create a `queue_state` tool that returns queue contents grouped by status (active, pending, done). Scans `.deia/hive/queue/`, `_active/`, and `_done/` directories. Keep existing `queue_list` tool unchanged for backward compat.

## Files to Read First
- `hivenode/hive_mcp/tools/queue.py` — existing `queue_list` and `queue_peek` tools
- `.deia/hive/queue/` — queue directory structure (backlog/, _active/, _done/, _needs_review/)
- `.deia/hive/scripts/queue/spec_parser.py` — how specs are parsed

## Acceptance Criteria
- [ ] New `queue_state` tool registered in MCP server
- [ ] Parameters: `include_done` (optional bool, default false)
- [ ] Returns `{"active": [...], "pending": [...], "done": [...]}` grouped format
- [ ] `active` scans `_active/` directory
- [ ] `pending` scans `backlog/` directory (same as current queue_list)
- [ ] `done` scans `_done/` directory (only when include_done=true)
- [ ] Each entry includes: `file_name`, `priority`, `area_code`, status-specific fields
- [ ] Existing `queue_list` tool unchanged
- [ ] Tests: empty queue, mixed states, include_done flag, directory missing gracefully

## Smoke Test
```bash
cd hivenode && python -m pytest tests/hivenode/test_mcp_tools.py -k queue_state -v
```

## Constraints
- No file over 500 lines
- TDD: tests first
- Add to existing `tools/queue.py`, do NOT create new file
- Do NOT modify `queue_list` behavior
