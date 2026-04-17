# SPEC-WAVE0-D: BAT End-to-End Validation

## Priority
P0

## Model Assignment
sonnet

## Depends On
SPEC-WAVE0-C-scheduler-state-machine

## Intent

Validate the complete DDD pipeline end to end. Run a test task through the full cycle: queue -> running -> code_complete -> qa_review -> q33n_review -> done. Confirm every state transition works and every artifact is produced correctly.

## Files to Read First

.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md
.deia/docs/impl/SCHEMA.md
.deia/hive/templates/QA-BEE-TEMPLATE.md
hivenode/scheduler/scheduler_daemon.py
.deia/hive/scripts/queue/run_queue.py

## Work Required

### 1. Create a test task

Write a minimal test task: TASK-DDD-SMOKE-TEST.md
Objective: create a single file test.txt containing "DDD pipeline test" in .deia/docs/test/smoke/

This is the simplest possible task -- one file, no code changes, trivially verifiable. Purpose is to exercise the pipeline, not produce value.

### 2. Run the task through the pipeline manually

Execute the following sequence and verify each step:

Step 1: Place TASK-DDD-SMOKE-TEST.md in .deia/hive/queue/
Step 2: Dispatch a Haiku bee to execute it
Step 3: Verify: test.txt created, IMPL-DDD-SMOKE-TEST.md produced
Step 4: Verify: task moved to _code_complete/
Step 5: Verify: qa_review_needed event written to qa_review_log.jsonl
Step 6: Manually dispatch QA bee with QA-BEE-TEMPLATE.md
Step 7: Verify: QA recommendation written to qa_review_log.jsonl
Step 8: Simulate Q33N approval: move task to _done/
Step 9: Verify: scheduler reads _done/ count correctly in next cycle

### 3. Verify IMPL doc schema compliance

Read the IMPL doc produced in Step 3. Verify:
- All required frontmatter fields present
- All required sections present (Summary, Deltas, Files, Decisions, Known Issues, Verification)
- Three currencies fields present (even if estimated)
- parent_spec field points to correct SPEC

### 4. Report

Document what worked, what failed, what needs fixing before main build.

## Acceptance Criteria

- [ ] Test task completes full pipeline cycle without manual intervention beyond the Q33N approval step
- [ ] IMPL doc produced and schema-compliant
- [ ] qa_review_log.jsonl contains both the dispatch event and QA recommendation
- [ ] Task appears in _done/ after simulated Q33N approval
- [ ] Scheduler reads pipeline_state correctly after cycle completes
- [ ] No existing tests broken by WAVE0-A, B, C changes

## GO / NO-GO Gate

If this task produces a GO verdict: dispatch tonight's main build.
If NO-GO: fix blocking issues before main build dispatches.

Document the GO/NO-GO verdict explicitly at the top of the response file.

## Constraints

- No git operations
- No production code changes (smoke test only)
- 8-section response file on completion
- Response file must begin with GO or NO-GO on line 1

## Smoke Test

After completion:
```bash
# Verify all pipeline artifacts exist
ls -la .deia/docs/test/smoke/test.txt
ls -la .deia/docs/impl/IMPL-DDD-SMOKE-TEST.md
ls -la .deia/hive/_done/TASK-DDD-SMOKE-TEST.md

# Check qa_review_log has both entries
cat .deia/logs/qa_review_log.jsonl | wc -l  # should be >= 2

# Verify scheduler recognized the transition
tail -1 .deia/hive/schedule_log.jsonl | grep pipeline_state
```
