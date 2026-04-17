# SPEC-MCP-TRANSPORT-FIX: Replace SSE with Streamable HTTP

## Objective

Update hivenode/hive_mcp/local_server.py from deprecated SSE transport to MCP Streamable HTTP transport. Update .mcp.json and integration tests.

## Context

Phase 0 built SSE transport, but MCP SDK has deprecated SSE in favor of Streamable HTTP. Fix before building more tools on top.

## Files to Read First
- hivenode/hive_mcp/local_server.py
- .mcp.json
- hivenode/hive_mcp/tests/test_integration.py
- hivenode/hive_mcp/tools/queue.py
- hivenode/hive_mcp/tools/tasks.py

## Files to Modify
- hivenode/hive_mcp/local_server.py
- .mcp.json
- hivenode/hive_mcp/tests/test_integration.py

## Deliverables
- [ ] local_server.py uses Streamable HTTP transport instead of SSE
- [ ] .mcp.json updated with correct transport type and URL
- [ ] Integration tests updated for new transport
- [ ] All existing tools still work (queue_list, queue_peek, task_list, task_read)

## Acceptance Criteria
- [ ] local_server.py uses Streamable HTTP transport (not SSE)
- [ ] .mcp.json updated with correct transport type and URL
- [ ] Server still runs on localhost:8421
- [ ] All existing tools still work (queue_list, queue_peek, task_list, task_read)
- [ ] Integration tests updated and passing
- [ ] Multiple concurrent clients still supported

## Smoke Test
- [ ] cd hivenode && python -m pytest hive_mcp/tests/test_integration.py -v — all tests pass
- [ ] cd hivenode && python -m pytest hive_mcp/tests/ -v — no regressions

## Constraints
- Check MCP Python SDK docs for current Streamable HTTP API
- Keep port 8421
- No stubs, TDD, 500-line limit

## Model Assignment
sonnet

## Priority
P0
