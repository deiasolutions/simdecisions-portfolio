# SPEC-RESEARCH-TELEMETRY-SURVEY-001: Real-Time Telemetry & Factory Visibility Survey -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

## Files Modified
None (research only)

## What Was Done
- Surveyed entire codebase for real-time telemetry, monitoring, and observability infrastructure
- Cataloged all implemented endpoints, tools, and data streams
- Reviewed all completed and specced telemetry-related work
- Identified gaps and minimal paths to factory dashboard

---

## Section 1: What Exists Today (Implemented)

### Q1.1 — Status, Health, and Telemetry Endpoints

| Endpoint | Method | Path | Auth | Data Returned | Type |
|----------|--------|------|------|---------------|------|
| **Health** | GET | `/health` | None | status, mode, version, uptime_s | Polling |
| **Health (alt)** | GET | `/hivenode/health` | None | status, mode, version, uptime_s | Polling |
| **Status** | GET | `/status` | None | mode, version, node_id, volumes[], event_count, uptime_s | Polling |
| **Build Heartbeat** | POST | `/build/heartbeat` | None | Stores heartbeat, returns ack | Polling |
| **Build Status** | GET | `/build/status` | None | active[], completed[], failed[], total_cost, queue_total, queue_completed, log[] | Polling |
| **Build Stream** | GET | `/build/stream` | None | SSE stream of heartbeats (snapshot + heartbeat events) | **SSE Streaming** |
| **Build Ping** | POST | `/build/ping` | None | Lightweight liveness ping (no logging) | Polling |
| **Build Slot Status** | GET | `/build/slot-status` | None | reserved slots, capacity | Polling |
| **File Claims** | GET | `/build/claims` | None | active file claims, FIFO wait queues | Polling |
| **File Claim** | POST | `/build/claim` | None | Claim files for bee task | Polling |
| **File Release** | POST | `/build/release` | None | Release file claims | Polling |
| **Queue Wake** | POST | `/build/queue-wake` | None | Wake embedded queue runner | Polling |
| **Queue Runner Status** | GET | `/build/queue-runner-status` | None | running, embedded, queue_dir | Polling |
| **MCP Queue Notify** | POST | `/mcp/queue/notify` | None | Queue event notification (internal) | Polling |
| **MCP Queue Broadcast** | POST | `/mcp/queue/broadcast` | None | Broadcast queue event to subscribers | Polling |
| **MCP Queue Subscribe** | POST | `/mcp/queue/subscribe` | None | Register as queue event subscriber | Polling |
| **MCP Health** | GET | `/mcp/health` | None | status: "ok" | Polling |

**Files:**
- `hivenode/routes/health.py` (54 lines) — `/health`, `/status`
- `hivenode/routes/build_monitor.py` (1000+ lines) — All `/build/*` endpoints
- `hivenode/routes/queue_events.py` (221 lines) — All `/mcp/queue/*` endpoints
- `hivenode/hive_mcp/local_server.py` (800+ lines) — MCP server on port 8421

### Q1.2 — SSE (Server-Sent Events) and WebSocket Endpoints

**SSE Endpoints:**
- **`GET /build/stream`** (hivenode/routes/build_monitor.py:569-601)
  - Returns full state snapshot as `snapshot` event on connect
  - Streams `heartbeat` events for every build monitor heartbeat
  - Sends keepalive comments every 15s (`: keepalive {timestamp}`)
  - Media type: `text/event-stream`
  - Headers: `Cache-Control: no-cache`, `Connection: keep-alive`, `X-Accel-Buffering: no`
  - Subscriber model: In-memory queue per client
  - State: BuildState class with `_subscribers` list (asyncio.Queue per subscriber)

**WebSocket Endpoints:**
- **`WS /relay/ws`** (main.py:494-495, hivenode/relay/ws.py)
  - Efemera messaging relay (channel/DM real-time events)
  - NOT for factory telemetry (different domain)

**No SSE/WebSocket for:**
- Queue state changes (specs moving between folders)
- Scheduler output
- Dispatcher activity
- Event Ledger writes

### Q1.3 — Event Ledger

**Schema:** `hivenode/ledger/schema.py`
- SQLite database at `.deia/hive/event_ledger.db`
- Columns: id, timestamp, event_type, actor, target, domain, signal_type, oracle_tier, random_seed, completion_promise, verification_method, payload_json, cost_tokens, cost_tokens_up, cost_tokens_down, cost_usd, cost_carbon, currencies, context, previous_hash, merkle_root

**Write Frequency:**
- On-demand via `LedgerWriter.write_event()` (hivenode/ledger/writer.py)
- BUILD_ATTEMPT events logged by `telemetry_logger.log_build_attempt()` (.deia/hive/scripts/queue/telemetry_logger.py:13-109)
- NODE_ANNOUNCED events (remote mode only)
- LEDGER_NORMALIZATION events (auto-correction tracking)
- Heartbeat tool in MCP optionally logs BUILD_ATTEMPT events (hivenode/hive_mcp/tools/telemetry.py:98-143)

**Real-Time Query:**
- LedgerReader provides sync queries: `query()`, `query_by_event_type()`, `query_by_actor()`, `query_by_domain()`, `query_by_time_range()` (hivenode/ledger/reader.py)
- **No SSE/streaming endpoint** for ledger writes
- No tail/watch interface

**Triggers:**
- Build attempts (via telemetry_logger)
- Node announcements (remote mode startup + heartbeat)
- MCP heartbeat calls (best-effort, if cost data available)

### Q1.4 — monitor-state.json

**Path:** `.deia/hive/queue/monitor-state.json` (51:build_monitor.py)

**Contents:**
```json
{
  "tasks": {
    "TASK-ID": {
      "task_id": "...",
      "status": "...",
      "model": "...",
      "role": null,
      "first_seen": "...",
      "last_seen": "...",
      "last_heartbeat": "...",
      "cost_usd": 0.0,
      "tests_passed": null,
      "tests_total": null,
      "messages": [],
      "input_tokens": 0,
      "output_tokens": 0,
      "last_logged_message": null
    }
  },
  "log": [...],
  "total_cost": 0.0,
  "total_input_tokens": 0,
  "total_output_tokens": 0,
  "last_task_id": null,
  "slot_reservations": {}
}
```

**Who Writes It:**
- BuildState class in hivenode/routes/build_monitor.py (174-210)
- Written on every heartbeat via `_save_to_disk()` (195-210)
- Loaded on startup via `_load_from_disk()` (174-193)

**Who Reads It:**
- Build monitor on startup (restores state after restart)
- **Currently 16,099 lines** (JSON formatted, contains full history)

**Purpose:**
- Crash recovery (state persists across hivenode restarts)
- Historical record of all tasks/heartbeats
- Slot reservations tracking

### Q1.5 — MCP Server Tools for Factory/Queue Visibility

**MCP Server:** hivenode/hive_mcp/local_server.py (port 8421)

**Phase 0 Tools (Implemented):**
- `queue_list` — List specs in queue with filters (status, area_code, priority)
- `queue_peek` — Read specific spec file
- `queue_state` — Get queue grouped by status (active, pending, done)
- `task_list` — List task files with filters (assigned_bee, wave, status)
- `task_read` — Read task file with parsed YAML frontmatter
- `briefing_write` — Write coordination briefing
- `briefing_read` — Read coordination briefing (latest or by filename)
- `briefing_ack` — Acknowledge briefing receipt
- `task_write` — Write new task file
- `task_archive` — Archive completed task
- `response_submit` — Submit response file
- `response_read` — Read response file

**Telemetry Tools (hivenode/hive_mcp/tools/telemetry.py):**
- `heartbeat` — Send heartbeat to build monitor + log to Event Ledger (11-150)
- `status_report` — Get current build status report (153-194)
- `cost_summary` — Get aggregated costs (CLOCK/COIN/CARBON) (197-255)

**Dispatch Tools (hivenode/hive_mcp/tools/dispatch.py):**
- `dispatch_bee` — Dispatch bee to work on task

**SSE Stream (hivenode/hive_mcp/events_sse.py):**
- Sync queue SSE stream (not yet integrated into routes)

### Q1.6 — Log Files

**Log Files in Repo Root:**
1. `hivenode.log` — Hivenode main process logs
2. `scheduler.log` — Scheduler daemon logs
3. `dispatcher.log` — Dispatcher daemon logs
4. `queue_runner.log` — Queue runner logs
5. `triage_daemon.log` — Triage daemon logs
6. `vite.log` — Vite dev server logs
7. `mcp_server.log` — MCP server logs

**Format:** Plain text, Python logging module output (timestamp, logger name, level, message)

**Events Captured:**
- Spec processing (queue runner)
- Schedule computation (scheduler)
- Spec dispatch (dispatcher)
- Triage decisions (triage daemon)
- API requests/errors (hivenode)
- Build errors/warnings (vite)
- MCP tool calls (mcp_server)

**Real-Time Visibility:**
- Could be tailed via `tail -f *.log`
- No HTTP/SSE endpoint for log streaming
- Not aggregated or structured

### Q1.7 — Heartbeats Emitted by Queue Runner and Scheduler

**Queue Runner:**
- Sends heartbeats via `send_heartbeat()` (.deia/hive/scripts/queue/run_queue.py:142-174)
  - Target: `http://127.0.0.1:8420/build/heartbeat`
  - Payload: `{"task_id": "queue-runner", "status": "...", "model": "python", "role": "QR", "message": "...", "queue_items": [...], "cost_usd": ...}`
- Sends liveness pings via `send_liveness_ping()` (177-200)
  - Target: `http://127.0.0.1:8420/build/ping`
  - Payload: `{"task_id": "queue-runner", "timestamp": "..."}`
  - Frequency: Every 30s
- Heartbeats on state changes (spec started, completed, failed, etc.)

**Scheduler:**
- **No heartbeat emissions found** in scheduler_daemon.py
- Writes to `schedule.json` and `schedule_log.jsonl` (.deia/hive/)
- Reads dispatcher feedback from `dispatched.jsonl`
- Logs to `scheduler.log` (stderr)

**Dispatcher:**
- **No heartbeat emissions found** in dispatcher_daemon.py
- Writes to `dispatched.jsonl` and `dispatcher_log.jsonl`
- Reads schedule from `schedule.json`
- Logs to `dispatcher.log` (stderr)

### Q1.8 — Frontend Components with Real-Time Status

**Build Monitor Adapter:**
- File: `browser/src/apps/buildMonitorAdapter.tsx` (1-200+)
- Connects to **`/build/stream` SSE endpoint** (162)
- Listens for `snapshot` and `heartbeat` events (165-194)
- Displays live feed of dispatch heartbeats
- Auto-reconnects on disconnect (196-199)
- Caches status to survive HMR remounts
- Renders: active tasks, completed tasks, failed tasks, cost, tokens, log

**No Other Real-Time Consumers Found:**
- No queue state dashboard
- No scheduler/dispatcher monitoring
- No Event Ledger viewer
- Build monitor is the ONLY real-time frontend component

---

## Section 2: What's Been Specced But Not Built

### Q2.1 — Telemetry/Monitoring Specs

**Completed Specs (in `queue/_done/`):**
1. **SPEC-MCP-002-heartbeat-upgrade.md** (P0, sonnet)
   - Status: DONE (completed)
   - Added `progress` (0.0-1.0) and `spec_id` params to heartbeat tool
   - Wired heartbeats to Event Ledger via `telemetry_logger.log_build_attempt()`

2. **SPEC-FACTORY-006-telemetry-policy-split.md** (P0, sonnet)
   - Status: DONE (completed)
   - Built telemetry_logger module for Event Ledger logging
   - Observation-only pattern (no routing mutation)
   - Response: `.deia/hive/responses/20260407-QUEUE-TEMP-SPEC-FACTORY-006-RESPONSE.md`

3. **SPEC-MCP-007-sync-queue-bridge.md** (P0, sonnet)
   - Status: DONE (completed)
   - Embedded queue runner bridge in hivenode
   - Queue state sync via MCP events

**Rejected/Escalated Specs (in `queue/_escalated/`):**
1. **SPEC-MCP-005-telemetry-log-tool.rejection.md** (GATE0_FAIL)
   - Rejected 3 times (empty output)
   - Reason: Scope violation (tried to modify forbidden telemetry.py)
   - Escalated by triage daemon

**MCP-Related Specs (archived in `tasks/_archive/`):**
1. **TASK-MCP-003-SSE-TRANSPORT.md** (archived)
   - SSE transport for MCP (legacy, pre-Streamable HTTP)

2. **TASK-MCP-007-DISPATCH-TELEMETRY.md** (archived)
   - Dispatch telemetry (superseded by MCP-002)

**Build Monitor Specs:**
- Multiple archived tasks in `.deia/hive/tasks/_archive/` (2026-03-13-TASK-063 through TASK-067)
  - Build monitor backend tokens (063)
  - Build monitor frontend layout (064)
  - Build monitor frontend tokens (065)
  - Build monitor frontend timers (066)
  - Build monitor integration tests (067)
- All COMPLETE (shipped)

**Dashboard/Metrics Specs:**
- **SPEC-METRICS-001** and **SPEC-METRICS-002** (responses found in `.deia/hive/responses/`)
  - Context: Pipeline metrics (not factory metrics)
- **SPEC-WAVE0-C** (response found)
  - Context: Unknown (need to read spec)
- **QUEUE-TEMP-SPEC-BMON-01-pipeline-dashboard** (response found)
  - Build monitor pipeline dashboard (shipped)

### Q2.2 — MCP Specs Related to Telemetry

**Completed:**
- SPEC-MCP-001 (health endpoint)
- SPEC-MCP-002 (heartbeat upgrade) — **Telemetry integration**
- SPEC-MCP-007 (sync queue bridge)

**In Progress:**
- None

**Failed/Escalated:**
- SPEC-MCP-005 (telemetry log tool) — GATE0_FAIL, escalated

**Proposed (not yet specced):**
- None found

---

## Section 3: Gaps and Recommendations

### Q3.1 — Fastest Path to Real-Time Factory Activity View

**What Exists:**
- `/build/stream` SSE endpoint (already streaming heartbeats)
- `monitor-state.json` (persisted state snapshot)
- Build monitor frontend adapter (already consuming SSE)
- Queue runner heartbeats (already being sent)

**Fastest Path (< 1 day):**
1. **Extend `/build/stream` to include queue events**
   - Queue watcher already emits events to `.deia/hive/queue_events.jsonl`
   - Add SSE broadcast for queue state transitions (spec_queued, spec_active, spec_done, spec_dead)
   - Piggyback on existing BuildState subscriber model
   - File: `hivenode/routes/queue_events.py` (already has POST `/mcp/queue/broadcast`)
   - Just need: SSE endpoint `/queue/stream` or merge into `/build/stream`

2. **Add scheduler/dispatcher heartbeats**
   - Scheduler: Send heartbeat on schedule computation (every 30s)
   - Dispatcher: Send heartbeat on dispatch cycle (every 60s)
   - Target: Same `/build/heartbeat` endpoint
   - Task IDs: `scheduler-daemon`, `dispatcher-daemon`

3. **Frontend: Extend build monitor adapter**
   - Add queue state section (backlog count, active count, done count)
   - Add scheduler/dispatcher liveness indicators
   - Render from existing SSE stream

**Alternative (SSE-only):**
- Create `/factory/stream` endpoint that multiplexes:
  - Build heartbeats (from `/build/stream`)
  - Queue events (from queue watcher)
  - Scheduler activity (from schedule.json writes)
  - Dispatcher activity (from dispatched.jsonl writes)
- Single SSE connection for all factory telemetry

### Q3.2 — Data Generated But NOT Exposed

**File-Only Data (no HTTP/SSE endpoint):**
1. **Queue Events** — `.deia/hive/queue_events.jsonl`
   - Written by queue watcher (hivenode/queue_watcher.py)
   - Events: spec_queued, spec_active, spec_done, spec_dead, spec_backlog
   - NOT streamed via SSE (only file writes)

2. **Schedule** — `.deia/hive/schedule.json`
   - Written by scheduler daemon every 30s
   - Contains: task graph, time windows, deadlines, dependencies
   - NOT exposed via HTTP endpoint

3. **Schedule Log** — `.deia/hive/schedule_log.jsonl`
   - Written by scheduler daemon (append-only)
   - Contains: schedule decisions, timing, conflicts
   - NOT exposed via HTTP endpoint

4. **Dispatched Log** — `.deia/hive/dispatched.jsonl`
   - Written by dispatcher daemon (append-only)
   - Contains: spec dispatch events, timestamps, target directories
   - NOT exposed via HTTP endpoint

5. **Dispatcher Log** — `.deia/hive/dispatcher_log.jsonl`
   - Written by dispatcher daemon (structured log)
   - Contains: dispatch actions, slot calculations, errors
   - NOT exposed via HTTP endpoint

6. **Event Ledger** — `.deia/hive/event_ledger.db`
   - Written by LedgerWriter (on-demand)
   - Contains: BUILD_ATTEMPT events, NODE_ANNOUNCED events
   - Queryable via LedgerReader, but **no SSE/streaming endpoint**
   - No tail/watch interface

7. **Log Files** — `*.log` in repo root
   - Written by all daemons (hivenode, scheduler, dispatcher, queue_runner, triage)
   - Plain text, not structured
   - NOT exposed via HTTP (could tail via file system)

**Summary:** ~7 data sources exist but are file-only. No streaming endpoints for queue events, scheduler output, or Event Ledger writes.

### Q3.3 — Minimal "Factory Dashboard" Requirements

**Data Streams Required:**
1. **Queue State** (real-time)
   - Active specs (count + list)
   - Pending specs in backlog (count + list)
   - Completed specs (count + list)
   - Dead/rejected specs (count + list)

2. **Build Progress** (real-time)
   - Active bees (count + list with task IDs, status, progress)
   - Heartbeats (last 100 entries)
   - Total cost (USD, tokens)
   - Tests passed/total

3. **Scheduler/Dispatcher Liveness** (real-time)
   - Scheduler: last run timestamp, next run timestamp
   - Dispatcher: last dispatch timestamp, available slots
   - Queue runner: status (running/stopped)

4. **Error/Alert Feed** (real-time)
   - Spec failures (rejection reasons)
   - TTL timeouts
   - Gate failures
   - Triage escalations

**Backend Requirements:**
- Extend `/build/stream` to include queue events
- Add scheduler/dispatcher heartbeats to `/build/heartbeat`
- Create `/factory/stream` SSE endpoint (multiplexed)
- OR: Extend existing `/build/stream` with additional event types

**Frontend Requirements:**
- Queue state panel (counts + drill-down)
- Active bees panel (from build monitor, already exists)
- Scheduler/dispatcher liveness indicators
- Error/alert feed (scroll log)

**Minimal MVP (< 2 days):**
- Add queue event broadcast to `/build/stream`
- Add scheduler/dispatcher heartbeats
- Extend buildMonitorAdapter.tsx to render queue state
- Deploy

---

## Files Read

1. `hivenode/main.py` (519 lines) — App startup, middleware, MCP server mount (port 8421)
2. `hivenode/routes/health.py` (54 lines) — `/health`, `/status`
3. `hivenode/routes/build_monitor.py` (1000+ lines) — `/build/*` endpoints, SSE stream
4. `hivenode/routes/queue_events.py` (221 lines) — `/mcp/queue/*` endpoints
5. `hivenode/ledger/writer.py` (150 lines) — Event Ledger write interface
6. `hivenode/ledger/reader.py` (150 lines) — Event Ledger query interface
7. `hivenode/queue_watcher.py` (200 lines) — Queue folder watcher (emits MCP events)
8. `hivenode/hive_mcp/local_server.py` (800+ lines) — MCP server, tool registry
9. `hivenode/hive_mcp/tools/telemetry.py` (256 lines) — Heartbeat, status_report, cost_summary tools
10. `.deia/hive/scripts/queue/run_queue.py` (200 lines) — Queue runner, heartbeat emission
11. `.deia/hive/scripts/queue/telemetry_logger.py` (200 lines) — Event Ledger logging
12. `hivenode/scheduler/scheduler_daemon.py` (200 lines) — Scheduler loop
13. `hivenode/scheduler/dispatcher_daemon.py` (200 lines) — Dispatcher loop
14. `browser/src/apps/buildMonitorAdapter.tsx` (200+ lines) — Build monitor frontend
15. `.deia/hive/queue/monitor-state.json` (16,099 lines) — Persisted build state

**Spec Files Read:**
- `.deia/hive/queue/_done/SPEC-MCP-002-heartbeat-upgrade.md`
- `.deia/hive/queue/_escalated/SPEC-MCP-005-telemetry-log-tool.rejection.md`

**Total Files Read:** 17 code files, 2 spec files

---

## Summary: What We Have vs. What's Specced vs. What's Missing

### What We Have Today
- ✅ SSE streaming for build heartbeats (`/build/stream`)
- ✅ Build monitor frontend (real-time bee activity)
- ✅ Heartbeat system (queue runner → hivenode)
- ✅ Event Ledger (BUILD_ATTEMPT events)
- ✅ MCP server with telemetry tools (heartbeat, status_report, cost_summary)
- ✅ File-based telemetry (queue_events.jsonl, schedule.json, dispatched.jsonl, etc.)

### What's Specced
- ✅ SPEC-MCP-002: Heartbeat upgrade (progress + spec_id) — **DONE**
- ✅ SPEC-FACTORY-006: Telemetry logger + Event Ledger integration — **DONE**
- ❌ SPEC-MCP-005: Telemetry log tool — **REJECTED** (GATE0_FAIL)

### What's Missing
- ❌ SSE stream for queue events (specs moving between folders)
- ❌ SSE stream for Event Ledger writes
- ❌ Scheduler/dispatcher heartbeats (liveness visibility)
- ❌ Factory dashboard frontend (queue state + scheduler liveness)
- ❌ Unified `/factory/stream` endpoint (multiplexed telemetry)
- ❌ Log aggregation/streaming endpoint

---

## Fastest Path Forward

**To get a real-time factory activity view:**
1. Add queue event SSE broadcast (piggyback on `/build/stream` or create `/queue/stream`)
2. Add scheduler/dispatcher heartbeats to `/build/heartbeat`
3. Extend buildMonitorAdapter.tsx to render queue state + liveness indicators

**Total Effort:** < 2 days (1 backend spec + 1 frontend spec)

**Alternative (slower but cleaner):**
- Create unified `/factory/stream` SSE endpoint
- Multiplex: build heartbeats + queue events + scheduler activity
- Build standalone factory dashboard primitive

**Total Effort:** 3-4 days (2 backend specs + 1 frontend spec)

---

## Response File
`.deia/hive/responses/20260409-TELEMETRY-SURVEY-RESPONSE.md`

## Tests Created
None (research only)

## Blockers
None
