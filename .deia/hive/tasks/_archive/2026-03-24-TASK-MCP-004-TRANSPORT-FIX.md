# TASK-MCP-004: Replace SSE with Streamable HTTP Transport

## Objective
Update `hivenode/hive_mcp/local_server.py` from deprecated SSE transport to MCP Streamable HTTP transport, update `.mcp.json` config, and fix integration tests.

## Context
Phase 0 MCP server uses SSE transport, but MCP SDK has deprecated SSE in favor of Streamable HTTP. This must be fixed before building additional Phase 1 tools on top. The server currently provides 4 tools: `queue_list`, `queue_peek`, `task_list`, `task_read`. All must continue working after the transport change.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.mcp.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_integration.py`
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 3.1, 7.1, 7.3)

## Deliverables
- [ ] Update `local_server.py` to use Streamable HTTP transport (not SSE)
- [ ] Update `.mcp.json` with correct transport type and connection URL
- [ ] Update `test_integration.py` for new transport
- [ ] All existing Phase 0 tools still work (queue_list, queue_peek, task_list, task_read)
- [ ] Server still runs on localhost:8421
- [ ] Multiple concurrent clients still supported

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All integration tests pass
- [ ] Edge cases tested:
  - Concurrent client connections
  - Transport negotiation
  - Graceful shutdown
  - Tool invocation through new transport

## Constraints
- Port 8421 must not change
- No file over 500 lines
- No stubs
- Check MCP Python SDK docs for current Streamable HTTP API
- All existing tools must continue working without modification

## Acceptance Criteria
- [ ] local_server.py uses Streamable HTTP transport class
- [ ] .mcp.json updated with transport: "streamable-http" and url: "http://localhost:8421"
- [ ] Server starts successfully and accepts connections
- [ ] All 4 Phase 0 tools respond correctly through new transport
- [ ] Integration tests updated and passing (10+ tests)
- [ ] No SSE transport code remaining

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-004-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
