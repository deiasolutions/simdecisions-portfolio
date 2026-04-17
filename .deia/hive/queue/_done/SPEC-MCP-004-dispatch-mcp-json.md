---
id: MCP-004
priority: P0
model: sonnet
role: bee
depends_on: [MCP-001]
---
# SPEC-MCP-004: Dispatch Creates .mcp.json for Bees

## Priority
P0

## Model Assignment
sonnet

## Depends On
MCP-001

## Intent
Modify `dispatch.py` to create a temp directory per dispatch containing `.mcp.json` pointing to the MCP server. Pass `--mcp-config` flag to Claude Code CLI. Clean up temp dir on completion. Add MCP availability notice to bee prompt. Dispatch must proceed if MCP is unavailable.

## Files to Read First
- `.deia/hive/scripts/dispatch/dispatch.py` — current dispatch flow, find where CLI is spawned
- `hivenode/hive_mcp/local_server.py` — MCP server URL format
- `C:\Users\davee\Downloads\SPEC-MCP-REHABILITATION-001-v2.md` — sections 6, 7 for .mcp.json spec and prompt injection

## Acceptance Criteria
- [ ] `dispatch.py` creates `.deia/hive/temp/{dispatch_id}/` directory per dispatch
- [ ] dispatch_id format: `{YYYYMMDD}-{HHMM}-{role}-{model}-{spec_name}`
- [ ] `.mcp.json` written with `{"mcpServers": {"hive": {"url": "http://localhost:8421/mcp/sse", "transport": "sse"}}}`
- [ ] Claude Code CLI receives `--mcp-config` flag pointing to the `.mcp.json`
- [ ] Temp directory cleaned up after dispatch completes (success or failure)
- [ ] Bee prompt includes MCP availability notice (section 7 of rehab spec)
- [ ] If MCP health check fails, dispatch proceeds without `.mcp.json` (warning logged)
- [ ] Tests: temp dir creation, .mcp.json content, cleanup on success, cleanup on failure, dispatch without MCP

## Smoke Test
```bash
# Verify .mcp.json creation during dispatch (check temp dir exists mid-flight)
ls .deia/hive/temp/
```

## Constraints
- No file over 500 lines
- TDD: tests first
- Do NOT remove existing `_build_mcp_instructions()` — keep as fallback
- Temp dir MUST be cleaned up even on dispatch failure
- Dispatch MUST NOT fail if MCP is down
