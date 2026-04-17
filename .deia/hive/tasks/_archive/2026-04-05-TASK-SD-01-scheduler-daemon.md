# TASK-SD-01: Scheduler Daemon with Time Windows

## Objective
Build `scheduler_daemon.py` that computes task schedules with time windows using OR-Tools CP-SAT solver, runs in a 30-second daemon loop, reads dispatcher feedback and completions, writes schedule.json and schedule_log.jsonl.

## Context
The existing `scheduler_mobile_workdesk.py` (592 lines) contains a full OR-Tools CP-SAT solver implementation for the Mobile Workdesk build with 66 tasks. This daemon extracts and extends that solver logic to run continuously, adding:
- Time window computation (earliest_start, latest_start as ISO timestamps)
- Daemon loop (30s interval with graceful shutdown)
- Feedback from dispatcher via `dispatched.jsonl`
- Velocity updates from `_done/` completions
- Schedule diff logging to `schedule_log.jsonl`

The scheduler does NOT move files or dispatch work — it only computes the optimal schedule. The dispatcher (TASK-SD-02) consumes schedule.json.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_mobile_workdesk.py`
  Study: solve_schedule(), Task dataclass, TASKS list, load_state(), save_state(), apply_state(), compute_velocity(), mark_complete(), mark_started()
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\sync_daemon.py`
  Daemon pattern: threading.Thread, start/stop, daemon loop with sleep, graceful shutdown
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\queue_bridge.py`
  Alternative daemon pattern: asyncio.to_thread, wake_event for interruptible sleep

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py` (max 500 lines)
- [ ] Import and reuse from scheduler_mobile_workdesk.py: solve_schedule, Task, TASKS, load_state, save_state, apply_state, compute_velocity
- [ ] SchedulerDaemon class with threading.Thread pattern (like sync_daemon.py)
- [ ] start() method: launch daemon thread
- [ ] stop() method: graceful shutdown (sets running=False, joins thread with 10s timeout)
- [ ] _daemon_loop() method: 30s interval, reads dispatched.jsonl + _done/, computes schedule, writes schedule.json + schedule_log.jsonl
- [ ] Time window computation:
  - earliest_start = max(now, all_deps_complete_time)
  - latest_start = earliest_start + 1 hour (if no deps downstream, can be null)
  - Emit ISO 8601 timestamps (e.g., "2026-04-05T22:00:00Z")
- [ ] CLI with argparse:
  - `--min-bees` (default: 5)
  - `--max-bees` (default: 10)
  - `--dry-run` flag: compute schedule, print it, prompt "Press 'y' to start daemon loop or 'n' to exit:", only enter loop if user types 'y'
  - `--schedule-dir` (default: `.deia/hive/`)
  - `--queue-dir` (default: `.deia/hive/queue/`)
- [ ] File paths (all relative to schedule_dir):
  - Read: `dispatched.jsonl`, `queue/_done/SPEC-*.md` (for velocity updates)
  - Write: `schedule.json`, `schedule_log.jsonl` (append-only)
- [ ] schedule.json format:
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
        "adjusted_hours": 3,
        "deps": [],
        "status": "ready"
      },
      {
        "task_id": "MW-001",
        "earliest_start": null,
        "latest_start": null,
        "estimated_hours": 8,
        "adjusted_hours": 8,
        "deps": ["MW-T01"],
        "status": "blocked"
      }
    ]
  }
  ```
- [ ] schedule_log.jsonl format (append-only):
  ```json
  {"ts": "2026-04-05T22:00:00Z", "event": "schedule_computed", "makespan_hours": 50, "velocity": 1.0, "task_count": 66}
  {"ts": "2026-04-05T22:00:30Z", "event": "task_dispatched", "task_id": "MW-S01"}
  {"ts": "2026-04-05T22:30:00Z", "event": "velocity_updated", "old_velocity": 1.0, "new_velocity": 0.95, "reason": "MW-S01 took 3.2h (est 3h)"}
  ```
- [ ] Velocity updates: when specs in `_done/` have telemetry (actual_hours vs estimated_hours), update velocity = sum(actual) / sum(estimated)
- [ ] Task status tracking:
  - "ready" — all deps satisfied, can be dispatched
  - "blocked" — waiting on deps
  - "dispatched" — moved to queue by dispatcher (read from dispatched.jsonl)
  - "in_progress" — being built by queue-runner (inferred from _active/)
  - "done" — completed (inferred from _done/)
- [ ] Handle SIGINT/SIGTERM gracefully (Windows-compatible: use signal.signal for SIGINT only, no SIGTERM)
- [ ] Fix datetime.utcnow() deprecation: use `datetime.now(datetime.UTC)` everywhere
- [ ] Use ASCII fallback for icons (○, ▶, ✓) or set UTF-8 encoding at top of file
- [ ] Logging: use logging module, log to stdout at INFO level (daemon loop cycles, schedule changes, velocity updates)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_scheduler_daemon.py`
- [ ] Test: daemon starts and stops cleanly
- [ ] Test: --dry-run flag prevents daemon loop from starting
- [ ] Test: time window computation (earliest_start, latest_start)
- [ ] Test: velocity update from _done/ specs
- [ ] Test: task status transitions (ready → dispatched → done)
- [ ] Test: schedule.json written with correct format
- [ ] Test: schedule_log.jsonl appends events
- [ ] Test: SIGINT triggers graceful shutdown
- [ ] Edge cases:
  - No dispatched.jsonl file (start fresh)
  - Empty _done/ directory (velocity = 1.0)
  - Circular dependencies (should error or warn)
  - All tasks completed (daemon should idle)
- [ ] All tests pass: `cd hivenode && python -m pytest tests/hivenode/scheduler/test_scheduler_daemon.py -v`
- [ ] Minimum 10 test functions

## Constraints
- No file over 500 lines (hard limit)
- CSS: N/A (backend only)
- No stubs — every function fully implemented
- Import from scheduler_mobile_workdesk.py — do NOT copy/paste solve_schedule, Task, TASKS, or state management functions
- Use threading.Thread pattern (not asyncio) — matches sync_daemon.py
- Windows-compatible signals: SIGINT only (no SIGTERM)
- No external dependencies beyond what scheduler_mobile_workdesk.py already uses (ortools, dataclasses, json, argparse, datetime, pathlib, threading, signal, logging)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260405-TASK-SD-01-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — platform-populated from build monitor telemetry (do not estimate manually)
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
