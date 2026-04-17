# SPEC-MCP-REHABILITATION-001: Real-Time Bee Management via MCP

**Status:** APPROVED
**Author:** Q88N
**Date:** 2026-04-07
**Updated:** 2026-04-12 (architect decisions incorporated)
**Priority:** P1
**Depends On:** FACTORY-006 (Telemetry Policy Split)
**Blocks:** Real-time build monitoring, live bee coordination

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** Every requirement below follows
from this. If MCP is down, dispatch proceeds. MCP is observability and coordination
bonus, not infrastructure dependency.

---

## 1. Problem Statement

The MCP server exists at `hivenode/hive_mcp/` (port 8421), but it operates as a
disconnected sidecar. The factory loop (`run_queue.py`) communicates via:

1. HTTP to hivenode (heartbeats, status, wake) — `/build/*` routes on port 8420
2. Subprocess to `dispatch.py` → Claude Code CLI — fire-and-forget

Bees run blind. Once dispatched, they have no real-time channel for:
- Mid-flight status queries (what else is running?)
- Heartbeat submission (faster than file writes)
- Coordination document reads (get latest briefing)
- Advisory policy queries (should I continue or yield?)

The MCP server has tools built (`queue_list`, `dispatch_bee`, `coordination`,
`telemetry`) that bees could use, but:
- `dispatch.py` doesn't inject MCP configuration into the bee's working directory
- The queue runner doesn't verify MCP health before dispatch
- No graceful degradation — if MCP is down, nothing changes (because nothing uses it)

---

## 2. Design Principles

### 2.1 File Protocol Remains Canonical

The file-based task/response protocol is not replaced:
- Tasks: `.deia/hive/tasks/*.md`
- Responses: `.deia/hive/responses/*.md`
- Queue state: `.deia/hive/queue/*.md`

MCP is a **real-time sideband**, not a replacement. Bees use it for ephemeral
coordination; durable state flows through files.

### 2.2 Graceful Degradation

If MCP is unavailable:
- Dispatch proceeds with file-based flow
- Queue runner logs warning, continues
- No crash, no block, no retry loop

Controlled via `queue.yml`: `mcp_required: false` (default).

### 2.3 Localhost Only (Phase 1)

No authentication in Phase 1. MCP server binds to `localhost:8421`. Remote MCP
federation is out of scope.

### 2.4 Dual-Loop Telemetry (per FACTORY-006)

- **Observer loop:** MCP receives heartbeats, logs to Event Ledger
- **Advisor loop:** Policy recommender surfaces warnings (budget, stall)
- Advisory responses are non-blocking — bee decides whether to heed

Wire heartbeats → Event Ledger when convenient. Not a blocking dependency.

### 2.5 Tool Naming Convention

- **Existing tools keep their names.** Do not rename `heartbeat`, `queue_list`,
  `briefing_read`, `response_submit`, etc.
- **New tools get `mcp_*` prefix.** Only tools that don't exist yet (e.g.,
  `mcp_queue_state`, `mcp_claim_task`) use the prefix.

### 2.6 State Volatility

StateManager is in-memory with JSON backup. Heartbeats are ephemeral pings —
losing them on crash is acceptable. Event Ledger captures durable records on
task completion. Do not over-engineer transient state.

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           HIVENODE (8420)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ /build/*     │  │ /api/*       │  │ MCP SERVER (8421)        │  │
│  │ (HTTP)       │  │ (REST)       │  │ (SSE + JSON-RPC)         │  │
│  │              │  │              │  │                          │  │
│  │ - heartbeat  │  │ - storage    │  │ Existing tools:          │  │
│  │ - status     │  │ - llm        │  │ - heartbeat              │  │
│  │ - wake       │  │ - ...        │  │ - queue_list             │  │
│  │ - ping       │  │              │  │ - briefing_read          │  │
│  └──────────────┘  └──────────────┘  │ - response_submit        │  │
│                                      │                          │  │
│                                      │ New tools:               │  │
│                                      │ - mcp_queue_state        │  │
│                                      │ - mcp_claim_task (P1)    │  │
│                                      │ - mcp_release_task (P1)  │  │
│                                      │ - mcp_submit_response(P1)│  │
│                                      │                          │  │
│                                      │ Endpoints:               │  │
│                                      │ - /health (liveness)     │  │
│                                      │ - /mcp/health (full)     │  │
│                                      └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
         ▲                                        ▲
         │ HTTP                                   │ SSE/JSON-RPC
         │                                        │
┌────────┴────────┐                    ┌──────────┴──────────┐
│  QUEUE RUNNER   │                    │     BEE (Claude)    │
│  run_queue.py   │                    │  via .mcp.json      │
│                 │                    │                     │
│ - checks /mcp/ │                    │ - heartbeat         │
│   health        │                    │ - query queue       │
│ - dispatches    │                    │ - read coordination │
│   via dispatch. │                    │                     │
│   py            │                    │ (All optional —     │
│                 │                    │  file-based is the  │
│ - mcp_required: │                    │  floor, MCP is      │
│   false default │                    │  bonus)             │
└─────────────────┘                    └─────────────────────┘
         │
         │ subprocess
         ▼
┌─────────────────┐
│   dispatch.py   │
│                 │
│ - creates temp  │
│   dir per bee   │
│ - writes .mcp.  │
│   json there    │
│ - injects MCP   │
│   prompt block  │
│ - spawns Claude │
│   Code CLI      │
└─────────────────┘
```

---

## 4. Changes Required

### 4.1 MCP Server Lifecycle

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-001 | MCP server starts as part of hivenode startup | Already implemented — `asyncio.create_task()` in main.py |
| MCP-002 | Add `/mcp/health` endpoint | Returns `{"status": "ok", "tools": [...], "uptime_s": N}` |
| MCP-003 | Keep existing `/health` as-is | Bare liveness check, no tool list |
| MCP-004 | `mcp_required: false` in `queue.yml` | Kill switch for graceful degradation |
| MCP-005 | Startup log includes MCP status | `[HIVENODE] MCP server available at localhost:8421` |
| MCP-006 | If port 8421 unavailable, log warning, proceed | No pre-check blocking |

### 4.2 Dispatch Integration

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-010 | `dispatch.py` creates temp dir per bee | `.deia/hive/temp/{bee_id}/` — isolated, disposable |
| MCP-011 | Writes `.mcp.json` in temp dir | Points to `http://localhost:8421/mcp/sse` |
| MCP-012 | Bee prompt includes MCP availability notice | Prompt injection as fallback (see section 6) |
| MCP-013 | Queue runner checks `/mcp/health` before dispatch | Logs status. Non-blocking. |
| MCP-014 | Dispatch proceeds if MCP down | Warning only, not blocking |

### 4.3 Tool Surface — Phase 0 (Wire Existing Tools)

Existing tools already work. Phase 0 wires them to the MCP surface and ensures
dispatch makes them discoverable.

| Tool | Status | Parameters | Returns |
|------|--------|------------|---------|
| `heartbeat` | EXISTS | `{bee_id, task_id, status, model, input_tokens, output_tokens, cost_usd, message?}` | `{ack: true, timestamp, advisory?: {type, message}}` |
| `queue_list` | EXISTS | `{status?: string}` | Flat list of specs with file_name, status, area_code, priority, created |
| `briefing_read` | EXISTS | `{name: string}` | `{content: string, modified: timestamp}` |
| `response_submit` | EXISTS | `{spec_id, content, is_final: bool}` | `{received: bool, path?: string}` |

### 4.4 Tool Surface — Phase 0 (New Read-Only Tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `mcp_queue_state` | Grouped queue view | `{include_done?: bool}` | `{active: [...], pending: [...], done?: [...]}` |

### 4.5 Tool Surface — Phase 1 (New Write Tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `mcp_claim_task` | Claim spec (prevent double-dispatch) | `{spec_id, bee_id}` | `{claimed: bool, owner?: bee_id}` |
| `mcp_release_task` | Release claim | `{spec_id, reason: "done" \| "failed" \| "timeout"}` | `{released: bool}` |
| `mcp_submit_response` | Submit partial/final response | `{spec_id, content, is_final: bool}` | `{received: bool, path?: string}` |

**Claim/release implementation:** File-based. `mcp_claim_task` moves spec to
`_active/` directory. `mcp_release_task` moves it back or to `_done/`. This
aligns with existing queue runner, survives crashes. StateManager mirrors for
fast lookup but file is source of truth.

### 4.6 Telemetry Dual-Loop (per FACTORY-006)

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-040 | Observer loop: heartbeats → Event Ledger | Existing `heartbeat` calls `telemetry_logger.log_build_attempt()` |
| MCP-041 | Advisor loop: pattern detection | Budget warnings, stall detection |
| MCP-042 | Advisory responses via heartbeat ack | `{ack: true, advisory?: {type, message}}` |
| MCP-043 | Advisories are non-blocking | Bee decides whether to heed |

Wire when convenient. Not a blocking wave.

### 4.7 Sync Queue Bridge (Conditional)

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-030 | MCP server reads `~/.shiftcenter/sync_queue/` | Existing `sync.py` write path |
| MCP-031 | Aggregates sync events into `/mcp/events` SSE | Frontend can subscribe |
| MCP-032 | Event format matches Event Ledger schema | `{event_type, timestamp, payload}` |

**Conditional:** Verify that sync queue flush already happens on hivenode startup
(`main.py:157-161`). If confirmed, this section is redundant and dropped.

---

## 5. .mcp.json Specification

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

Claude Code CLI reads this automatically when present. Prompt injection remains
the fallback path for bees that don't auto-discover.

---

## 6. Bee Prompt Injection

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

## 7. Queue Runner Integration

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

## 8. Acceptance Criteria

| # | Criterion | Test |
|---|-----------|------|
| AC-01 | MCP server starts with hivenode | `pytest tests/hivenode/test_mcp_lifecycle.py` |
| AC-02 | `/mcp/health` returns tool list + uptime | HTTP GET, verify JSON schema |
| AC-03 | `/health` still returns bare liveness | HTTP GET, verify unchanged |
| AC-04 | `dispatch.py` creates `.mcp.json` in temp dir | Check file exists in `.deia/hive/temp/{bee_id}/` |
| AC-05 | Bee prompt includes MCP notice | Grep dispatch output for "MCP Tools" |
| AC-06 | `heartbeat` updates monitor state | Send heartbeat, verify via `/build/status` |
| AC-07 | `mcp_queue_state` returns grouped queue | Compare with file-based queue scan |
| AC-08 | Queue runner logs MCP status | Verify `[MCP] available` or `[MCP] unavailable` in logs |
| AC-09 | Dispatch proceeds if MCP down | Kill MCP, dispatch succeeds, warning logged |
| AC-10 | `mcp_claim_task` moves spec to `_active/` | File check after claim |
| AC-11 | `mcp_release_task` moves spec out of `_active/` | File check after release |

**Minimum test count:** 11 (one per AC)

---

## 9. Out of Scope

| Item | Reason |
|------|--------|
| Replacing file-based task/response protocol | MCP is sideband, not replacement |
| Multi-node MCP federation | Phase 2+ |
| MCP authentication | Localhost only for Phase 1 |
| DAG coordination via MCP | Remains OR-Tools scheduler domain |
| MCP tool invocation from frontend | Frontend uses REST/SSE to hivenode |
| Per-tool-invocation telemetry logging | FACTORY-006 telemetry sufficient |
| Renaming existing MCP tools | Keep existing names as-is |

---

## 10. File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/hive_mcp/local_server.py` | MODIFY | Add `/mcp/health` endpoint (full: tools, uptime) |
| `hivenode/hive_mcp/tools/queue_state.py` | CREATE | `mcp_queue_state` (grouped view) |
| `hivenode/hive_mcp/tools/claim.py` | CREATE | `mcp_claim_task`, `mcp_release_task` (file-based) |
| `.deia/hive/scripts/dispatch/dispatch.py` | MODIFY | Create temp dir, write `.mcp.json`, inject prompt |
| `.deia/hive/scripts/queue/run_queue.py` | MODIFY | Add MCP health check (non-blocking) |
| `.deia/hive/queue.yml` | MODIFY | Add `mcp_required: false` |
| `tests/hivenode/test_mcp_lifecycle.py` | CREATE | Lifecycle + health endpoint tests |
| `tests/hivenode/test_mcp_tools.py` | CREATE | Tool integration tests |
| `tests/hivenode/test_mcp_dispatch.py` | CREATE | Dispatch integration (temp dir, .mcp.json) |

---

## 11. Implementation Order

1. **Wave 0 — Integration Cleanup:** Wire existing tools to MCP surface, add `/mcp/health`, add `mcp_required` config (MCP-001 through MCP-006)
2. **Wave 1 — Tool Interface Standardization:** Add `mcp_queue_state` (grouped view). Ensure existing tools match documented interfaces. (Phase 0 tools)
3. **Wave 2 — Dispatch Integration:** Temp dir creation, `.mcp.json` writing, prompt injection, queue runner health check (MCP-010 through MCP-014)
4. **Wave 3 — Write Tools:** `mcp_claim_task`, `mcp_release_task`, `mcp_submit_response` (Phase 1 tools, file-based claim)
5. **Wave 4 — Sync Queue Bridge (conditional):** Verify if already handled by hivenode startup flush. If redundant, drop. (MCP-030 through MCP-032)
6. **Wave 5 — Telemetry Dual-Loop (wire when convenient):** Heartbeats → Event Ledger, advisory ack (MCP-040 through MCP-043)

---

## 12. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Heartbeat latency | < 100ms | MCP heartbeat vs. file write time |
| Dispatch overhead | < 500ms | Time to create temp dir + `.mcp.json` + verify health |
| Graceful degradation | 100% | Dispatch success rate when MCP down |
| Tool adoption | Observable | Count of heartbeat calls in Event Ledger |

---

## 13. Decisions Record

Architect responses (2026-04-12, Mr. AI via Q88N):

| # | Question | Decision |
|---|----------|----------|
| 1 | Tool naming | Keep existing names, `mcp_*` for new only |
| 2 | .mcp.json vs prompt injection | Both — .mcp.json is primary, injection is fallback |
| 3 | Heartbeat interface | Update spec to match existing (bee_id, task_id, model, tokens/cost) |
| 4 | Phase 0/1 sequencing | Phase 0 = wire existing, Phase 1 = add missing |
| 5 | queue_state format | Keep `queue_list` (flat), add `mcp_queue_state` (grouped) |
| 6 | Health endpoint | Add `/mcp/health` (full), keep `/health` (liveness) |
| 7 | mcp_telemetry_log | Skip — FACTORY-006 sufficient |
| 8 | Claim/release | File-based (`_active/` directory), StateManager mirrors |
| 9 | Working directory | `.deia/hive/temp/{bee_id}/` — isolated, disposable |
| 10 | Wave naming | Wave 0 = Integration Cleanup, Wave 1 = Tool Interface Standardization |
| 11 | FACTORY-006 timing | Wire when convenient, not blocking |
| 12 | Graceful degradation | `queue.yml` kill switch (`mcp_required: false`) |
| 13 | Sync queue flush | Verify if redundant, drop Wave 4 if so |
| 14 | StateManager persistence | Accept volatile — heartbeats are ephemeral |
| 15 | Port conflict | Log warning, proceed — no pre-check blocking |

---

## 14. References

- FACTORY-006: Telemetry Policy Split (dual-loop architecture)
- `.deia/hive/scripts/queue/run_queue.py`: Current queue runner
- `.deia/hive/scripts/dispatch/dispatch.py`: Current dispatcher
- `hivenode/hive_mcp/`: Existing MCP server
- `~/.shiftcenter/sync_queue/`: Sync queue write path
- Q33N Review: `.deia/hive/responses/20260407-MCP-REHAB-REVIEW-RESPONSE.md`
