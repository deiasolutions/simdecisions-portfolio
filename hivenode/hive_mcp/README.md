# Hive MCP — Model Context Protocol Server

Local MCP server providing typed, acknowledged, tool-call-based communication between hive roles (Q33NR, Q33N, bees).

## Architecture

The Hive MCP server is a **separate FastAPI application** running on `localhost:8421` (not integrated into the main hivenode on port 8420). It provides MCP protocol access to hive state and operations via SSE transport.

```
┌─────────────────┐
│  Claude Code    │
│  (MCP Client)   │
└────────┬────────┘
         │ SSE
         │ http://localhost:8421/mcp/sse
         │
┌────────▼────────────────────────┐
│  Hive MCP Server (port 8421)    │
│  - SSE Transport                │
│  - 4 Phase 0 Tools              │
│  - State Manager                │
└────────┬────────────────────────┘
         │
         │ Read/Write
         │
┌────────▼────────────────────────┐
│  .deia/hive/                    │
│  - queue/ (specs)               │
│  - tasks/ (task files)          │
│  - responses/                   │
└─────────────────────────────────┘
```

## Phase 0 Tools

- **`queue_list`**: List specs in `.deia/hive/queue/` with optional filters (status, area_code, priority)
- **`queue_peek`**: Read a specific spec file from the queue
- **`task_list`**: List task files in `.deia/hive/tasks/` with optional filters (assigned_bee, wave, status)
- **`task_read`**: Read a specific task file with parsed YAML frontmatter

## Running the Server

```bash
# Start server
python -m hivenode.hive_mcp.local_server

# Server starts on localhost:8421
# MCP SSE endpoint: http://localhost:8421/mcp/sse
# Health check: http://localhost:8421/health
```

## Configuration

The `.mcp.json` file in the repo root tells Claude Code about the MCP server:

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

Claude Code automatically discovers available tools via the MCP protocol's tool listing.

## State Management

- **In-memory state:** Held in StateManager (Python dicts) for fast access
- **JSON backup:** Auto-flushed to `~/.shiftcenter/hive_state/hive_state.json`
- **Thread-safe:** All operations serialized via locks
- **Survives restarts:** State reloads from JSON on startup

## Testing

```bash
# Run all MCP tests (58 tests)
pytest hivenode/hive_mcp/tests/

# Run integration tests only (10 tests)
pytest hivenode/hive_mcp/tests/test_integration.py

# Run with coverage
pytest hivenode/hive_mcp/tests/ --cov=hivenode.hive_mcp
```

## Development

### Adding a New Tool

1. Create tool function in `hivenode/hive_mcp/tools/`
2. Register tool in `local_server.py` `handle_list_tools()`
3. Add handler logic in `local_server.py` `handle_call_tool()`
4. Write tests in `hivenode/hive_mcp/tests/`

Example:

```python
# In handle_list_tools()
Tool(
    name="my_new_tool",
    description="What this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "arg1": {"type": "string", "description": "..."}
        },
        "required": ["arg1"]
    }
)

# In handle_call_tool()
elif name == "my_new_tool":
    result = my_module.my_function(arguments.get("arg1"))
    return [TextContent(type="text", text=json.dumps(result))]
```

## Security

- All file operations validate paths (no traversal, no absolute paths)
- Archived tasks rejected (`_archive` paths blocked)
- SSE transport includes DNS rebinding protection (MCP SDK)
- State manager uses atomic writes (temp file + move)

## Roadmap

- **Phase 0 (current):** Read-only tools (queue_list, task_list, task_read, queue_peek)
- **Phase 1:** Write tools (briefing_write, task_write, response_submit, dispatch_bee)
- **Phase 2:** Context delivery (work_package, inventory_query, spec_search)
- **Phase 3:** Cloud MCP server on Railway (PostgreSQL backend)
- **Phase 4:** Mid-task coordination (redirect, heartbeat-based)

## Links

- **Spec:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`
- **Task:** `.deia/hive/tasks/2026-03-24-TASK-MCP-003-SSE-TRANSPORT.md`
- **Response:** `.deia/hive/responses/20260324-TASK-MCP-003-RESPONSE.md`
