# TASK-166: Add Build Verification Gate

**Priority:** P0.85
**Model:** haiku
**Assigned:** 2026-03-15

---

## Objective

Implement build verification gate that runs AFTER spec validation, BEFORE baseline capture, catching Python syntax errors and TypeScript type errors early with graceful degradation for missing dependencies.

---

## Context

The queue runner currently does not verify build integrity before dispatching bees, leading to:
- Bees failing on syntax errors that existed before they started
- TypeScript type errors blocking bee work
- No clear signal whether repo is in good state before dispatch

This task adds the second quality gate from Process 13: **build verification**.

The build checker runs in `spec_processor.py` AFTER `validate_spec_format()` (TASK-165), BEFORE `_capture_baseline()`, BEFORE `dispatch.py`.

Flow sequence:
```
spec file
  → validate_spec_format() [TASK-165]
  → run_build_check() [NEW — this task]
  → _capture_baseline() [EXISTING]
  → dispatch.py (calls bee)
  → _run_verification() [EXISTING]
```

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (current processor logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-1519-SPEC-w2-01-process13-quality-gates.md` (the source spec)

---

## Deliverables

- [ ] New module: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\build_checker.py` (~200 lines)
  - Function: `run_build_check() -> tuple[bool, str]`
    - Returns: `(True, "")` if valid, `(False, error_message)` if build fails
  - Python compile check (mandatory):
    - Run: `python -m py_compile hivenode/__init__.py`
    - Run: `python -m py_compile engine/__init__.py`
    - If errors: return `(False, error_msg)` with syntax details
  - TypeScript type-check (optional, graceful degradation):
    - Check if `npm` is installed (run `npm --version`)
    - If npm missing: log warning, return `(True, "")`
    - Check if `browser/package.json` has `type-check` script
    - If script missing: log warning, return `(True, "")`
    - Run: `cd browser && npm run type-check`
    - If type errors: return `(False, error_msg)` with type error details
    - If success: return `(True, "")`

- [ ] Update: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (~10 lines)
  - Import `run_build_check` from `build_checker`
  - Call `run_build_check()` AFTER `validate_spec_format()`, BEFORE `_capture_baseline()`
  - If build check fails: set `status=NEEDS_DAVE`, `error_msg=<build error>`, skip dispatch

- [ ] New tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_build_checker.py` (~250 lines)
  - 8 tests minimum (see Test Requirements section)

---

## Test Requirements

Write tests FIRST (TDD). All tests must pass.

Required tests (8 minimum):

1. **test_python_compile_valid**
   - Clean Python files (no syntax errors)
   - Expected: `(True, "")`

2. **test_python_syntax_error_fails**
   - Temporarily inject syntax error into a test Python file
   - Expected: `(False, error_msg)` with syntax details

3. **test_typescript_type_check_valid**
   - TypeScript files with no type errors (requires npm + type-check script)
   - Expected: `(True, "")`

4. **test_typescript_type_errors_fail**
   - Mock `npm run type-check` to return type errors
   - Expected: `(False, error_msg)` with type error details

5. **test_npm_not_installed_graceful_degradation**
   - Mock `npm --version` to raise `FileNotFoundError`
   - Expected: `(True, "")` + warning logged to console

6. **test_type_check_script_missing_graceful_degradation**
   - Mock `package.json` to have no `type-check` script
   - Expected: `(True, "")` + warning logged to console

7. **test_integration_build_check_before_baseline**
   - Use real spec_processor workflow
   - Mock `run_build_check()` to return `(False, "Python syntax error")`
   - Call `process_spec()`
   - Expected: status=NEEDS_DAVE, error_msg includes build error, `_capture_baseline()` NOT called

8. **test_integration_build_failure_skips_dispatch**
   - Use real spec_processor workflow
   - Mock `run_build_check()` to return `(False, "Build failed")`
   - Call `process_spec()`
   - Expected: status=NEEDS_DAVE, dispatch.py NOT called

---

## Constraints

- No file over 500 lines
- No stubs — every function fully implemented
- TDD — tests first, then implementation
- No hardcoded colors (N/A for Python)
- Use `subprocess.run()` for build commands, capture stderr
- Use mocks in tests to avoid real build dependency

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-166-RESPONSE.md`

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

---

## Smoke Test

After implementation, run:

```bash
# Run build checker tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest .deia/hive/scripts/queue/tests/test_build_checker.py -v

# Run integration tests
python -m pytest .deia/hive/scripts/queue/tests/test_build_checker.py::test_integration_build_check_before_baseline -v
python -m pytest .deia/hive/scripts/queue/tests/test_build_checker.py::test_integration_build_failure_skips_dispatch -v

# Verify all queue tests still pass
python -m pytest .deia/hive/scripts/queue/tests/ -v
```

Expected: 8 tests pass (minimum), 0 failures.

---

**Status:** READY
**Assigned to:** BEE-HAIKU
**Dispatched by:** Q33N
