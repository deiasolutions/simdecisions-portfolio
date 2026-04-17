# TASK-FIX-224: Fix Role Detection Logic in dispatch_handler.py

## Objective
Fix the role detection logic in `dispatch_handler.py` so that spec files with implementation deliverables are dispatched with `role=bee` instead of incorrectly defaulting to `role=regent`.

## Context
TASK-224 (Directory State Machine) failed because it was dispatched with `role=regent` when it should have been `role=bee`. The spec contains implementation work (create directories, write code, write tests), not coordination work.

The current `_detect_role_from_spec()` function in `dispatch_handler.py` (line 31-41) only looks for an optional `## Role Override` section and defaults to "regent" if not found. This is incorrect — it should detect the role based on the **spec content type**:

- Specs with implementation deliverables (code, tests, files) → **role=bee**
- Specs with coordination directives (write briefings, dispatch tasks, review) → **role=queen**
- Specs asking for high-level planning/architecture → **role=regent**

From the failure response (20260317-1500-BEE-SONNET-QUEUE-TEMP-2026-03-16-SPEC-TASK-224-DIRECTORY-STATE-MACHINE-RAW.txt):
> "This task appears to be addressed directly to me as if I'm a BEE worker, not as Q33NR. The task includes implementation deliverables like 'Create `_active/`, `_failed/`, etc.' and 'Implement pickup logic' and 'Create tests.'"

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` (lines 31-41 and 106-112)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_done\2026-03-16-SPEC-TASK-224-directory-state-machine.md` (example bee task)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\HIVE.md` (role definitions)

## Deliverables

### 1. Update `_detect_role_from_spec()` Function
- [ ] Enhance role detection logic to analyze spec content, not just look for optional override
- [ ] If `## Role Override` section exists, use it (backward compat)
- [ ] Otherwise, detect role from content patterns:
  - **role=bee** if spec contains:
    - `## Deliverables` or `## Files to Create` or `## Files to Modify` sections
    - Keywords: "implement", "create tests", "write code", "TDD", "test files"
    - Pattern: `- [ ]` checkbox items with technical deliverables
  - **role=queen** if spec contains:
    - Keywords: "write briefing", "dispatch", "coordinate", "review task files"
    - Sections: `## Task Breakdown`, `## Coordination Plan`
  - **role=regent** (default) for:
    - High-level planning, architecture decisions, specs asking for breakdown
    - Fallback if no clear pattern detected

### 2. Write Tests
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_handler.py`
- [ ] Test `_detect_role_from_spec()` with various inputs:
  - Spec with `## Role Override` → returns overridden role
  - Spec with implementation deliverables → returns "bee"
  - Spec with coordination keywords → returns "queen"
  - Spec with high-level architecture → returns "regent"
  - Empty spec → returns "regent" (safe default)
  - TASK-224 spec content → returns "bee" (regression test)
- [ ] Minimum 10 tests covering all branches

### 3. Re-dispatch TASK-224 with Correct Role
- [ ] After fixing the detection logic, verify TASK-224 would now be detected as `role=bee`
- [ ] Write a brief validation script or test that proves TASK-224 spec → "bee"
- [ ] Do NOT actually re-dispatch TASK-224 (Q33N will handle that after this fix is approved)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Spec with both override and content patterns (override wins)
  - Spec with multiple role keywords (strongest signal wins)
  - Spec with mixed content (use primary section to decide)
  - Very short spec (1-2 lines)
  - Very long spec (500+ lines)

## Constraints
- No file over 500 lines
- Do NOT modify `call_dispatch()` logic (lines 79-192) — only `_detect_role_from_spec()`
- Do NOT change the function signature of `_detect_role_from_spec(spec_content: str) -> str`
- Preserve backward compatibility with `## Role Override` sections
- Follow TDD: write tests first, then implementation

## Acceptance Criteria
- [ ] `_detect_role_from_spec()` correctly identifies bee tasks from content
- [ ] All tests pass (minimum 10 tests)
- [ ] TASK-224 spec content is correctly detected as `role=bee` (regression test passes)
- [ ] No regressions on existing queue processing
- [ ] Response file written with all 8 sections

## Priority
P0 (blocks TASK-224 and other queued specs)

## Model Assignment
haiku — this is a targeted bug fix with clear requirements

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-FIX-224-RESPONSE.md`

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
