# TASK-165: Add Spec Format Validation Gate

**Priority:** P0.85
**Model:** haiku
**Assigned:** 2026-03-15

---

## Objective

Implement spec format validation gate that runs BEFORE dispatch, catching malformed spec files (invalid priority/model, missing sections) early and providing clear error messages to prevent downstream failures.

---

## Context

The queue runner currently dispatches spec files without validation, leading to:
- Invalid priorities (P4, P99) discovered mid-execution
- Invalid models (gpt4, claude) causing dispatch failures
- Missing acceptance criteria causing bee confusion
- Empty smoke test sections leaving no verification path

This task adds the first quality gate from Process 13: **spec format validation**.

The validator runs in `spec_processor.py` AFTER `validate_spec_format()`, BEFORE `_capture_baseline()`, BEFORE `dispatch.py`.

Flow sequence:
```
spec file
  → validate_spec_format() [NEW — this task]
  → run_build_check() [TASK-166, separate]
  → _capture_baseline() [EXISTING]
  → dispatch.py (calls bee)
  → _run_verification() [EXISTING]
```

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (current processor logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` (spec parsing logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-1519-SPEC-w2-01-process13-quality-gates.md` (the source spec)

---

## Deliverables

- [ ] New module: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_validator.py` (~150 lines)
  - Function: `validate_spec_format(spec_path: str) -> tuple[bool, str]`
    - Returns: `(True, "")` if valid, `(False, error_message)` if invalid
  - Validation rules (FAIL):
    - Priority not in `[P0, P0.5, P0.85, P1, P2, P3]`
    - Model not in `[haiku, sonnet, opus]`
    - Objective section empty or missing
    - Acceptance Criteria section empty (no checkboxes)
    - Smoke Test section empty (no commands)
  - Validation rules (WARN):
    - Constraints section missing → log to console, return `(True, "")`
  - Validation rules (SKIP):
    - Hold section present → return `(True, "")` (queue runner handles this separately)

- [ ] Update: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (~5 lines)
  - Import `validate_spec_format` from `spec_validator`
  - Call `validate_spec_format(spec_path)` BEFORE `_capture_baseline()`
  - If validation fails: set `status=NEEDS_DAVE`, `error_msg=<validation error>`, skip dispatch

- [ ] New tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_spec_validator.py` (~200 lines)
  - 8 tests minimum (see Test Requirements section)

---

## Test Requirements

Write tests FIRST (TDD). All tests must pass.

Required tests (8 minimum):

1. **test_valid_spec_all_sections_present**
   - Spec with priority=P1, model=haiku, objective, acceptance criteria (3 checkboxes), smoke test (2 commands), constraints
   - Expected: `(True, "")`

2. **test_missing_objective_fails**
   - Spec with empty or missing objective section
   - Expected: `(False, "Objective section is empty or missing")`

3. **test_invalid_priority_fails**
   - Spec with priority=P4 (invalid)
   - Expected: `(False, "Priority must be one of [P0, P0.5, P0.85, P1, P2, P3], got P4")`

4. **test_invalid_model_fails**
   - Spec with model=gpt4 (invalid)
   - Expected: `(False, "Model must be one of [haiku, sonnet, opus], got gpt4")`

5. **test_empty_acceptance_criteria_fails**
   - Spec with "## Acceptance Criteria" header but no checkboxes
   - Expected: `(False, "Acceptance Criteria section is empty (no checkboxes found)")`

6. **test_empty_smoke_test_fails**
   - Spec with "## Smoke Test" header but no commands (no code blocks or bullet points)
   - Expected: `(False, "Smoke Test section is empty (no commands found)")`

7. **test_missing_constraints_warns_but_passes**
   - Spec with all required sections, but no Constraints section
   - Expected: `(True, "")` + warning logged to console

8. **test_integration_spec_processor_calls_validator_before_dispatch**
   - Use real spec_processor workflow
   - Create invalid spec (missing objective)
   - Call `process_spec()`
   - Expected: status=NEEDS_DAVE, error_msg includes validation failure, dispatch.py NOT called

---

## Constraints

- No file over 500 lines
- No stubs — every function fully implemented
- TDD — tests first, then implementation
- No hardcoded colors (N/A for Python)
- No subprocess calls to dispatch.py in the validator itself (only in integration test)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-165-RESPONSE.md`

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
# Run validator tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest .deia/hive/scripts/queue/tests/test_spec_validator.py -v

# Run integration test
python -m pytest .deia/hive/scripts/queue/tests/test_spec_validator.py::test_integration_spec_processor_calls_validator_before_dispatch -v

# Verify all queue tests still pass
python -m pytest .deia/hive/scripts/queue/tests/ -v
```

Expected: 8 tests pass (minimum), 0 failures.

---

**Status:** READY
**Assigned to:** BEE-HAIKU
**Dispatched by:** Q33N
