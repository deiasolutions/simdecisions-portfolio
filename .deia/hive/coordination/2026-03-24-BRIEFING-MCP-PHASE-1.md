# BRIEFING: Hive MCP Phase 1 — Write Tools + Streamable HTTP Fix

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Context

Phase 0 is complete (58 tests, state manager, read-only tools, SSE transport). Two things need to happen now:

1. **Fix transport:** Phase 0 built SSE, but MCP has deprecated SSE in favor of Streamable HTTP. Update `local_server.py` to use Streamable HTTP transport instead of SSE. Update `.mcp.json` accordingly.

2. **Build Phase 1 write tools** from SPEC-HIVE-MCP-001-v2.

## Spec

**Read this first:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

Also read the Phase 0 code that already exists:
- `hivenode/hive_mcp/local_server.py` — current SSE server (needs transport fix)
- `hivenode/hive_mcp/state.py` — state manager
- `hivenode/hive_mcp/tools/queue.py` — existing read tools
- `hivenode/hive_mcp/tools/tasks.py` — existing read tools
- `.mcp.json` — current config (needs update for Streamable HTTP)

## Phase 1 Scope (from spec section 10)

1. Implement `briefing_write`, `briefing_read`, `briefing_ack`
2. Implement `task_write`, `response_submit` (with frontmatter validation + structured errors per spec section 8), `task_archive`
3. Implement `dispatch_bee` (wrapping existing `dispatch.py`)
4. Add MCP `heartbeat` as opt-in tool. dispatch.py's own heartbeat continues as fallback.
5. Wire sync queue writer for outbound state (claims, heartbeats, tool log → `~/.shiftcenter/sync_queue/`)

PLUS the transport fix:
6. Replace SSE transport with Streamable HTTP in `local_server.py`
7. Update `.mcp.json` to match new transport

## Task Breakdown (suggested)

**Task A — Transport Fix:** Update `local_server.py` from SSE to Streamable HTTP. Update `.mcp.json`. Update integration tests. This is independent and can run in parallel with others.

**Task B — Coordination Tools:** Implement `briefing_write`, `briefing_read`, `briefing_ack` in `hivenode/hive_mcp/tools/coordination.py`. Write tests.

**Task C — Write Tools + Validation:** Implement `task_write`, `response_submit` (with structured error handling per spec section 8), `task_archive` in `hivenode/hive_mcp/tools/tasks.py` (extend existing file) or new files if needed. Write tests. `response_submit` must validate frontmatter and return actionable errors (spec section 8.1).

**Task D — Dispatch + Telemetry:** Implement `dispatch_bee` (wraps `dispatch.py`) in `hivenode/hive_mcp/tools/dispatch.py`. Implement `heartbeat`, `status_report`, `cost_summary` in `hivenode/hive_mcp/tools/telemetry.py`. Implement sync queue writer in `hivenode/hive_mcp/sync.py`. Write tests.

**Parallelism:** Task A is independent. Tasks B, C, D all depend on Phase 0 code but are independent of each other — dispatch all three in parallel after A completes (A may change the server structure they need to register tools with).

Actually — Tasks B, C, D don't touch `local_server.py` directly (they just add tool modules). So all 4 can be parallel if you register the new tools in local_server.py as a final step. Use your judgment on sequencing.

## Key Constraints

- All code must have tests (TDD)
- 500-line file limit
- No stubs
- Python 3.13, FastAPI
- Sonnet bees, `--inject-boot`
- `response_submit` MUST return structured errors per spec section 8.1 format
- `dispatch_bee` wraps existing `dispatch.py` at `.deia/hive/scripts/dispatch/dispatch.py`
- Sync queue writes to `~/.shiftcenter/sync_queue/` (outside OneDrive)
- Validation error format must match spec section 8.1 exactly

## Error Handling (spec section 8)

`response_submit` must reject responses missing required frontmatter fields and return:
```json
{
  "error": "validation_failed",
  "tool": "response_submit",
  "violations": [
    {"field": "features_delivered", "issue": "missing", "fix": "Add features_delivered list to YAML frontmatter"}
  ],
  "retryable": true
}
```

3-retry limit before TASK_BLOCKED event.

## Dispatch and Report

Create task files, dispatch bees, report results. Do not wait for Q33NR approval between tasks — you have blanket approval to dispatch all Phase 1 tasks.
