# TASK-MCP-QUEUE-06: Update Documentation

## Objective

Update process docs, deployment guides, and create spec document to capture the MCP queue notification architecture for future reference.

## Context

Tasks 01-05 implemented and tested the MCP notification system. This task documents the architecture, operational procedures, and deployment steps.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`

## Files to Read First

- `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
  - Complete design document (source material)
- `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-TEST-REPORT.md`
  - Test results and recommendations
- `.deia/processes/` (if exists)
  - Existing process docs to understand format

## Deliverables

- [ ] `.deia/processes/P-SCHEDULER.md` — Scheduler process doc (NEW or UPDATE)
  - Overview of scheduler daemon
  - MCP event flow diagram
  - Fallback polling behavior
  - CLI flags and configuration
  - Troubleshooting guide
- [ ] `.deia/processes/P-DISPATCHER.md` — Dispatcher process doc (NEW or UPDATE)
  - Overview of dispatcher daemon
  - MCP event flow diagram
  - In-memory counter architecture
  - Fallback refresh behavior
  - CLI flags and configuration
  - Troubleshooting guide
- [ ] `.deia/specs/SPEC-MCP-QUEUE-NOTIFICATIONS.md` — Canonical spec (copy of design doc)
  - Exact copy of design doc for archival
  - Link to implementation tasks
  - Link to test report
- [ ] `docs/deployment/RAILWAY-DEPLOYMENT.md` — Railway deployment guide (UPDATE)
  - MCP configuration (env vars)
  - Port configuration (8422, 8423)
  - Health check endpoints
  - Monitoring recommendations
- [ ] `docs/deployment/LOCAL-DEV.md` — Local development guide (UPDATE)
  - How to run scheduler/dispatcher with MCP enabled
  - How to test MCP events manually
  - How to disable MCP for debugging
- [ ] `README.md` updates (if applicable)
  - Brief mention of MCP event system
  - Link to process docs

## Test Requirements

- [ ] Documentation review (internal consistency check)
- [ ] Deployment steps validated on local dev environment
- [ ] CLI examples tested (copy-paste into terminal, verify works)
- [ ] All links valid (no broken references)

## Acceptance Criteria

- [ ] All process docs accurate and complete
- [ ] Deployment guides include MCP-specific steps
- [ ] Troubleshooting sections cover common issues:
  - "Scheduler not waking on events" → check MCP server port
  - "Dispatcher counters out of sync" → check fallback refresh logs
  - "Events not delivered" → check subscriber registry
- [ ] All CLI examples tested and working
- [ ] Spec document archived in `.deia/specs/`
- [ ] Q88N approves documentation (pending review)
- [ ] No file over 500 lines

## Implementation Notes

### Process Doc Template (P-SCHEDULER.md)

```markdown
# P-SCHEDULER: Scheduler Daemon with MCP Events

**Status:** OPERATIONAL
**Owner:** Q88N
**Last Updated:** 2026-04-06

## Overview

The scheduler daemon computes optimal task schedules using OR-Tools CP-SAT solver. It runs in a daemon loop, recalculating schedules when specs complete.

**MCP Integration:** Scheduler wakes instantly on `queue.spec_done` events instead of polling every 30s.

## Architecture

[Event flow diagram]

```
[Queue runner moves spec to _done/]
    ↓
[Hivenode watcher detects move]
    ↓
[POST /mcp/queue/broadcast]
    ↓
[POST http://localhost:8422/mcp/event]
    ↓
[Scheduler daemon.on_mcp_event()]
    ↓
[Wake event set]
    ↓
[Daemon loop wakes, recalculates schedule]
```

## Configuration

### CLI Flags

- `--mcp-enabled` (default: true) — Enable MCP event-driven mode
- `--min-bees N` — Minimum concurrent bees
- `--max-bees N` — Maximum concurrent bees

### Environment Variables

- `SCHEDULER_MCP_PORT` (default: 8422) — MCP event receiver port
- `SCHEDULER_FALLBACK_INTERVAL` (default: 60) — Fallback polling interval (seconds)

## Fallback Behavior

If MCP server unavailable:
- Daemon falls back to 60s polling (slower than event-driven, but reliable)
- Logs warning: "MCP server unavailable, using fallback polling"
- No crashes, no data loss

## Troubleshooting

### Scheduler not waking on events

**Symptoms:** Schedule recalculates every 60s instead of instantly

**Diagnosis:**
```bash
curl http://localhost:8422/health
# Should return {"status": "ok"}
```

**Fix:**
- Check MCP server started (log: "MCP server started on port 8422")
- Check port not blocked by firewall
- Check hivenode watcher running (log: "Watcher started")

### Schedule computation errors

**Symptoms:** schedule.json not updated, errors in schedule_log.jsonl

**Diagnosis:**
```bash
tail -f .deia/hive/schedule_log.jsonl | grep error
```

**Fix:**
- Check task dependencies (circular dependencies fail solver)
- Check velocity computation (requires completed specs in _done/)

## Monitoring

Metrics to monitor:
- Latency: time from spec completion to schedule update (<2s expected)
- Fallback polls: should be rare (<1/hour if MCP healthy)
- Solver failures: should be 0

## References

- Design doc: `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
- Source: `hivenode/scheduler/scheduler_daemon.py`
```

### Deployment Guide Updates (RAILWAY-DEPLOYMENT.md)

```markdown
## MCP Queue Notifications (2026-04-06)

### Configuration

Add to Railway environment variables:

```bash
MCP_ENABLED=true
SCHEDULER_MCP_PORT=8422
DISPATCHER_MCP_PORT=8423
```

### Health Checks

Railway health check URLs:
- Hivenode: `http://localhost:8420/health`
- Scheduler MCP: `http://localhost:8422/health`
- Dispatcher MCP: `http://localhost:8423/health`

### Monitoring

Set up alerts for:
- MCP server downtime (health check 500)
- High fallback poll rate (>10/hour)
- Event delivery failures (check hivenode logs)

### Deployment Steps

1. Deploy hivenode (includes watcher)
2. Verify watcher started: `curl http://localhost:8420/health`
3. Start scheduler daemon: `python hivenode/scheduler/scheduler_daemon.py --mcp-enabled`
4. Start dispatcher daemon: `python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled`
5. Test event delivery: move a spec to `_done/`, verify schedule updates within 2s
```

### Local Dev Guide Updates (LOCAL-DEV.md)

```markdown
## Running Scheduler/Dispatcher with MCP

**Terminal 1: Hivenode (includes watcher)**
```bash
python -m hivenode.main
```

**Terminal 2: Scheduler**
```bash
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled
```

**Terminal 3: Dispatcher**
```bash
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

## Testing MCP Events Manually

**1. Move a spec to _done/**
```bash
mv .deia/hive/queue/_active/SPEC-TEST-001.md .deia/hive/queue/_done/
```

**2. Check event log**
```bash
tail -f .deia/hive/queue_events.jsonl
```

Expected output:
```json
{"event":"queue.spec_done","spec_file":"SPEC-TEST-001.md","task_id":"TEST-001","directory":"_done","timestamp":"2026-04-06T12:34:56Z"}
```

**3. Verify scheduler woke**
```bash
tail -f .deia/hive/schedule_log.jsonl
```

Expected latency: <2s

## Disabling MCP (for debugging)

```bash
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled=false
```

Scheduler will fall back to 30s polling (original behavior).
```

## Constraints

- Follow existing docs style (check `.deia/processes/` for format)
- No file over 500 lines
- Use clear headings, bullet points, code blocks
- Include diagrams (ASCII or mermaid) for event flows
- All examples must be copy-pasteable
- No stubs — all docs complete

## Dependencies

**Depends on:** TASK-MCP-QUEUE-05 (test results needed for deployment recommendations)

## Estimated Duration

1-1.5 hours (Haiku or Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-06-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts (N/A for docs, but verify links)
5. **Build Verification** — N/A for docs (skip or write "N/A")
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — Q88N approval pending, any gaps in docs

DO NOT skip any section.
