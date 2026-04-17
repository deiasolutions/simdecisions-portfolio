# SPEC-MCP-WAVE-5-TELEMETRY-LOOP: Telemetry Dual-Loop

**Master Spec:** docs/specs/SPEC-MCP-REHABILITATION-001.md
**Status:** LOW PRIORITY
**Priority:** P2
**Depends On:** SPEC-MCP-WAVE-0-INTEGRATION-CLEANUP.md
**Model Assignment:** haiku

---

## ⚠️ LOW PRIORITY

**Wire when convenient per architect decision. Not blocking any other work.**

This wave implements the dual-loop telemetry architecture from FACTORY-006:
- Observer loop: heartbeats → Event Ledger
- Advisor loop: pattern detection → advisory responses

---

## Objective

Wire heartbeat tool to log events to the Event Ledger and implement advisory feedback (budget warnings, stall detection) via heartbeat acknowledgment responses.

---

## Governing Constraint

**MCP complements dispatch; it never blocks it.** If MCP is down, dispatch proceeds. MCP is observability and coordination bonus, not infrastructure dependency.

---

## Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| MCP-040 | Observer loop: heartbeats → Event Ledger | Existing `heartbeat` calls `telemetry_logger.log_build_attempt()` |
| MCP-041 | Advisor loop: pattern detection | Budget warnings, stall detection |
| MCP-042 | Advisory responses via heartbeat ack | `{ack: true, advisory?: {type, message}}` |
| MCP-043 | Advisories are non-blocking | Bee decides whether to heed |

---

## Architecture — Dual-Loop Telemetry

```
┌────────────────────────────────────────────────────┐
│  BEE sends heartbeat                               │
│  {bee_id, task_id, status, model, cost_usd, ...}  │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│  MCP Server: heartbeat tool                        │
│                                                     │
│  Observer Loop:                                    │
│  - Log to Event Ledger (telemetry_logger)         │
│  - Append to StateManager                          │
│                                                     │
│  Advisor Loop:                                     │
│  - Check budget (session cost vs limit)            │
│  - Check stall (last heartbeat age)                │
│  - Generate advisory if threshold exceeded         │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│  Response to BEE                                   │
│  {ack: true, advisory?: {type, message}}           │
│                                                     │
│  Example advisories:                               │
│  - {type: "budget_warning", message: "80% used"}   │
│  - {type: "stall_warning", message: "no progress"} │
└────────────────────────────────────────────────────┘
```

---

## Observer Loop Implementation

Existing `heartbeat` tool should call:

```python
telemetry_logger.log_build_attempt(
    spec_id=task_id,
    model=model,
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    cost_usd=cost_usd,
    result="in_progress"  # or "complete", "failed"
)
```

This writes to Event Ledger at `.deia/hive/event-ledger.json`.

---

## Advisor Loop Implementation

Before returning heartbeat ack, check:

1. **Budget Warning:**
   - Read session cost from StateManager
   - Compare with `queue.yml` budget limit
   - If >80%, return advisory: `{type: "budget_warning", message: "Session cost at 85%, consider wrapping up"}`

2. **Stall Detection:**
   - Check last heartbeat timestamp for this bee
   - If >15 minutes since last heartbeat, return advisory: `{type: "stall_warning", message: "No progress for 15+ minutes"}`

Advisory structure:

```json
{
  "ack": true,
  "timestamp": "2026-04-12T14:30:00Z",
  "advisory": {
    "type": "budget_warning",
    "message": "Session cost at 85%, consider wrapping up"
  }
}
```

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `hivenode/hive_mcp/tools/heartbeat.py` | MODIFY | Wire to telemetry_logger, add advisor checks |
| `hivenode/telemetry/telemetry_logger.py` | VERIFY | Ensure `log_build_attempt()` exists |
| `tests/core/test_mcp_telemetry.py` | CREATE | Telemetry dual-loop tests |

---

## Acceptance Criteria

- [ ] AC-06: `heartbeat` updates monitor state (send heartbeat, verify via `/build/status`)
- [ ] AC-20: `heartbeat` logs to Event Ledger (verify event written to `.deia/hive/event-ledger.json`)
- [ ] AC-21: Budget warning advisory returned when session cost >80%
- [ ] AC-22: Stall warning advisory returned when >15 min since last heartbeat
- [ ] AC-23: Advisories are non-blocking (bee can ignore and continue)

---

## Smoke Test

- [ ] Send heartbeat with high cost: `{bee_id: "BEE-001", task_id: "TEST", cost_usd: 9.50}` (assuming $10 session limit)
- [ ] Verify response includes `advisory.type = "budget_warning"`
- [ ] Check `.deia/hive/event-ledger.json` for logged event

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
| 3 | Heartbeat interface | Update spec to match existing (bee_id, task_id, model, tokens/cost) |
| 7 | mcp_telemetry_log | Skip — FACTORY-006 sufficient |
| 11 | FACTORY-006 timing | Wire when convenient, not blocking |

---

## Response File Template

When complete, write: `.deia/hive/responses/YYYYMMDD-SPEC-MCP-WAVE-5-TELEMETRY-LOOP-RESPONSE.md`

Required sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (concrete changes)
4. **Tests Run** (commands + results)
5. **Acceptance Criteria Status** (check each AC)
6. **Blockers** (if any)
7. **Cost** (tokens, USD)
8. **Next Steps** (for Q33N/Q33NR)
