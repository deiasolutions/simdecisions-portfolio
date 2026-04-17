# TASK-161: Port entity scheduler

## Objective
Port entity scheduler from platform to shiftcenter. APScheduler integration for nightly recalculation cron job. API endpoints for scheduler control (start, stop, status, trigger-now).

## Context
The entity scheduler wraps APScheduler and runs the nightly recalculation job at a configurable time (default: 02:00 UTC). It provides API endpoints to start/stop the scheduler, check status, and manually trigger the nightly recalc.

**Platform source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\scheduler.py` (188 lines)

**Target file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\scheduler.py` (NEW)

**Key features to port:**
- `EntityScheduler` class wrapping APScheduler `BackgroundScheduler`
- `start()` — starts scheduler with nightly recalc job
- `stop()` — stops scheduler gracefully
- `get_status()` — returns scheduler state (running, stopped, job count)
- `trigger_now()` — manually triggers nightly recalc (useful for testing)
- Configurable cron schedule (env var `ENTITY_RECALC_CRON`, default `0 2 * * *` = 02:00 UTC daily)
- Error handling and logging for job execution

**Dependencies:**
- `hivenode.entities.updates` (nightly_recalculation function) — **TASK-160 dependency**
- `apscheduler` library — needs to be added to pyproject.toml
- `engine.database` (get_db for session management)

**Important:** This task depends on TASK-160 (updates.py) completing first. The scheduler calls `nightly_recalculation()` from updates.py.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\scheduler.py` (source file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\updates.py` (newly created by TASK-160)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\database.py` (for session management pattern)

## Deliverables
- [ ] Add `apscheduler = "^3.10.4"` to `pyproject.toml` dependencies
- [ ] `hivenode\entities\scheduler.py` created with full implementation (no stubs)
- [ ] `EntityScheduler` class fully implemented
- [ ] `start()` method — initializes scheduler and adds nightly recalc job
- [ ] `stop()` method — shuts down scheduler gracefully
- [ ] `get_status()` method — returns dict with scheduler state
- [ ] `trigger_now()` method — manually executes nightly recalc
- [ ] Configurable cron schedule via env var (default: `0 2 * * *`)
- [ ] Proper error handling (job execution failures don't crash scheduler)
- [ ] Logging for job execution (info level for start/stop, debug for job triggers)
- [ ] Singleton pattern (only one scheduler instance allowed)
- [ ] File size under 500 lines (platform source is 188, should fit easily)
- [ ] All methods return proper types (no `Any`, no placeholders)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `tests\hivenode\entities\test_scheduler.py`
- [ ] All tests pass
- [ ] Test count target: 8-10 tests minimum
- [ ] Edge cases:
  - Start scheduler twice → second call is no-op or raises error
  - Stop scheduler before start → no error
  - Trigger job before scheduler started → raises error
  - Job execution failure → logged but scheduler continues running
  - Invalid cron expression → raises error on start
  - Scheduler state after start → returns "running"
  - Scheduler state after stop → returns "stopped"
  - Multiple trigger_now calls in rapid succession → queued properly
- [ ] Test scheduler lifecycle (start → check status → trigger → stop)
- [ ] Test job registration (verify nightly recalc job added to scheduler)
- [ ] Test manual trigger (verify nightly_recalculation called)
- [ ] Mock APScheduler for deterministic tests (don't wait for cron)
- [ ] Mock nightly_recalculation to verify it's called with correct db session

## Constraints
- No file over 500 lines (platform source is 188, port should be similar)
- CSS: var(--sd-*) only (not applicable, backend only)
- No stubs — every function fully implemented
- TDD: tests first, then implementation
- Scheduler must be singleton (only one instance allowed)
- Proper cleanup on shutdown (call stop() on app shutdown)
- All imports must use absolute paths (`from hivenode.entities.updates import ...`)
- Follow existing service patterns in hivenode (see other scheduler/background task examples if any)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-161-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Test Commands

```bash
# Run scheduler tests only
python -m pytest tests/hivenode/entities/test_scheduler.py -v

# Run all entity tests (verify no regressions)
python -m pytest tests/hivenode/entities/ -v
```

## Model Assignment
Haiku (straightforward scheduler wrapper, no complex logic)

## Priority
P0.55 (critical path for entity vectors MVP)

## Dependencies
**BLOCKED BY:** TASK-160 (updates.py must exist with nightly_recalculation function)

## Additional Notes
After this task completes, the scheduler needs to be registered in the FastAPI app startup/shutdown lifecycle:
- On app startup: call `EntityScheduler().start()`
- On app shutdown: call `EntityScheduler().stop()`

This will be handled in TASK-162 (routes) or can be done in hivenode/main.py if scheduler is meant to run independently of routes.
