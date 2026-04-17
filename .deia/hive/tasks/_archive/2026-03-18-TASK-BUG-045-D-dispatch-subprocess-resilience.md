# TASK-BUG-045-D: Wrap dispatch subprocess in exception handler

## Objective
Verify and enhance exception handling in `spec_processor.py` dispatch operations to ensure subprocess failures (exit code 127, command not found, etc.) don't propagate unhandled.

## Context
`spec_processor.py` contains `process_spec()` and `process_spec_no_verify()` which call `handler.call_dispatch()` to spawn subprocess for bee dispatch. The DispatchHandler is in a separate module, but the spec_processor must handle failures gracefully.

Current code at line 180 checks `if not success:` but may not catch all subprocess-related exceptions (e.g., OSError when dispatch.py is missing, timeout exceptions, etc.).

This task:
1. Reviews existing exception handling in process_spec and process_spec_no_verify
2. Adds a broad try/except around the dispatch call if not already present
3. Ensures all subprocess failures return a SpecResult with status="NEEDS_DAVE" and descriptive error_msg
4. Logs errors with `[QUEUE] ERROR:` prefix

**Architecture:** Both functions follow same pattern:
- Lines 175-210 in process_spec: call_dispatch + result checking
- Lines 371-394 in process_spec_no_verify: same pattern

If dispatch raises an exception (not just returns success=False), it must be caught.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (lines 84-307 for process_spec, 309-442 for process_spec_no_verify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` (if it exists, to understand what exceptions call_dispatch can raise)

## Deliverables
- [ ] Wrap `handler.call_dispatch()` in try/except Exception in both functions
- [ ] On exception: log `[QUEUE] ERROR:` + traceback + spec ID
- [ ] On exception: return SpecResult(status="NEEDS_DAVE", error_msg=str(e))
- [ ] Test: mock call_dispatch to raise OSError, verify NEEDS_DAVE result
- [ ] Test: mock call_dispatch to raise subprocess.TimeoutExpired, verify NEEDS_DAVE result
- [ ] Cleanup temp file on exception (handler.cleanup_temp_file)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass: `python -m pytest .deia/hive/scripts/queue/tests/ -v`
- [ ] New test file: `.deia/hive/scripts/queue/tests/test_spec_processor_resilience.py`
- [ ] New test: call_dispatch raises OSError, verify SpecResult(NEEDS_DAVE)
- [ ] New test: call_dispatch raises Exception, verify temp file cleaned up
- [ ] Edge case: verify error message includes spec ID and exception type

## Constraints
- No file over 500 lines
- Do not change dispatch logic
- Only add exception handling around subprocess call
- Log everything with `[QUEUE] ERROR:` prefix
- Use `import traceback; traceback.print_exc()` for full stack traces
- TDD: Write tests first, then implementation
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-045-D-RESPONSE.md`

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
