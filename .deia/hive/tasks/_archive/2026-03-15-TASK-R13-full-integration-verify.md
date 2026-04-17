# TASK-R13: Full Integration Test Verification

## Objective
Run the complete hivenode and browser test suites to verify all 16 rebuild tasks (R01-R12, TASK-147, 148, 159, 160) restored functionality without cross-task regressions. **This is a verification-only task — NO code changes allowed.**

## Context
The project underwent a rebuild sequence (R01-R12) to restore DES routes, RAG indexer components, shell CSS variables, and several ported features. Following this, four additional tasks (147, 148, 159, 160) were completed for animation tests, color fixes, and entity archetypes.

All rebuild tasks completed individually with passing tests. Now we need full integration verification to catch any cross-module regressions or import chain issues that weren't visible in isolated task testing.

**This task runs AFTER all 16 rebuild tasks complete.**

## Files to Read First
None required. This is a test execution and reporting task.

## Deliverables

### 1. Run Full Hivenode Test Suite
- [ ] Run: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/ -v`
- [ ] Document pass/fail counts by module (routes, rag, efemera, shell, phase_ir, etc.)
- [ ] Capture full output with error messages for any failures
- [ ] Target: **969+ tests passing** (pre-reset baseline)

### 2. Run Full Browser Test Suite
- [ ] Run: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run`
- [ ] Document pass/fail counts by file
- [ ] Capture full output with error messages for any failures
- [ ] Target: **1122+ tests passing** (pre-reset baseline)

### 3. Import Verification
- [ ] Confirm no import errors across any module
- [ ] All test files load cleanly

### 4. Regression Documentation (if failures found)
- [ ] For each failing test, document:
  - Module/file affected
  - Full error message and traceback
  - Root cause if identifiable from error message
  - Which rebuild task likely introduced the issue
  - Recommended fix (but DO NOT implement the fix)

### 5. Final Report
- [ ] Pass/fail counts by module
- [ ] Comparison to baseline (969 hivenode, 1122 browser)
- [ ] **If all tests pass:** Green light for commit
- [ ] **If any tests fail:** List of blocking issues with fix recommendations (for follow-up tasks)

## Test Requirements
- [ ] Hivenode test suite executed fully
- [ ] Browser test suite executed fully
- [ ] All import errors documented (if any)
- [ ] All test failures documented with full tracebacks (if any)

## Constraints
- **NO CODE CHANGES.** This is a verification-only task. Run tests, parse output, document results.
- **Do NOT fix anything.** If failures are found, document them for follow-up fix tasks.
- **Do NOT skip tests.** Run the full suites.
- **TDD exception:** This is pure testing/verification, no implementation.
- **Response file mandatory:** All 8 sections required.

## Test Baselines (from 2026-03-14)
- **Hivenode:** 969 tests passing (includes 248 PHASE-IR tests)
- **Browser:** 1122 tests passing (87 files, 1 skipped)
- **Known skips:** 1 test (acceptable)

## Acceptance Criteria
- [ ] `python -m pytest tests/hivenode/ -v` executed and output captured
- [ ] `cd browser && npx vitest run` executed and output captured
- [ ] Pass/fail counts documented by module
- [ ] Target: 969+ hivenode tests passing
- [ ] Target: 1122+ browser tests passing
- [ ] No import errors across any module (or documented if found)
- [ ] Any test failures documented with full error messages and tracebacks
- [ ] Final status: GREEN LIGHT (all pass) OR BLOCKING ISSUES LIST (with fix recommendations)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-R13-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — should be "None (verification only)" unless response file itself
3. **What Was Done** — bullet list of test commands executed, not fixes
4. **Test Results** — full test output summary with pass/fail counts by module
5. **Build Verification** — pytest + vitest exit codes, summary lines, last 10 lines of each output
6. **Acceptance Criteria** — copy from above, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** —
   - If all pass: "No issues. Green light for commit."
   - If failures: Full list of blocking issues with module, error, traceback, and recommended fix

DO NOT skip any section.
