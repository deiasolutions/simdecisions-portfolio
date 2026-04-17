# BRIEFING: Scheduler + Dispatcher Daemon System

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-05
**Priority:** P0 — Q88N wants this running tonight

## Objective

Split the existing `scheduler_mobile_workdesk.py` into a two-daemon system: **scheduler_daemon.py** (computes schedules with time windows) and **dispatcher_daemon.py** (feeds tasks to the queue runner). Both communicate via files. The existing queue-runner is unchanged.

## Architecture

```
scheduler_daemon.py → schedule.json → dispatcher_daemon.py → backlog/ → queue/ → queue-runner (existing)
```

Two separate processes communicating via files:

```
┌─────────────────────────────────────────────────────────────────┐
│                         SCHEDULER                               │
│                   (scheduler_daemon.py)                         │
├─────────────────────────────────────────────────────────────────┤
│ READS:                                                          │
│   - dispatched.jsonl (what dispatcher sent)                     │
│   - _done/ (completions, for velocity)                          │
│                                                                 │
│ WRITES:                                                         │
│   - schedule.json (current schedule, ordered list)              │
│   - schedule_log.jsonl (diffs, decisions, adjustments)          │
│                                                                 │
│ LOOP every 30s:                                                 │
│   1. Read dispatched.jsonl, mark those tasks as "dispatched"    │
│   2. Read _done/, update velocity from completions              │
│   3. Recompute schedule if needed                               │
│   4. Write schedule.json                                        │
│   5. Log changes to schedule_log.jsonl                          │
│   6. Sleep, repeat                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ schedule.json
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DISPATCHER                              │
│                    (dispatcher_daemon.py)                        │
├─────────────────────────────────────────────────────────────────┤
│ READS:                                                          │
│   - schedule.json (what to dispatch next)                       │
│   - queue/ (how many already in queue)                          │
│   - running/ a.k.a _active/ (how many bees active)             │
│                                                                 │
│ WRITES:                                                         │
│   - backlog/ → queue/ (moves task files)                        │
│   - dispatched.jsonl (append: what it dispatched)               │
│   - dispatcher_log.jsonl (actions taken)                        │
│                                                                 │
│ LOOP every 10s:                                                 │
│   1. Read schedule.json                                         │
│   2. Check slots: max_bees - running - queued                   │
│   3. Move top N tasks from backlog/ to queue/                   │
│   4. Append to dispatched.jsonl                                 │
│   5. Log to dispatcher_log.jsonl                                │
│   6. Sleep, repeat                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ queue/
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       QUEUE-RUNNER (existing, unchanged)        │
└─────────────────────────────────────────────────────────────────┘
```

## File Contracts (all in `.deia/hive/`)

| File | Written by | Read by | Format |
|------|------------|---------|--------|
| `schedule.json` | Scheduler | Dispatcher | Ordered task list with time windows |
| `schedule_log.jsonl` | Scheduler | Ops | Append-only diffs |
| `dispatched.jsonl` | Dispatcher | Scheduler | Append-only dispatch records |
| `dispatcher_log.jsonl` | Dispatcher | Ops | Append-only actions |

### schedule.json format:
```json
{
  "computed_at": "2026-04-05T22:00:00Z",
  "velocity": 1.0,
  "makespan_hours": 50,
  "constraints": {"min_bees": 5, "max_bees": 10},
  "tasks": [
    {
      "task_id": "MW-S01",
      "earliest_start": "2026-04-05T22:00:00Z",
      "latest_start": "2026-04-05T23:00:00Z",
      "estimated_hours": 3,
      "deps": [],
      "status": "ready"
    },
    {
      "task_id": "MW-001",
      "earliest_start": null,
      "latest_start": null,
      "estimated_hours": 8,
      "deps": ["MW-T01"],
      "status": "blocked"
    }
  ]
}
```

### dispatched.jsonl format:
```json
{"ts": "2026-04-05T22:01:00Z", "task_id": "MW-S01", "moved_to": "queue/"}
```

## Source Code

The existing scheduler to extend: `hivenode/scheduler/scheduler_mobile_workdesk.py` (592 lines)

Key functions to reuse:
- `solve_schedule(tasks, min_bees, max_bees, velocity)` — OR-Tools CP-SAT solver, returns schedule with start_hour/end_hour per task
- `Task` dataclass (id, description, duration_hours, dependencies, task_type, status)
- `TASKS` list — 66 tasks with full dependency graph
- `load_state()` / `save_state()` / `apply_state()` / `compute_velocity()` — state management
- `mark_complete()` / `mark_started()` — task lifecycle

Daemon patterns to follow (already in repo):
- `hivenode/rag/indexer/sync_daemon.py` — SyncDaemon with threading.Thread, start/stop, daemon loop
- `hivenode/queue_bridge.py` — QueueRunnerBridge with asyncio.to_thread, wake_event

## Queue Directory Layout (existing)

```
.deia/hive/queue/
├── _active/        ← specs currently being processed by queue-runner
├── _done/          ← completed specs
├── _dead/          ← failed specs (max retries)
├── _hold/          ← specs on hold
├── _stage/         ← staging area
├── _needs_review/  ← needs human review
├── backlog/        ← NEW: dispatcher moves from here to queue root
├── SPEC-*.md       ← queue root: specs waiting for queue-runner to pick up
└── monitor-state.json
```

NOTE: `backlog/` does not exist yet — Q33N must create it. The dispatcher moves spec files from `backlog/` to `queue/` root. The queue-runner picks up from `queue/` root as it always has.

## Deliverables

### Task 1: scheduler_daemon.py (P0, start immediately)
- File: `hivenode/scheduler/scheduler_daemon.py`
- Reuse `solve_schedule()`, `Task`, `TASKS`, and state management from existing scheduler
- Import from scheduler_mobile_workdesk.py — do NOT copy/paste
- Add time window computation (earliest_start, latest_start as ISO timestamps)
- `--dry-run` flag: show schedule, wait for "y" before entering loop
- Daemon loop: 30s interval, reads dispatched.jsonl + _done/, writes schedule.json + schedule_log.jsonl
- Time windows: earliest_start = max(now, all deps complete), latest_start = earliest_start + 1 hour (or null)
- CLI: `python scheduler_daemon.py --min-bees 5 --max-bees 10 --dry-run`
- **Model: sonnet** (this is algorithmic, needs precision)

### Task 2: dispatcher_daemon.py (P0, can start in parallel)
- File: `hivenode/scheduler/dispatcher_daemon.py`
- Loop: 10s interval
- Reads schedule.json, checks slots (max_bees - active - queued)
- Moves spec files from `backlog/` to `queue/` root
- Writes to dispatched.jsonl + dispatcher_log.jsonl
- Task files must exist in backlog/ — dispatcher moves them, doesn't create them
- CLI: `python dispatcher_daemon.py --max-bees 10`
- **Model: sonnet**

### Task 3: Create backlog/ directory and seed with test specs (P1)
- Create `.deia/hive/queue/backlog/`
- Write 2-3 small test spec files to verify the pipeline works
- **Model: haiku** (simple file creation)

## Constraints

- No file over 500 lines
- TDD: tests first (pytest)
- No stubs
- Import from existing scheduler, don't duplicate
- Both daemons must handle graceful shutdown (SIGINT/SIGTERM)
- Both must work on Windows (Git Bash) — no Unix-only signals
- Fix the `datetime.utcnow()` deprecation — use `datetime.now(datetime.UTC)` everywhere
- Fix Windows encoding: use ASCII fallback for icons or set UTF-8 encoding

## Dependencies

- Task 1 and Task 2 can run in parallel (different files, communicate via files)
- Task 3 depends on Task 2 (needs dispatcher to exist to test pipeline)

## Startup Sequence

```bash
# Terminal 1: Scheduler
python hivenode/scheduler/scheduler_daemon.py --min-bees 5 --max-bees 10 --dry-run

# Terminal 2: Dispatcher
python hivenode/scheduler/dispatcher_daemon.py --max-bees 10

# Terminal 3: Queue-runner (already running, unchanged)
```
