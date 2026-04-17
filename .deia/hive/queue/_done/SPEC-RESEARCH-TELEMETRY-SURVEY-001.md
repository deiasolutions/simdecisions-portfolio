# SPEC-RESEARCH-TELEMETRY-SURVEY-001: Real-Time Telemetry & Factory Visibility Survey

**MODE: EXECUTE**

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Survey the entire codebase to catalog what real-time telemetry, monitoring, and observability infrastructure exists today — both implemented and specced. Q88N wants a real-time view of hivenode activity and factory build progress. Before building anything new, we need to know exactly what's already in place.

## Read First

Start with these, then follow any references you find:

- `hivenode/main.py` — app startup, middleware, any SSE/WebSocket endpoints
- `hivenode/routes/` — scan ALL route files for anything related to: heartbeat, status, health, events, SSE, WebSocket, streaming, monitor, telemetry, metrics
- `hivenode/scheduler/` — scheduler daemon, dispatcher daemon, any status/heartbeat emission
- `hivenode/ledger/` — Event Ledger: schema, write paths, query endpoints
- `hivenode/hive_mcp/` — MCP server: any health, heartbeat, or status tools
- `.deia/hive/scripts/queue/run_queue.py` — queue runner: heartbeat, status emission, logging
- `.deia/hive/scripts/queue/queue_pool.py` — pool processing, any status callbacks
- `.deia/hive/scripts/queue/spec_processor.py` — spec processing, any event emission
- `hivenode/queue_watcher.py` — filesystem watcher, event types emitted
- `hivenode/relay/` — relay bus: does it carry factory events?
- `browser/src/` — any frontend components that consume real-time data (SSE listeners, WebSocket connections, polling)
- `.deia/hive/queue/monitor-state.json` — what does this contain?
- `hivenode/scheduler/scheduler_daemon.py` — scheduler loop, what it emits
- `hivenode/scheduler/dispatcher_daemon.py` — dispatcher loop, what it emits

Also search for:
- Any `EventSource` or `SSE` patterns in frontend code
- Any `/events`, `/stream`, `/ws`, `/monitor` endpoints
- Any spec files (in `queue/_done/`, `docs/specs/`, or `queue/backlog/`) related to telemetry, monitoring, dashboard, or real-time visibility
- Log files: `scheduler.log`, `hivenode.log`, `dispatcher.log`, `queue_runner.log` — what format, what events are logged

## Questions to Answer

### Section 1: What Exists Today (Implemented)

**Q1.1** List every endpoint that provides status, health, or telemetry data. For each: path, method, auth requirement, what data it returns, whether it's polling or streaming.

**Q1.2** Does hivenode have any SSE (Server-Sent Events) or WebSocket endpoints? If yes, what events do they emit? If no, is there any streaming infrastructure at all?

**Q1.3** What does the Event Ledger currently capture? Schema, write frequency, what triggers a write. Can it be queried in real-time?

**Q1.4** What does `monitor-state.json` contain? Who writes it? How often? Is anything reading it?

**Q1.5** What does the MCP server expose for factory/queue visibility? List every tool and resource related to build status, queue state, or factory activity.

**Q1.6** What log files exist, what format are they in, and what events do they capture? Could they be tailed for real-time visibility?

**Q1.7** Does the queue runner or scheduler emit heartbeats? To where? In what format? How frequently?

**Q1.8** Does any frontend component currently display real-time hivenode or factory status? Search for polling intervals, SSE listeners, WebSocket connections.

### Section 2: What's Been Specced But Not Built

**Q2.1** Search `queue/_done/`, `queue/backlog/`, `queue/_needs_review/`, `docs/specs/`, and `.deia/hive/responses/` for any specs related to: telemetry, monitoring, dashboard, real-time, SSE, WebSocket, heartbeat, observability, metrics. List each with status (done, in-progress, specced-not-built).

**Q2.2** Are there any MCP specs (SPEC-MCP-*) related to telemetry or monitoring? What do they propose?

### Section 3: Gaps and Recommendations

**Q3.1** Given what exists: what is the fastest path to a real-time factory activity view? Could we get there by just adding an SSE endpoint that streams existing heartbeat/log data?

**Q3.2** What data is being generated but NOT exposed to any consumer? (e.g., events written to log files but not queryable via API)

**Q3.3** What would a minimal "factory dashboard" need from the backend? List the data streams required: queue state, active specs, build progress, heartbeats, errors.

## Acceptance Criteria

- [ ] Every file in "Read First" list examined and reported with path, line count, key findings
- [ ] All 13 questions (Q1.1–Q3.3) answered with file+line citations
- [ ] Every endpoint related to status/health/telemetry cataloged in a table
- [ ] Every spec related to telemetry/monitoring listed with current status
- [ ] Clear summary: "what we have today" vs "what's specced" vs "what's missing"
- [ ] Response written to `.deia/hive/responses/20260409-TELEMETRY-SURVEY-RESPONSE.md`

## Smoke Test

```bash
test -f .deia/hive/responses/20260409-TELEMETRY-SURVEY-RESPONSE.md && echo "Response exists" || echo "MISSING"
grep -c "^##" .deia/hive/responses/20260409-TELEMETRY-SURVEY-RESPONSE.md
# Should show at least 5 sections
```

## Constraints

- RESEARCH ONLY — do not modify any code files
- Answer from actual file reads, not from memory or assumptions
- If a file does not exist, state "FILE NOT FOUND"
- No stubs. Every question answered.
- Max response length: 600 lines

## Response File

`.deia/hive/responses/20260409-TELEMETRY-SURVEY-RESPONSE.md`
