# SPEC-APPLY-QFIX-01: Apply Queue Runner Completion Detection Fix

## Priority
P1

## Model Assignment
haiku

## Depends On
None

## Intent
Verify and apply the code changes from SPEC-QUEUE-FIX-01 (Completion Detection). A bee already wrote the code — this spec verifies it works. The bee updated `parse_response_header()` to recognize ALREADY_COMPLETE and NO_ACTION_NEEDED statuses, and added strict SPEC-*.md filename filtering to `load_queue()`.

## Files to Read First
.deia/hive/responses/20260406-SPEC-QUEUE-FIX-01-RESPONSE.md
.deia/hive/scripts/queue/dispatch_handler.py
.deia/hive/scripts/queue/spec_parser.py
.deia/hive/scripts/queue/run_queue.py
.deia/hive/scripts/queue/test_completion_detection.py

## Acceptance Criteria
- [ ] `dispatch_handler.py` recognizes ALREADY_COMPLETE and NO_ACTION_NEEDED as success statuses
- [ ] `spec_parser.py` load_queue() only loads files starting with `SPEC-`
- [ ] `run_queue.py` contains `_is_valid_spec_filename()` helper
- [ ] All 5 tests in `test_completion_detection.py` pass
- [ ] Backward compatibility: COMPLETE status and RAW.txt format still recognized
- [ ] Non-spec files (BRIEFING-*, TASK-*, QUEUE-TEMP-*) are skipped with log message

## Constraints
- Do NOT modify any code. Verification only.
- If tests fail, document the failures in your response but do NOT attempt fixes.
- No git operations.

## Smoke Test
Run `python -m pytest .deia/hive/scripts/queue/test_completion_detection.py -v` and verify 5 tests pass.
