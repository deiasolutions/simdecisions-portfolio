# BRIEFING: FACTORY Pipeline — Final Wave Completion

## Objective

Complete the final phase of the FACTORY pipeline. FACTORY-008 needs to be dispatched (all deps satisfied). FACTORY-005 and FACTORY-006 are still active. Monitor everything to completion and write a final summary.

## Current State

### Done (in `_done/`)
- FACTORY-001: Node model extension
- FACTORY-002: Dependency resolution
- FACTORY-003: TTL enforcement
- FACTORY-004: Acceptance criteria
- FACTORY-007: DAG support

### Active (in `_active/`)
- FACTORY-005: Bundle context guard (bee running)
- FACTORY-006: Telemetry policy split (bee running)

### Blocked (in `backlog/`)
- FACTORY-008: Orphan detection — deps all satisfied (001, 002, 007 are done)

### Infrastructure
- Hivenode running on port 8420
- Scheduler daemon and dispatcher daemon should be running
- If not running, restart them

## What You Must Do

### Step 1: Dispatch FACTORY-008
FACTORY-008's dependencies (001, 002, 007) are all in `_done/`. It should be dispatched.

If the scheduler/dispatcher are running correctly, FACTORY-008 should automatically move from backlog to queue root. Check schedule.json to verify FACTORY-008 shows `status: "ready"`.

If the scheduler has the known bug (done_ids not including queue-completed specs), you may need to move FACTORY-008 from backlog to queue root manually:
```bash
mv .deia/hive/queue/backlog/SPEC-FACTORY-008-orphan-detection.md .deia/hive/queue/
curl -X POST http://127.0.0.1:8420/build/queue-wake
```

### Step 2: Monitor Active Bees
Check every 2 minutes:
- `ls .deia/hive/queue/_active/` — should show active specs
- `ls .deia/hive/queue/_done/` — specs completing
- `ls .deia/hive/queue/_needs_review/` — any failures
- `curl -s http://127.0.0.1:8420/build/status` — heartbeat

### Step 3: Handle Failures
If any spec goes to `_needs_review/`:
- Read the response file in `.deia/hive/responses/`
- Diagnose the issue
- Write a fix spec to `queue/backlog/` if needed

### Step 4: Write Final Summary
When ALL 8 FACTORY specs are complete, write a comprehensive summary to:
`.deia/hive/responses/20260407-FACTORY-PIPELINE-FINAL-SUMMARY.md`

Include:
- Status of all 8 specs (complete/failed)
- Test counts per spec
- Total cost
- Files created/modified
- Known issues or bugs found
- Any scheduler/dispatcher bugs encountered

## Constraints
- Do NOT modify scheduler or dispatcher code
- Do NOT stop running services unless they're broken
- If hivenode is down, restart it: `python -m uvicorn hivenode.main:app --host 0.0.0.0 --port 8420`
- Check hivenode health before any queue operations
