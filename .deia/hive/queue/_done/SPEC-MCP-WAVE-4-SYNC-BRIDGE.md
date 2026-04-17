# SPEC-MCP-WAVE-4-SYNC-BRIDGE: Sync Queue Bridge

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** CONDITIONAL
**Priority:** P2
**Depends On:** SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP.md
**Model Assignment:** sonnet

---

## ⚠️ CONDITIONAL IMPLEMENTATION

**Before building, verify that sync queue flush already happens on hivenode startup (`main.py:157-161`).**

If sync queue flush is confirmed to already exist on startup:
1. Write a response explaining the finding
2. Move this spec to `.deia/hive/queue/_done/` without implementation
3. Mark status as REDUNDANT

If sync queue flush does NOT exist on startup:
1. Proceed with implementation as described below

---

## Objective

Bridge the sync queue (`~/.shiftcenter/sync_queue/`) to MCP by reading sync events and exposing them via `/mcp/events` SSE endpoint. This allows frontend or bees to subscribe to real-time sync events.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-030 | MCP server reads `~/.shiftcenter/sync_queue/` | Existing `sync.py` write path |
| MCP-031 | Aggregates sync events into `/mcp/events` SSE | Frontend can subscribe |
| MCP-032 | Event format matches Event Ledger schema | `{event_type, timestamp, payload}` |

---

## Architecture

```
┌──────────────────────────────────────────────┐
│  Sync Process (writes to sync_queue/)       │
│  ~/.shiftcenter/sync_queue/*.json           │
└──────────────────┬───────────────────────────┘
                   │
                   ▼ (file watch or poll)
┌──────────────────────────────────────────────┐
│  MCP Server (reads sync_queue/)             │
│  /mcp/events (SSE endpoint)                 │
└──────────────────┬───────────────────────────┘
                   │
                   ▼ (SSE stream)
┌──────────────────────────────────────────────┐
│  Frontend / Bees (subscribe to events)      │
└──────────────────────────────────────────────┘
```

---

## Event Format

Match Event Ledger schema:

```json
{
  "event_type": "SYNC_COMPLETED",
  "timestamp": "2026-04-12T14:30:00Z",
  "payload": {
    "source": "wiki",
    "entries_synced": 42,
    "duration_ms": 123
  }
}
```

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/main.py` | VERIFY | Check if sync queue flush exists (lines ~157-161) |
| `hivenode/hive_mcp/sync_watcher.py` | CREATE (conditional) | Watch `~/.shiftcenter/sync_queue/` for new events |
| `hivenode/hive_mcp/local_server.py` | MODIFY (conditional) | Add `/mcp/events` SSE endpoint |
| `tests/core/test_mcp_sync_bridge.py` | CREATE (conditional) | Sync queue event tests |

---

## Acceptance Criteria

- [ ] AC-19: Verify sync queue flush on startup (read `main.py:157-161`)
- [ ] **If redundant:** Write response explaining finding, move to `_done/`
- [ ] **If not redundant:** MCP server reads sync queue directory
- [ ] **If not redundant:** `/mcp/events` SSE endpoint streams sync events
- [ ] **If not redundant:** Event format matches Event Ledger schema

---

## Smoke Test

**If redundant:** N/A

**If implemented:**
- [ ] Write a test event to `~/.shiftcenter/sync_queue/test-event.json`
- [ ] Subscribe to `curl -N http://localhost:8421/mcp/events`
- [ ] Verify event appears in SSE stream

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
| 13 | Sync queue flush | Verify if redundant, drop Wave 4 if so |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-4-SYNC-BRIDGE-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED | REDUNDANT (with explanation)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes OR verification results)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)
