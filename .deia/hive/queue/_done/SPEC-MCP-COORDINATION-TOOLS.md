# SPEC-MCP-COORDINATION-TOOLS: Briefing Write/Read/Ack Tools

## Objective

Implement briefing_write, briefing_read, briefing_ack MCP tools for Q33NR to Q33N coordination.

## Context

Phase 1 of SPEC-HIVE-MCP-001-v2. These tools enable acknowledged briefing delivery — the walkie-talkie click pattern where Q33NR knows Q33N received a briefing.

## Files to Read First
- hivenode/hive_mcp/local_server.py
- hivenode/hive_mcp/state.py
- hivenode/hive_mcp/tools/coordination.py
- hivenode/hive_mcp/tests/test_tools_coordination.py
- hivenode/hive_mcp/tools/queue.py
- hivenode/hive_mcp/tools/tasks.py

## Files to Modify
- hivenode/hive_mcp/tools/coordination.py
- hivenode/hive_mcp/tests/test_tools_coordination.py
- hivenode/hive_mcp/local_server.py

## Deliverables
- [ ] briefing_write creates file in .deia/hive/coordination/ with enforced naming
- [ ] briefing_read returns latest or specified briefing content
- [ ] briefing_ack writes timestamp to file header and state manager
- [ ] Tools registered in local_server.py

## Acceptance Criteria
- [ ] briefing_write creates file in .deia/hive/coordination/ with enforced naming
- [ ] briefing_read returns latest or specified briefing content
- [ ] briefing_ack writes timestamp to file header and state manager
- [ ] Naming convention validated (rejects malformed names)
- [ ] Path traversal rejected
- [ ] 10+ tests passing
- [ ] No stubs

## Smoke Test
- [ ] cd hivenode && python -m pytest hive_mcp/tests/test_tools_coordination.py -v — all tests pass
- [ ] cd hivenode && python -m pytest hive_mcp/tests/ -v — no regressions

## Constraints
- TDD, 500-line limit, Python 3.13
- Use existing state.py for ack storage
- Naming convention: YYYY-MM-DD-BRIEFING-*.md

## Depends On
- SPEC-MCP-TRANSPORT-FIX

## Model Assignment
sonnet

## Priority
P0
