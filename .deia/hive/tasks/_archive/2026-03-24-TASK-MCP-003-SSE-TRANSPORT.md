# TASK-MCP-003: Hive MCP SSE Transport + Integration Test

## Objective
Wire SSE transport on localhost:8421, create `.mcp.json` in repo root, write integration test proving a client can connect and call tools.

## Context
Phase 0 of SPEC-HIVE-MCP-001-v2. This task completes the MCP server foundation by exposing it via SSE and verifying end-to-end connectivity.

**Dependencies:** TASK-MCP-001 (state.py), TASK-MCP-002 (tools)

**Spec location:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

**MCP Python SDK:** Use `mcp` package for protocol compliance. Check current API at https://pypi.org/project/mcp/

## Files to Read First
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 3.1, 7.2, 7.3, 9.1)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\queue.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\tasks.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (FastAPI app structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (route registration pattern)

## Deliverables
- [ ] Create `hivenode/hive_mcp/local_server.py`:
  - **Separate FastAPI app** (NOT a router on the main hivenode app) running on port 8421
  - The MCP server is its own process/uvicorn instance — hivenode stays on 8420, MCP SSE on 8421
  - MCP protocol handler using `mcp` Python SDK
  - Tool registration: `queue_list`, `queue_peek`, `task_list`, `task_read`
  - Handles multiple concurrent clients (SSE supports this natively)
  - Returns MCP protocol responses (tool results, errors, metadata)
  - Entry point: `python -m hivenode.hive_mcp.local_server` starts uvicorn on 8421
- [ ] Do NOT register MCP routes in `hivenode/routes/__init__.py` — the MCP server is a separate process on a separate port
- [ ] Create `.mcp.json` in repo root:
  ```json
  {
    "mcpServers": {
      "hive-local": {
        "type": "sse",
        "url": "http://localhost:8421/mcp/sse"
      }
    }
  }
  ```
- [ ] Update `hivenode/hive_mcp/__init__.py`:
  - Export StateManager, tools, local_server
- [ ] Create integration test `hivenode/hive_mcp/tests/test_integration.py`:
  - Start hivenode server in background (subprocess or TestClient)
  - Connect to SSE endpoint as MCP client
  - Call `task_list` tool via MCP protocol
  - Verify structured response
  - Clean shutdown

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `hivenode/hive_mcp/tests/test_integration.py` (5+ tests)
- [ ] Test coverage:
  - SSE endpoint responds to connection
  - MCP tool listing returns all 4 tools (queue_list, queue_peek, task_list, task_read)
  - Calling `task_list` via MCP returns structured data
  - Calling `queue_list` via MCP returns structured data
  - Multiple concurrent clients can connect (2+ clients in same test)
  - Invalid tool calls return MCP error responses
- [ ] All tests pass (minimum 5 tests)
- [ ] Integration test runs against real FastAPI server (not mocked)
- [ ] Use httpx or SSE client library for MCP client simulation

## Constraints
- No file over 500 lines
- No hardcoded colors (N/A — backend only)
- No stubs — every function fully implemented
- Python 3.13
- Use `mcp` Python SDK for MCP protocol compliance
- SSE port must be configurable (default 8421 from spec)
- Do NOT use stdio transport (spec requires SSE for multi-client support)
- Router must integrate cleanly with existing hivenode FastAPI app

## Acceptance Criteria
- [ ] SSE endpoint `/mcp/sse` responds on http://localhost:8421
- [ ] `.mcp.json` exists in repo root with correct URL
- [ ] MCP client can list available tools (queue_list, queue_peek, task_list, task_read)
- [ ] MCP client can call `task_list` and receive structured response
- [ ] Integration test proves end-to-end connectivity
- [ ] All 5+ tests pass
- [ ] No stub functions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-003-RESPONSE.md`

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
