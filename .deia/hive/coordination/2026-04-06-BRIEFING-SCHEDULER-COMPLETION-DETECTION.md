# BRIEFING: Scheduler Not Detecting Task Completions

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P0

## Context

The scheduler/dispatcher pipeline is running. The queue-runner (hivenode) processed 19 MW tasks overnight and moved them to `_done/`. But the scheduler daemon keeps reporting "66 tasks, makespan=95h" every 30s cycle — it's not detecting any completions, so the dispatcher never releases dependency-blocked tasks from backlog/.

The dispatcher successfully moved 17 specs from backlog/ to queue/ (the dependency-free root tasks). The queue-runner picked them up, dispatched bees, and completed them. But the scheduler doesn't see this, so the next wave (Phase 0.5 tests, Phase 1-4 builds) stays blocked.

## The Problem

The scheduler daemon reads `_done/` and `dispatched.jsonl` to determine which tasks have completed. But after 19 tasks completed overnight, the scheduler still shows all 66 tasks with unchanged makespan.

**Investigate:**
1. What format does the scheduler expect completed tasks in `_done/`?
2. What format does the queue-runner actually produce in `_done/`?
3. Is there a naming mismatch? (e.g., scheduler looks for `MW-S01` but file is `SPEC-MW-S01-command-interpreter.md`)
4. Does the scheduler read `dispatched.jsonl` to correlate task_id → spec_file?
5. Is the scheduler looking at the right `_done/` path?

## Key Files

- **Scheduler daemon:** `hivenode/scheduler/scheduler_daemon.py` — the `_check_completions()` or equivalent method
- **Dispatcher daemon:** `hivenode/scheduler/dispatcher_daemon.py` — writes `dispatched.jsonl` with task_id → spec_file mapping
- **Queue-runner:** `.deia/hive/scripts/queue/run_queue.py` and `spec_processor.py` — moves specs to `_done/`
- **Schedule file:** `.deia/hive/schedule.json` — current schedule state
- **Dispatched log:** `.deia/hive/dispatched.jsonl` — records of what was dispatched
- **Done directory:** `.deia/hive/queue/_done/` — where queue-runner puts completed specs
- **Scheduler source:** `hivenode/scheduler/scheduler_mobile_workdesk.py` — TASKS list with IDs and dependencies

## What the Fix Needs to Do

1. **Diagnose** why the scheduler doesn't see completions — read the scheduler daemon code, check what it looks for in `_done/`, compare against what's actually there
2. **Fix** the scheduler daemon to correctly detect completed tasks by matching spec filenames in `_done/` to task IDs (using prefix matching, same pattern as FIX-01 for the dispatcher)
3. **Verify** the scheduler recalculates and releases blocked tasks when it detects completions
4. **Test** with existing `_done/` contents — scheduler should immediately see the 19 completions and update the schedule

## Deliverables

### Task A: Diagnose and fix scheduler completion detection (sonnet bee)
- File: `hivenode/scheduler/scheduler_daemon.py`
- Read the completion detection logic
- Read `_done/` directory to see actual file format
- Read `dispatched.jsonl` to see the task_id → spec_file mapping
- Fix the mismatch
- Add/update tests for completion detection
- Verify all scheduler tests pass
- After fix: scheduler should detect 19 completed tasks and reduce makespan

## Constraints
- TDD where applicable
- No file over 500 lines
- No stubs
- The fix should work with both the queue-runner's file format AND any future format
- Must be backward compatible with existing scheduler behavior
