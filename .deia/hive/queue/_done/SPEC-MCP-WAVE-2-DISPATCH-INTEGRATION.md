# SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION: Dispatch Integration

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** READY
**Priority:** P1
**Depends On:** SPEC-MCP-WAVE-1-TOOL-STANDARDIZATION.md
**Model Assignment:** sonnet

---

## Objective

Integrate MCP into the dispatch workflow: create isolated bee temp directories, write `.mcp.json` configuration, inject MCP availability notice into bee prompts, and add non-blocking MCP health checks to the queue runner.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-010 | `dispatch.py` creates temp dir per bee | `.deia/hive/temp/{bee_id}/` — isolated, disposable |
| MCP-011 | Writes `.mcp.json` in temp dir | Points to `http://localhost:8421/mcp/sse` |
| MCP-012 | Bee prompt includes MCP availability notice | Prompt injection as fallback (see section below) |
| MCP-013 | Queue runner checks `/mcp/health` before dispatch | Logs status. Non-blocking. |
| MCP-014 | Dispatch proceeds if MCP down | Warning only, not blocking |

---

## .mcp.json Specification

Created by `dispatch.py` in the bee's temp directory (`.deia/hive/temp/{bee_id}/`):

```json
{
  "mcpServers": {
    "hive": {
      "url": "http://localhost:8421/mcp/sse",
      "transport": "sse"
    }
  }
}
```

Claude Code CLI reads this automatically when present.

---

## Bee Prompt Injection

Added to dispatch prompt header (in addition to `.mcp.json`):

```
## MCP Tools (Optional)

Real-time coordination tools are available via MCP server at localhost:8421.
These are OPTIONAL — file-based protocol remains canonical.

Available tools:
- heartbeat: Send progress update (bee_id, task_id, status, model, tokens/cost)
- queue_list: Query queue contents (flat list)
- mcp_queue_state: Query queue grouped by state (active/pending/done)
- briefing_read: Fetch coordination document by name
- response_submit: Submit response via API

Use these for real-time coordination. Do not depend on them for critical state.
If MCP is unavailable, continue with file-based workflow.
```

---

## Queue Runner MCP Health Check

In `run_queue.py`, before processing queue:

```python
def _check_mcp_health() -> bool:
    """Check if MCP server is available. Non-blocking."""
    try:
        resp = requests.get("http://localhost:8421/mcp/health", timeout=2)
        if resp.ok:
            data = resp.json()
            tools = data.get("tools", [])
            print(f"[MCP] available, {len(tools)} tools", flush=True)
            return True
    except Exception:
        pass
    print("[MCP] unavailable, file-only mode", flush=True)
    return False
```

Called at:
1. Queue runner startup
2. Before each dispatch batch (optional, configurable via `queue.yml`)

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `.deia/hive/scripts/dispatch/dispatch.py` | MODIFY | Create temp dir, write `.mcp.json`, inject prompt |
| `.deia/hive/scripts/queue/run_queue.py` | MODIFY | Add MCP health check (non-blocking) |
| `tests/hive/test_mcp_dispatch.py` | CREATE | Dispatch integration (temp dir, .mcp.json) |

---

## Acceptance Criteria

- [ ] AC-04: `dispatch.py` creates `.mcp.json` in temp dir (check file exists in `.deia/hive/temp/{bee_id}/`)
- [ ] AC-05: Bee prompt includes MCP notice (grep dispatch output for "MCP Tools")
- [ ] AC-08: Queue runner logs MCP status (verify `[MCP] available` or `[MCP] unavailable` in logs)
- [ ] AC-09: Dispatch proceeds if MCP down (kill MCP, dispatch succeeds, warning logged)
- [ ] AC-13: Temp directory is isolated per bee (check `.deia/hive/temp/{bee_id}/` uniqueness)
- [ ] AC-14: `.mcp.json` points to correct endpoint (`http://localhost:8421/mcp/sse`)

---

## Smoke Test

- [ ] Run `python .deia/hive/scripts/dispatch/dispatch.py <test-task> --model sonnet --role bee`
- [ ] Verify `.deia/hive/temp/BEE-<task-id>/.mcp.json` exists
- [ ] Verify prompt output contains "MCP Tools (Optional)"

---

## Constraints

1. Do not rename existing MCP tools (existing names stay as-is)
2. New tools get `mcp_*` prefix only
3. File-based claim/release (not in-memory)
4. Bee temp dir: `.deia/hive/temp/{bee_id}/`
5. `queue.yml` kill switch: `mcp_required: false`

---

## Decisions Record (Reference)

Architect responses (2026-04-12, Mr. AI via Q88N):

| # | Question | Decision |
|---|----------|----------|
| 2 | .mcp.json vs prompt injection | Both — .mcp.json is primary, injection is fallback |
| 9 | Working directory | `.deia/hive/temp/{bee_id}/` — isolated, disposable |
| 12 | Graceful degradation | `queue.yml` kill switch (`mcp_required: false`) |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)
