# TASK-BUG-045-C: Wrap fix cycle file I/O in exception handlers

## Objective
Add exception handling to `generate_fix_spec()` and `generate_q33n_fix_spec()` in fix_cycle.py so that file write failures don't crash the queue runner.

## Context
`fix_cycle.py` contains two functions that generate fix specs by writing markdown files to the queue directory:
- `generate_fix_spec()` (line 49): writes fix specs for bee failures
- `generate_q33n_fix_spec()` (line 117): writes fix specs for Q33N (regression fixes)

Both functions call `Path.write_text()` (lines 112, 188) which can fail with:
- OSError (disk full, permission denied)
- FileNotFoundError (parent directory deleted)
- Other I/O errors

Currently, these exceptions propagate up to the caller (_handle_spec_result) and can kill the queue. This task wraps the write operations in try/except, logs errors, and returns None on failure (instead of a Path).

**Caller contract:** `_handle_spec_result()` checks if the returned path is None and handles it gracefully (moves original spec to _needs_review/).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (entire file, 191 lines)

## Deliverables
- [ ] `generate_fix_spec()` write operation wrapped in try/except
- [ ] `generate_q33n_fix_spec()` write operation wrapped in try/except
- [ ] On exception: log `[QUEUE] ERROR:` + traceback + spec ID
- [ ] On exception: return None (instead of Path)
- [ ] Update docstrings to document None return on failure
- [ ] Test: mock Path.write_text to raise OSError, verify None returned
- [ ] Test: mock Path.write_text to raise PermissionError, verify None returned

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass (if any exist for fix_cycle.py)
- [ ] New test file: `.deia/hive/scripts/queue/tests/test_fix_cycle_resilience.py`
- [ ] New test: generate_fix_spec with disk full (OSError), verify None returned
- [ ] New test: generate_q33n_fix_spec with permission denied, verify None returned
- [ ] Edge case: verify error message includes spec ID and operation context
- [ ] All tests pass: `python -m pytest .deia/hive/scripts/queue/tests/ -v`

## Constraints
- No file over 500 lines
- Do not change fix spec content generation logic
- Only wrap file I/O operations in try/except
- Log everything with `[QUEUE] ERROR:` prefix
- Use `import traceback; traceback.print_exc()` for full stack traces
- TDD: Write tests first, then implementation
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-045-C-RESPONSE.md`

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
