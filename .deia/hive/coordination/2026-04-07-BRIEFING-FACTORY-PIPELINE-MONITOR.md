# BRIEFING: FACTORY Pipeline Monitor & Completion

## Objective

Monitor the FACTORY spec pipeline through completion. 8 FACTORY specs (001-008) are queued in `.deia/hive/queue/backlog/`. The scheduler daemon and dispatcher daemon are running. FACTORY-001 has been dispatched to queue root. The hivenode server needs to be started so the queue runner bridge picks up specs and dispatches bees.

Your job: ensure the hivenode server is running, monitor the pipeline, and verify each FACTORY spec completes in dependency order.

## Current State

- **Scheduler daemon**: Running (PID 23100), computes `schedule.json` every 30s
- **Dispatcher daemon**: Running (PID 76992), moves "ready" specs from backlog → queue root
- **Hivenode server**: Needs to be started (`python -m uvicorn hivenode.main:app --host 0.0.0.0 --port 8420`)
- **FACTORY-001**: Already in queue root (`.deia/hive/queue/SPEC-FACTORY-001-node-model-extension.md`)
- **FACTORY-002 through 008**: In backlog, blocked by dependencies

## Dependency Graph

```
FACTORY-001 (no deps) → ready NOW
  ├── FACTORY-002 (depends: 001)
  ├── FACTORY-003 (depends: 001)
  ├── FACTORY-004 (depends: 001)
  │     ├── FACTORY-005 (depends: 001, 004)
  │     └── FACTORY-006 (depends: 001, 004)
  └── FACTORY-002 + FACTORY-001:
        └── FACTORY-007 (depends: 001, 002)
              └── FACTORY-008 (depends: 001, 002, 007)
```

## What You Must Do

1. **Start hivenode** if health check fails: `python -m uvicorn hivenode.main:app --host 0.0.0.0 --port 8420`
2. **Monitor the pipeline** by checking:
   - `curl -s http://127.0.0.1:8420/build/status` — queue runner heartbeat
   - `ls .deia/hive/queue/` — specs in queue root (being processed)
   - `ls .deia/hive/queue/_active/` — specs with active bees
   - `ls .deia/hive/queue/_done/` — completed specs
   - `ls .deia/hive/queue/_needs_review/` — failed specs
   - `cat .deia/hive/schedule.json` — current schedule state
   - `tail -5 .deia/hive/dispatcher_log.jsonl` — dispatcher actions
3. **Do NOT manually move spec files.** The scheduler + dispatcher handle all movements.
4. **If a spec fails** (goes to `_needs_review/`): read its output, diagnose the issue, and write a fix spec to `queue/backlog/` with proper YAML frontmatter and `depends_on` referencing the original spec.
5. **Report progress** by writing to `.deia/hive/responses/20260407-FACTORY-PIPELINE-STATUS.md` with:
   - Which specs completed
   - Which failed
   - What's currently active
   - What's blocked

## Key Files

- Specs: `.deia/hive/queue/backlog/SPEC-FACTORY-001` through `SPEC-FACTORY-008`
- PRISM-IR source: `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md`
- Scheduler: `hivenode/scheduler/scheduler_daemon.py`
- Dispatcher: `hivenode/scheduler/dispatcher_daemon.py`
- Queue runner: `.deia/hive/scripts/queue/run_queue.py`
- Queue bridge: `hivenode/queue_bridge.py`

## Constraints

- Do NOT directly move spec files between directories
- Do NOT stop the scheduler or dispatcher daemons
- Do NOT modify the scheduler or dispatcher code
- Check hivenode health every 2 minutes; restart if down
- If ALL 8 specs complete, write a final summary to responses/
