# Briefing: MCP Dispatch & Telemetry Tools (Phase 1)

**Date:** 2026-03-25
**From:** Q33NR
**To:** Q33N
**Spec:** SPEC-MCP-DISPATCH-TELEMETRY
**Model Assignment:** sonnet
**Priority:** P0

---

## Objective

Implement MCP tools for dispatch_bee, heartbeat, status_report, cost_summary, and the sync queue writer. This is Phase 1 of SPEC-HIVE-MCP-001-v2.

---

## Context

The spec calls for:

1. **dispatch_bee** — wraps `.deia/hive/scripts/dispatch/dispatch.py` as a subprocess, returns PID
2. **heartbeat** — stores telemetry in state manager AND POSTs to `/build/heartbeat`
3. **status_report** — returns all active bees and tasks from state
4. **cost_summary** — returns aggregated costs
5. **Sync queue** — writes JSON files to `~/.shiftcenter/sync_queue/` (outside OneDrive) for future cloud sync

These tools enable:
- Q33N to dispatch bees via MCP (instead of subprocess calls)
- Bees to report heartbeat telemetry (opt-in, dispatch.py heartbeat continues as fallback)
- Q33NR to check bee status and costs via MCP
- Future cloud sync of queue state

---

## Files to Read First

### Existing MCP Infrastructure
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` — main MCP server, tool registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py` — state manager for bee tracking
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\__init__.py` — exports

### Tools to Implement
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\dispatch.py` — dispatch_bee tool (may be empty/stub)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\telemetry.py` — heartbeat, status_report, cost_summary tools (may be empty/stub)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\sync.py` — sync queue writer (may be empty/stub)

### Tests to Implement
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_dispatch.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_telemetry.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_sync.py`

### Related Infrastructure
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — the subprocess that dispatch_bee will call

---

## Requirements from Spec

### dispatch_bee
- Runs `dispatch.py` as subprocess (background, non-blocking)
- Returns PID
- Stores dispatch event in state manager

### heartbeat
- Stores data in state manager (bee_id, task_id, timestamp, cost, tokens, tests, message)
- POSTs to `/build/heartbeat` (hivenode endpoint)
- Returns confirmation

### status_report
- Returns all active bees and tasks from state manager
- Format: `{ "active": [...], "completed": [...] }`

### cost_summary
- Returns aggregated costs from state manager
- Format: `{ "total_cost_usd": X, "bees": [...] }`

### Sync Queue
- Writes JSON files to `~/.shiftcenter/sync_queue/` (Windows: `C:\Users\davee\.shiftcenter\sync_queue\`)
- One file per bee/task event
- Naming: `YYYYMMDD-HHMMSS-<bee_id>.json`
- Schema: `{ "bee_id": "...", "task_id": "...", "event": "...", "timestamp": "...", "data": {...} }`

---

## Test Requirements

Spec calls for **15+ tests passing**. Breakdown:

- `test_tools_dispatch.py`: 5+ tests (dispatch_bee returns PID, stores event, handles errors, path validation)
- `test_tools_telemetry.py`: 6+ tests (heartbeat stores + POSTs, status_report returns active/completed, cost_summary aggregates)
- `test_sync.py`: 4+ tests (writes JSON, creates dir, filename format, schema validation)

---

## Constraints

- TDD (tests first)
- 500-line limit per file
- Python 3.13
- dispatch_bee MUST NOT block (subprocess, background)
- Sync queue dir: `~/.shiftcenter/sync_queue/` (outside OneDrive to avoid sync conflicts)
- heartbeat wraps existing `/build/heartbeat` endpoint, does NOT replace dispatch.py heartbeat

---

## Acceptance Criteria (from spec)

- [ ] dispatch_bee runs dispatch.py as subprocess and returns PID
- [ ] heartbeat stores data in state manager and POSTs to /build/heartbeat
- [ ] status_report returns all active bees and tasks from state
- [ ] cost_summary returns aggregated costs
- [ ] Sync queue writes JSON files to ~/.shiftcenter/sync_queue/
- [ ] 15+ tests passing
- [ ] No stubs

---

## Smoke Test (from spec)

```bash
cd hivenode && python -m pytest hive_mcp/tests/test_tools_dispatch.py -v
cd hivenode && python -m pytest hive_mcp/tests/test_tools_telemetry.py -v
cd hivenode && python -m pytest hive_mcp/tests/test_sync.py -v
cd hivenode && python -m pytest hive_mcp/tests/ -v  # no regressions
```

---

## Dependencies

Spec says: "Depends On: SPEC-MCP-TRANSPORT-FIX"

Check queue status — if SPEC-MCP-TRANSPORT-FIX is complete, proceed. If not, wait or flag blocking dependency.

---

## Q33N Instructions

1. **Read the existing files first.** Understand the current state of `hive_mcp/` — what's already implemented, what's stub.
2. **Write task files** for bees to implement:
   - One task for dispatch_bee tool + tests
   - One task for telemetry tools (heartbeat, status_report, cost_summary) + tests
   - One task for sync queue writer + tests
   - OR: one combined task if the work is tightly coupled and small enough for one bee

3. **Task files must include:**
   - Absolute file paths for all files to modify
   - Test requirements (TDD, how many tests, which scenarios)
   - No hardcoded paths (use `os.path.expanduser('~/.shiftcenter/sync_queue/')` for sync queue dir)
   - Clear acceptance criteria matching the spec

4. **Return task files to Q33NR for review.** Do NOT dispatch bees yet. Wait for approval.

---

## Expected Deliverables from Q33N

- Task file(s) in `.deia/hive/tasks/` (absolute paths, test requirements, no stubs)
- Summary of task breakdown (how many bees, what each bee does)

---

## Notes

- This is Phase 1 of a larger MCP integration (SPEC-HIVE-MCP-001-v2)
- dispatch_bee enables Q33N to dispatch bees via MCP instead of Bash subprocess calls
- heartbeat is OPT-IN for bees — dispatch.py heartbeat continues as fallback
- Sync queue is future-proofing for cloud sync (not implemented yet, just the writer)

---

**Q33N: read, plan, write task files, return for review.**
