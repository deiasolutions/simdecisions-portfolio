# TASK-SEC-6: Fix Windows tmp_path PermissionError in Tests

## Objective
Fix PermissionError when pytest creates `tmp_path` fixtures under Windows `%TEMP%` directory by redirecting to `~/.shiftcenter/test_tmp/`.

## Context
On Windows, pytest `tmp_path` fixtures sometimes fail with PermissionError when trying to create directories under `%TEMP%`. This is a known Windows issue. The fix is to override `tempfile.tempdir` in the root conftest.py to use a location under the user's home directory.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py`

## Deliverables
- [ ] Add to `tests/hivenode/conftest.py` (at the top, before other imports):
  ```python
  import tempfile
  import os

  if os.name == 'nt':
      _test_tmp = os.path.join(os.path.expanduser("~"), ".shiftcenter", "test_tmp")
      os.makedirs(_test_tmp, exist_ok=True)
      tempfile.tempdir = _test_tmp
  ```
- [ ] Run backend tests: `python -m pytest tests/hivenode/ -v --tb=short`
- [ ] Record pass/fail/skip counts in response file
- [ ] If any tests fail due to this change, document them

## Test Requirements
- Run full backend test suite
- Record baseline: pass/fail/skip counts
- Tests should no longer fail with PermissionError on tmp_path creation

## Constraints
- Only modify `tests/hivenode/conftest.py`
- Do NOT change test logic, only temp directory location
- This change applies only on Windows (`os.name == 'nt'`)

## Model
Haiku (simple fix, well-defined)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-6-RESPONSE.md`

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
