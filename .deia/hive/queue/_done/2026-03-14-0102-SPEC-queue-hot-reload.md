# SPEC: BL-121 Queue Runner Hot-Reload

## Priority
P1

## Objective
Make run_queue.py re-scan the queue directory on each loop iteration so new specs added while the queue is running are picked up automatically without restarting.

## Context
Currently `run_queue.py` reads the queue directory once at startup and processes that fixed list. If new specs are added to `.deia/hive/queue/` while the queue is running, they are not picked up until the next manual run. This spec adds hot-reload: each iteration of the main loop re-scans the directory for new `.md` files.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue orchestration loop
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — queue config

## Acceptance Criteria
- [ ] Each iteration of the main loop in run_queue.py re-scans `.deia/hive/queue/` for `.md` files (excluding morning reports, README, etc.)
- [ ] New specs added during a running queue session are detected and processed in the next iteration
- [ ] Already-processed specs (moved to `_done/` or `_needs_review/`) are not re-processed
- [ ] Already-in-progress specs are not re-dispatched
- [ ] Session tracking distinguishes between specs from initial scan vs hot-reloaded specs
- [ ] Print a log message when new specs are detected: "Hot-reload: found N new spec(s)"
- [ ] Budget tracking still works correctly with hot-reloaded specs (total cost across all specs)
- [ ] 6+ tests covering: re-scan detection, deduplication, budget continuity, empty re-scan
- [ ] Use `flush=True` on all print() calls (stdout buffering fix from earlier session)

## Model Assignment
haiku

## Constraints
- Do NOT restructure the main loop — add re-scan logic at the top of each iteration
- Do NOT change the spec file format
- Keep the existing `_done/` and `_needs_review/` archive behavior
- No file over 500 lines
