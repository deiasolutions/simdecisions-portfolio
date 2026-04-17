# SPEC-HIVENODE-RELIABILITY-001-LITE

**Status:** DRAFT  
**Author:** Q33NR (via Claude)  
**Date:** 2026-04-05  
**Type:** Lite spec — scoping and investigation, not full task breakdown

---

## 1. Problem Statement

Telemetry data is being lost because:

1. **Hivenode must be running** for heartbeats to land — if it's down, dispatch.py fails silently
2. **No reconciliation** — when hivenode was down, that data is gone (but Claude/Anthropic still has records)
3. **No uptime tracking** — we don't know how much data we're losing
4. **No redundancy** — single point of failure (Mac)

Additionally:
- Mobile needs to reach hivenode, which currently runs on localhost
- Direct Claude Code sessions may not be going through dispatch.py (needs audit)

---

## 2. Current State

| Component | Status |
|-----------|--------|
| Heartbeat pipeline | ✅ Works when hivenode is up |
| monitor-state.json | ✅ Captures real token counts from API |
| Event Ledger | ❌ Schema exists, never written to |
| Hivenode auto-start | ❌ Manual |
| Hivenode on VPS | ❓ Unknown if possible — needs investigation |
| Gap reconciliation | ❌ None |
| Uptime tracking | ❌ None |

**Known data:** $1,515.86 in monitor-state.json  
**Unknown:** How much was lost when hivenode was down

---

## 3. Required Investigations

### 3.1 Can hivenode run on a VPS?

**Ask Mr. Code:**

```
Can hivenode run on a Linux VPS today?

1. System dependencies — Python version, packages, native libs, macOS-specific?
2. Local assumptions — hardcoded paths? localhost assumptions? SQLite vs PostgreSQL?
3. What changes needed — config only? code changes? storage adapter changes?

grep:
- grep -r "localhost\|127.0.0.1" hivenode/ --include="*.py"
- grep -r "sqlite\|postgres\|database" hivenode/ --include="*.py"  
- grep -r "/Users\|/home\|expanduser" hivenode/ --include="*.py"
```

**Outcome:** Either "config change" or "requires project X"

### 3.2 Audit tonight's build

Compare:
- Tasks dispatched (from queue-runner logs)
- Heartbeats received (monitor-state.json)
- Anthropic dashboard usage

This tells us where data is dropping.

### 3.3 How does mobile reach hivenode?

Current state unknown. Options if not working:
- Tailscale/ngrok tunnel to Mac
- Hivenode on VPS (if possible)
- Cloudflare tunnel

---

## 4. Proposed Fixes

### 4.1 Heartbeat → Event Ledger (~50 lines)

**Priority:** HIGH — blocks research track

Wire `build_monitor.py` to call `LedgerWriter.write_event()` on each heartbeat. Real data becomes queryable.

```python
# In build_monitor.py handle_heartbeat():
from hivenode.ledger import LedgerWriter

LedgerWriter.write_event(
    event_type="llm_call",
    task_id=data["task_id"],
    model_id=data["model"],
    tokens_in=data["input_tokens"],
    tokens_out=data["output_tokens"],
    cache_read=data.get("cache_read_tokens", 0),
    cache_write=data.get("cache_creation_tokens", 0),
    cost_usd=data["cost_usd"],
    carbon_g=compute_carbon(data),
    clock_ms=data.get("latency_ms", 0),
)
```

### 4.2 Hivenode auto-start (launchd)

Create `~/Library/LaunchAgents/com.deia.hivenode.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.deia.hivenode</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/hivenode/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/hivenode.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/hivenode.err</string>
</dict>
</plist>
```

### 4.3 Uptime tracking

Hivenode emits heartbeat to itself every 60s. Log gaps. Dashboard shows:
- Current status (up/down)
- Uptime percentage (24h, 7d, 30d)
- Gap periods (when it was down)

### 4.4 Gap reconciliation from Claude records

When hivenode was down, we lost heartbeat data. But Anthropic has records.

**Manual process (for now):**
1. Export usage from Anthropic console for date range
2. Compare to monitor-state.json
3. Identify gaps
4. Backfill Event Ledger with missing data

**Future:** API integration with Anthropic usage endpoint (if available)

### 4.5 VPS as backup (pending investigation)

If hivenode can run on VPS:
- Primary: VPS (always reachable from mobile)
- Backup: Mac (local, fast)
- Failover: automatic based on health check

If not possible without code changes, scope the work.

---

## 5. Prioritization

| Fix | Blocks | Effort | Priority |
|-----|--------|--------|----------|
| Heartbeat → Ledger | Research track | ~50 lines | **P0** |
| Audit tonight's build | Understanding | 1h manual | **P0** |
| Hivenode auto-start | Daily reliability | 30min | P1 |
| VPS investigation | Mobile, redundancy | 1h research | P1 |
| Uptime tracking | Visibility | 2-4h | P2 |
| Gap reconciliation | Data completeness | 4-8h | P2 |

---

## 6. Out of Scope for This Spec

- Mobile workdesk primitives (see SPEC-MOBILE-WORKDESK-001)
- Scheduler/backlog/staging pipeline (see SPEC-MOBILE-WORKDESK-001)
- Queue-runner changes (already works)

---

## 7. Next Steps

1. Run tonight's build through queue
2. Tomorrow: audit dispatch logs vs monitor-state.json vs Anthropic dashboard
3. Ask Mr. Code about VPS feasibility
4. Write TASK for heartbeat → ledger wiring (P0)
5. Set up launchd plist for hivenode

---

*End of SPEC-HIVENODE-RELIABILITY-001-LITE*
