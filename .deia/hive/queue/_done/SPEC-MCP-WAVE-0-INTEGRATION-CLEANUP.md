# SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP: MCP Integration Cleanup

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** READY
**Priority:** P1
**Depends On:** None
**Model Assignment:** sonnet

---

## Objective

Wire existing MCP tools to the MCP surface, add health endpoints, and establish graceful degradation controls. This wave makes MCP discoverable and observable without changing any tool behavior.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-001 | MCP server starts as part of hivenode startup | Already implemented — `asyncio.create_task()` in main.py |
| MCP-002 | Add `/mcp/health` endpoint | Returns `{"status": "ok", "tools": [...], "uptime_s": N}` |
| MCP-003 | Keep existing `/health` as-is | Bare liveness check, no tool list |
| MCP-004 | `mcp_required: false` in `queue.yml` | Kill switch for graceful degradation |
| MCP-005 | Startup log includes MCP status | `[HIVENODE] MCP server available at localhost:8421` |
| MCP-006 | If port 8421 unavailable, log warning, proceed | No pre-check blocking |

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/hive_mcp/local_server.py` | MODIFY | Add `/mcp/health` endpoint (full: tools, uptime) |
| `.deia/config/queue.yml` | MODIFY | Add `mcp_required: false` |
| `hivenode/main.py` | VERIFY | Confirm MCP server starts via `asyncio.create_task()` |
| `tests/core/test_mcp_lifecycle.py` | CREATE | Lifecycle + health endpoint tests |

---

## Acceptance Criteria

- [ ] AC-01: MCP server starts with hivenode (`pytest tests/core/test_mcp_lifecycle.py`)
- [ ] AC-02: `/mcp/health` returns tool list + uptime (HTTP GET, verify JSON schema)
- [ ] AC-03: `/health` still returns bare liveness (HTTP GET, verify unchanged)
- [ ] AC-04: `queue.yml` contains `mcp_required: false`
- [ ] AC-05: Hivenode startup logs show MCP status (`[HIVENODE] MCP server available...` or warning)
- [ ] AC-06: If port 8421 is occupied, hivenode logs warning and continues without crash

---

## Smoke Test

- [ ] `curl -s http://localhost:8421/mcp/health | jq '.status'` returns `"ok"`
- [ ] `curl -s http://localhost:8420/health` returns `200 OK` (unchanged)

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
| 1 | Tool naming | Keep existing names, `mcp_*` for new only |
| 2 | .mcp.json vs prompt injection | Both — .mcp.json is primary, injection is fallback |
| 6 | Health endpoint | Add `/mcp/health` (full), keep `/health` (liveness) |
| 12 | Graceful degradation | `queue.yml` kill switch (`mcp_required: false`) |
| 15 | Port conflict | Log warning, proceed — no pre-check blocking |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)
