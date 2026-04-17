# TASK-BUG-045-B: Wrap _handle_spec_result() in exception handler

## Objective
Add exception handling inside `_handle_spec_result()` to isolate individual spec result processing failures so that one bad spec result doesn't kill the entire queue.

## Context
`_handle_spec_result()` at line 291 in run_queue.py processes individual spec results: moves files to _done/, generates fix specs, creates timeout resumes, etc. Currently, if file I/O fails (PermissionError, FileNotFoundError, disk full), the exception propagates up and can kill the watch loop.

This task adds exception handling to critical sections within `_handle_spec_result()`:
- File move operations (spec.path.rename)
- Fix spec generation (generate_fix_spec, generate_q33n_fix_spec)
- Timeout resume creation (_create_timeout_resume)
- Auto-commit (already has try/except, verify it's sufficient)

**Architecture:** The function has 3 main branches:
1. CLEAN status (line 328): move to _done/, auto-commit, cleanup orphans
2. TIMEOUT status (line 353): create resume spec, move original to _done/
3. NEEDS_DAVE/failure (line 411): auto-commit, generate fix spec or move to _needs_review/

Each branch contains file operations that can fail. Wrap each risky section in try/except, log the error, move the spec to _needs_review/ with error details, and return empty list (no new specs).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (lines 291-498, _handle_spec_result)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (generate_fix_spec, generate_q33n_fix_spec)

## Deliverables
- [ ] File rename operations wrapped in try/except (catch OSError)
- [ ] Fix spec generation wrapped in try/except (catch Exception)
- [ ] Timeout resume creation wrapped in try/except (catch Exception)
- [ ] On exception: log `[QUEUE] ERROR:` + traceback
- [ ] On exception: move spec to _needs_review/ with error details in filename or log
- [ ] On exception: return empty list (no new specs to queue)
- [ ] Test: mock spec.path.rename to raise PermissionError, verify spec moves to _needs_review/
- [ ] Test: mock generate_fix_spec to raise FileNotFoundError, verify graceful handling

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass
- [ ] New test: file move fails (PermissionError), verify spec → _needs_review/
- [ ] New test: fix spec generation fails, verify original spec → _needs_review/
- [ ] New test: timeout resume creation fails, verify spec → _needs_review/
- [ ] Edge case: verify error details logged with spec ID and operation context

## Constraints
- No file over 500 lines
- Do not change result handling logic
- Only add error handling around risky operations
- Log everything with `[QUEUE] ERROR:` prefix
- Use `import traceback; traceback.print_exc()` for full stack traces
- TDD: Write tests first, then implementation
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-045-B-RESPONSE.md`

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
