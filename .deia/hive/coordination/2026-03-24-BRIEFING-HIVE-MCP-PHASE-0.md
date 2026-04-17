# BRIEFING: Hive MCP Intercom Layer — Phase 0 Foundation

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Objective

Build Phase 0 of SPEC-HIVE-MCP-001-v2. The spec is checked into the repo at the path below. READ THE FULL SPEC FIRST — every design decision is already made.

**Spec file:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

If you cannot read from Downloads, the key decisions are summarized in section 14 of the spec. The critical points for Phase 0:

## Phase 0 Scope (from spec section 10)

1. Scaffold `hivenode/hive_mcp/` package
2. Implement in-memory state manager (`state.py`) with JSON persistence to `~/.shiftcenter/hive_state/`
3. Implement read-only tools: `queue_list`, `task_list`, `task_read`
4. Wire SSE transport on localhost:8421
5. Create `.mcp.json` in repo root
6. Test: a bee can read its assigned task via MCP instead of file searching

## Explicitly OUT OF SCOPE for Phase 0

- `task_claim` (future worker-pool pattern)
- `heartbeat` (bee-initiated — dispatch.py continues its own)
- Mid-task redirect
- Cloud server
- All write tools (briefing_write, task_write, response_submit, etc.) — those are Phase 1

## Architecture Decisions (all final — do not deviate)

1. **Package location:** `hivenode/hive_mcp/` — extension of hivenode, same FastAPI stack
2. **Transport:** SSE only (NOT stdio). Single server process, multiple concurrent clients. Port 8421.
3. **State storage:** In-memory Python dicts + JSON backup to `~/.shiftcenter/hive_state/` (outside OneDrive sync). NO SQLite for hive state (OneDrive file sync conflicts).
4. **MCP SDK:** Use the `mcp` Python package for MCP protocol compliance
5. **File structure:**
   ```
   hivenode/
     hive_mcp/
       __init__.py
       local_server.py    # Local MCP server entry point + SSE transport
       state.py           # In-memory state manager + JSON persistence
       tools/
         __init__.py
         queue.py          # queue_list, queue_peek
         tasks.py          # task_list, task_read
   ```

## How to Dispatch

Break Phase 0 into bee-sized tasks. Suggested split:

- **Task A:** Scaffold `hivenode/hive_mcp/` package, implement `state.py` (in-memory state + JSON persistence), write tests
- **Task B:** Implement `queue_list`, `queue_peek`, `task_list`, `task_read` tools, write tests
- **Task C:** Wire SSE transport on localhost:8421 via `local_server.py`, create `.mcp.json`, write integration test showing a client can connect and call tools

Tasks A and B can be parallel. Task C depends on A and B.

Use Sonnet bees. Use `--inject-boot`.

## Key Files to Reference

- Spec: `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`
- Existing hivenode structure: `hivenode/` (look at how routes are organized)
- Existing dispatch: `.deia/hive/scripts/dispatch/dispatch.py`
- Queue directory: `.deia/hive/queue/`
- Tasks directory: `.deia/hive/tasks/`
- MCP Python SDK docs: https://pypi.org/project/mcp/ (bee should check current API)

## Constraints

- All code must have tests (TDD)
- 500-line file limit
- CSS variables only (if any CSS needed — unlikely for backend)
- No stubs — every function complete
- Python 3.13, FastAPI
