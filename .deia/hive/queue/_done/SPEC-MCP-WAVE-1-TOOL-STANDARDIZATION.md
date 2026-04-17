# SPEC-MCP-WAVE-1-TOOL-STANDARDIZATION: Tool Interface Standardization

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** READY
**Priority:** P1
**Depends On:** SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP.md
**Model Assignment:** sonnet

---

## Objective

Add `mcp_queue_state` (grouped queue view) and verify that all existing Phase 0 tools match their documented interfaces. This wave completes the read-only tool surface.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements — Phase 0 Tools (Existing)

Verify these tools are wired correctly and match documented interfaces:

| Tool | Status | Parameters | Returns |
|------|--------|------------|---------|
| `heartbeat` | EXISTS | `{bee_id, task_id, status, model, input_tokens, output_tokens, cost_usd, message?}` | `{ack: true, timestamp, advisory?: {type, message}}` |
| `queue_list` | EXISTS | `{status?: string}` | Flat list of specs with file_name, status, area_code, priority, created |
| `briefing_read` | EXISTS | `{name: string}` | `{content: string, modified: timestamp}` |
| `response_submit` | EXISTS | `{spec_id, content, is_final: bool}` | `{received: bool, path?: string}` |

---

## Requirements — Phase 0 Tools (New)

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `mcp_queue_state` | Grouped queue view | `{include_done?: bool}` | `{active: [...], pending: [...], done?: [...]}` |

**Implementation Note:** `mcp_queue_state` reads from `.deia/hive/queue/` subdirectories:
- `active`: specs in `_active/`
- `pending`: specs in root or `backlog/`
- `done`: specs in `_done/` (only if `include_done=true`)

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/hive_mcp/tools/queue_state.py` | CREATE | `mcp_queue_state` (grouped view) |
| `hivenode/hive_mcp/tools/heartbeat.py` | VERIFY | Ensure interface matches spec |
| `hivenode/hive_mcp/tools/queue_list.py` | VERIFY | Ensure interface matches spec |
| `hivenode/hive_mcp/tools/briefing_read.py` | VERIFY | Ensure interface matches spec |
| `hivenode/hive_mcp/tools/response_submit.py` | VERIFY | Ensure interface matches spec |
| `tests/core/test_mcp_tools.py` | CREATE | Tool integration tests (Phase 0) |

---

## Acceptance Criteria

- [ ] AC-07: `mcp_queue_state` returns grouped queue (compare with file-based queue scan)
- [ ] AC-08: `heartbeat` tool matches documented interface (parameters + return structure)
- [ ] AC-09: `queue_list` tool matches documented interface
- [ ] AC-10: `briefing_read` tool matches documented interface
- [ ] AC-11: `response_submit` tool matches documented interface
- [ ] AC-12: All Phase 0 tools have integration tests (`pytest tests/core/test_mcp_tools.py`)

---

## Smoke Test

- [ ] `curl -X POST http://localhost:8421/mcp/rpc -d '{"tool":"mcp_queue_state","params":{"include_done":false}}' | jq '.active | length'` returns spec count in `_active/`

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
| 3 | Heartbeat interface | Update spec to match existing (bee_id, task_id, model, tokens/cost) |
| 4 | Phase 0/1 sequencing | Phase 0 = wire existing, Phase 1 = add missing |
| 5 | queue_state format | Keep `queue_list` (flat), add `mcp_queue_state` (grouped) |
| 10 | Wave naming | Wave 0 = Integration Cleanup, Wave 1 = Tool Interface Standardization |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-1-TOOL-STANDARDIZATION-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)
