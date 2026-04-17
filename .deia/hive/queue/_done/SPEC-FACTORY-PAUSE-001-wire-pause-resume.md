## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-FACTORY-PAUSE-001-wire-pause-resume: Wire Pause/Resume to Queue Runner

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

The factory pause/resume endpoints in `factory_routes.py` write `queue_state.json` but the queue runner never reads it. Wire the queue runner's watch loop to check `queue_state.json` before processing specs, and skip processing when paused.

## Files to Read First

- hivenode/routes/factory_routes.py
- .deia/hive/scripts/queue/run_queue.py
- .deia/hive/scripts/queue/queue_pool.py

## Acceptance Criteria

- [ ] Queue runner reads `queue_state.json` from the queue directory before each processing cycle
- [ ] When `state == "paused"`, queue runner logs `[QUEUE] PAUSED — skipping processing` and sleeps until next tick
- [ ] When `state == "running"` or file does not exist, queue runner processes normally
- [ ] Pausing mid-run does NOT kill active bees — it only prevents new specs from being dispatched
- [ ] `POST /factory/pause` pauses the queue runner within one tick cycle
- [ ] `POST /factory/resume` resumes the queue runner within one tick cycle
- [ ] The `factory_routes.py` TODO comment at the signal line is replaced with actual wake call
- [ ] All existing tests still pass
- [ ] 3+ new tests: pause blocks new dispatch, resume allows dispatch, pause does not kill active bees

## Smoke Test

- [ ] `curl -X POST http://127.0.0.1:8420/factory/pause` then drop a spec in backlog — spec should NOT be picked up
- [ ] `curl -X POST http://127.0.0.1:8420/factory/resume` — spec should be picked up on next tick

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Do NOT change the schema of `queue_state.json` — the file is already written by `factory_routes.py`
- Only add read logic in `run_queue.py` to consume the existing state file

## Triage History
- 2026-04-14T21:39:48.559574Z — requeued (empty output)
- 2026-04-14T21:44:48.569488Z — requeued (empty output)
- 2026-04-14T23:14:23.555539Z — requeued (empty output)
