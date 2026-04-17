# SPEC-WAVE0-B: QA Bee Dispatch Logic + qa_review_log

## Priority
P0

## Model Assignment
sonnet

## Depends On
None

## Intent

Implement the QA bee dispatch trigger and qa_review_log output format. When a task completes, a QA bee is automatically dispatched to review the IMPL doc against the SPEC.

## Files to Read First

.deia/hive/scripts/queue/run_queue.py
.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md

## Work Required

### 1. Create QA bee dispatch trigger

In the queue-runner (run_queue.py or dispatch_handler.py), after a task completes successfully:

- Check if IMPL-{task_id}.md exists in .deia/docs/impl/
- If exists: emit a qa_review_needed event and move task to _code_complete/
- If missing: log a warning, keep task in running state with error flag "IMPL doc required but not produced"

The qa_review_needed event payload:
  {
    "event": "qa_review_needed",
    "task_id": "{task_id}",
    "spec_path": ".deia/hive/queue/{task_file}",
    "impl_path": ".deia/docs/impl/IMPL-{task_id}.md",
    "completed_at": "ISO8601",
    "build_bee": "{bee_id}"
  }

Write this event to .deia/logs/qa_review_log.jsonl (append, one JSON per line).

### 2. Create QA bee task template

Write .deia/hive/templates/QA-BEE-TEMPLATE.md:

The QA bee receives:
- Original SPEC file path
- IMPL doc path
- Code diff summary (files created/modified from IMPL frontmatter)

The QA bee checks:
1. Frontmatter complete and accurate (files match actual changes)
2. Deltas from spec documented honestly
3. Key decisions explained with rationale
4. Three currencies recorded (clock, coin, carbon, tokens)
5. Verification instructions present

The QA bee writes its recommendation to qa_review_log.jsonl:
  {
    "task_id": "{task_id}",
    "qa_bee": "{bee_id}",
    "model": "{model}",
    "timestamp": "ISO8601",
    "recommendation": "approve" | "revise",
    "issues": [
      {"section": "...", "issue": "...", "suggested": "..."}
    ],
    "notes": "..."
  }

### 3. Create .deia/logs/ directory and initialize qa_review_log.jsonl

Create the logs directory if it does not exist. Initialize qa_review_log.jsonl as an empty file.

## Acceptance Criteria

- [ ] queue-runner emits qa_review_needed event on task completion
- [ ] Task moves to _code_complete/ when IMPL doc exists
- [ ] Warning logged when IMPL doc missing (task not silently lost)
- [ ] qa_review_log.jsonl created and writable
- [ ] QA-BEE-TEMPLATE.md exists with complete instructions
- [ ] Existing queue-runner behavior unchanged for tasks without IMPL docs
- [ ] Tests cover: IMPL present (happy path), IMPL missing (warning path)

## Constraints

- Do NOT break existing queue-runner behavior
- Add IMPL check as optional gate -- tasks without IMPL docs warn but complete
- No file over 500 lines
- No stubs
- No git operations
- 8-section response file on completion

## Smoke Test

After completion:
```bash
# Verify logs directory and qa_review_log exist
ls -la .deia/logs/qa_review_log.jsonl

# Verify QA template exists
cat .deia/hive/templates/QA-BEE-TEMPLATE.md | head -30

# Run queue-runner tests
cd hivenode && python -m pytest tests/queue/ -v -k qa
```
