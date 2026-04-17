# TASK-SD-02: Dispatcher Daemon with Slot Management

## Objective
Build `dispatcher_daemon.py` that reads schedule.json, checks available bee slots (max_bees - active - queued), moves spec files from `backlog/` to `queue/` root, logs dispatches to `dispatched.jsonl` and `dispatcher_log.jsonl`, runs in a 10-second daemon loop.

## Context
The dispatcher is the execution arm of the scheduler. It does NOT compute schedules — it consumes schedule.json (written by TASK-SD-01) and makes it happen by:
1. Reading schedule.json to see what tasks are ready to dispatch
2. Counting active bees (`_active/`) and queued specs (`queue/` root)
3. Calculating available slots: `max_bees - active_count - queued_count`
4. Moving the top N spec files from `backlog/` to `queue/` root (where queue-runner picks them up)
5. Logging what it dispatched to `dispatched.jsonl` (scheduler reads this)
6. Logging its actions to `dispatcher_log.jsonl` (ops visibility)

The dispatcher does NOT create spec files — it only moves existing files. The spec files must already exist in `backlog/` with names matching task_id from schedule.json (e.g., `SPEC-MW-S01.md`).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\sync_daemon.py`
  Daemon pattern: threading.Thread, start/stop, daemon loop with sleep, graceful shutdown
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-04-05-BRIEFING-SCHEDULER-DAEMONS.md`
  Architecture diagram, file contracts, dispatched.jsonl format

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\dispatcher_daemon.py` (max 500 lines)
- [ ] DispatcherDaemon class with threading.Thread pattern
- [ ] start() method: launch daemon thread
- [ ] stop() method: graceful shutdown (sets running=False, joins thread with 10s timeout)
- [ ] _daemon_loop() method: 10s interval, reads schedule.json, counts slots, moves files, logs dispatches
- [ ] CLI with argparse:
  - `--max-bees` (default: 10)
  - `--schedule-dir` (default: `.deia/hive/`)
  - `--queue-dir` (default: `.deia/hive/queue/`)
  - `--dry-run` flag: log what it WOULD dispatch, but don't move files
- [ ] Slot calculation:
  ```python
  active_count = count_specs_in(queue_dir / "_active")
  queued_count = count_specs_in(queue_dir, pattern="SPEC-*.md")
  available_slots = max_bees - active_count - queued_count
  ```
- [ ] File paths (all relative to queue_dir):
  - Read: `backlog/SPEC-*.md`, `_active/SPEC-*.md`, `queue/SPEC-*.md` (root)
  - Read: `../schedule.json` (schedule_dir)
  - Write: `../dispatched.jsonl` (schedule_dir, append-only)
  - Write: `../dispatcher_log.jsonl` (schedule_dir, append-only)
- [ ] Dispatch logic:
  1. Read schedule.json
  2. Filter tasks to status="ready" (not blocked, not dispatched, not in_progress, not done)
  3. Sort by earliest_start (ascending)
  4. For each ready task (up to available_slots):
     - Look for `backlog/SPEC-{task_id}.md` (case-insensitive match on task_id)
     - If file exists: move to `queue/SPEC-{task_id}.md`
     - If file does NOT exist: log warning to dispatcher_log.jsonl, skip
  5. Append each successful dispatch to dispatched.jsonl
  6. Log all actions to dispatcher_log.jsonl
- [ ] dispatched.jsonl format (append-only):
  ```json
  {"ts": "2026-04-05T22:01:00Z", "task_id": "MW-S01", "moved_to": "queue/", "spec_file": "SPEC-MW-S01.md"}
  ```
- [ ] dispatcher_log.jsonl format (append-only):
  ```json
  {"ts": "2026-04-05T22:01:00Z", "event": "cycle_start", "active": 2, "queued": 3, "slots": 5, "max_bees": 10}
  {"ts": "2026-04-05T22:01:00Z", "event": "dispatch", "task_id": "MW-S01", "spec_file": "SPEC-MW-S01.md"}
  {"ts": "2026-04-05T22:01:00Z", "event": "spec_not_found", "task_id": "MW-S02", "expected_file": "SPEC-MW-S02.md"}
  {"ts": "2026-04-05T22:01:00Z", "event": "cycle_end", "dispatched": 1, "skipped": 1}
  ```
- [ ] Handle missing schedule.json gracefully: log warning, sleep, retry next cycle
- [ ] Handle SIGINT/SIGTERM gracefully (Windows-compatible: use signal.signal for SIGINT only)
- [ ] Fix datetime.utcnow() deprecation: use `datetime.now(datetime.UTC)` everywhere
- [ ] Logging: use logging module, log to stdout at INFO level (dispatch cycles, file moves, warnings)
- [ ] Atomic file moves: use `shutil.move()` to avoid partial writes

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_dispatcher_daemon.py`
- [ ] Test: daemon starts and stops cleanly
- [ ] Test: --dry-run flag prevents file moves
- [ ] Test: slot calculation (active + queued vs max_bees)
- [ ] Test: moves spec files from backlog/ to queue/
- [ ] Test: appends to dispatched.jsonl with correct format
- [ ] Test: appends to dispatcher_log.jsonl with cycle events
- [ ] Test: skips tasks when spec file not found in backlog/
- [ ] Test: handles missing schedule.json gracefully (logs warning, retries next cycle)
- [ ] Test: respects max_bees limit (does not over-dispatch)
- [ ] Test: SIGINT triggers graceful shutdown
- [ ] Edge cases:
  - No backlog/ directory (create it or log error)
  - No schedule.json (daemon idles and logs warning)
  - All slots full (daemon idles until slots open)
  - Case-insensitive task_id matching (MW-S01 should match SPEC-mw-s01.md)
- [ ] All tests pass: `cd hivenode && python -m pytest tests/hivenode/scheduler/test_dispatcher_daemon.py -v`
- [ ] Minimum 12 test functions

## Constraints
- No file over 500 lines (hard limit)
- CSS: N/A (backend only)
- No stubs — every function fully implemented
- Use threading.Thread pattern (not asyncio) — matches sync_daemon.py
- Windows-compatible signals: SIGINT only (no SIGTERM)
- No external dependencies beyond stdlib (json, argparse, datetime, pathlib, threading, signal, logging, shutil)
- Do NOT create spec files — only move existing files from backlog/ to queue/

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260405-TASK-SD-02-RESPONSE.md`

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
