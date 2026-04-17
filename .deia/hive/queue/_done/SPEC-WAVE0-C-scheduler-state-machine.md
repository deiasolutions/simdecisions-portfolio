# SPEC-WAVE0-C: Scheduler State Machine Extension

## Priority
P0

## Model Assignment
sonnet

## Depends On
SPEC-WAVE0-A-ddd-directories
SPEC-WAVE0-B-qa-dispatch-logic

## Intent

Extend the scheduler to recognize the new DDD state directories and include them in velocity tracking and capacity planning.

## Files to Read First

hivenode/scheduler/scheduler_daemon.py
hivenode/scheduler/dispatcher_daemon.py
.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md

## Work Required

### 1. Add new states to scheduler

The scheduler currently tracks tasks in: backlog/, queue/, running/, _done/

Add recognition of the new states:
  _code_complete/   -- built, awaiting QA bee
  _qa_review/       -- QA bee reviewing
  _q33n_review/     -- awaiting Q33N decision
  _needs_revision/  -- returned for fixes

### 2. Update velocity calculation

Tasks in _code_complete/, _qa_review/, _q33n_review/ are "in flight" -- they should count against active capacity and NOT be scheduled over.

Tasks in _needs_revision/ are re-queued -- they should be treated as new tasks re-entering the queue with elevated priority (P0.5).

### 3. Update schedule.json output

Add a new section to the schedule.json the scheduler produces:

  "pipeline_state": {
    "in_queue": N,
    "running": N,
    "code_complete_awaiting_qa": N,
    "in_qa_review": N,
    "in_q33n_review": N,
    "needs_revision": N,
    "done_today": N
  }

### 4. Update schedule_log.jsonl

Each scheduler cycle entry should include pipeline_state snapshot.

## Acceptance Criteria

- [ ] Scheduler reads task counts from all 8 state directories
- [ ] _code_complete and _qa_review tasks count against active capacity
- [ ] _needs_revision tasks re-enter queue at P0.5 priority
- [ ] schedule.json includes pipeline_state section
- [ ] Scheduler does not crash if new directories are empty
- [ ] Existing scheduler behavior unchanged for standard states
- [ ] Tests cover all new state transitions

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- 8-section response file on completion

## Smoke Test

After completion:
```bash
# Verify scheduler recognizes new states
python hivenode/scheduler/scheduler_daemon.py --dry-run

# Check schedule.json contains pipeline_state
cat .deia/hive/schedule.json | grep -A 10 pipeline_state

# Run scheduler tests
cd hivenode && python -m pytest tests/scheduler/ -v -k state
```
