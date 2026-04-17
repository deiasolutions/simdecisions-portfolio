# BRIEFING: Full Integration Test Verification After Rebuild

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0.85
**Model:** Sonnet

---

## Objective

Run the complete hivenode and browser test suites to verify all 16 rebuild tasks (R01-R12 + TASK-147, TASK-148, TASK-159, TASK-160) restored functionality without cross-task regressions.

---

## Context

The project underwent a rebuild sequence (R01-R12) to restore DES routes, RAG indexer components, shell CSS variables, and several ported features. Following this, four additional tasks (147, 148, 159, 160) were completed for animation tests, color fixes, and entity archetypes.

All rebuild tasks completed individually with passing tests. Now we need full integration verification to catch any cross-module regressions or import chain issues that weren't visible in isolated task testing.

---

## Spec Source

`.deia/hive/queue/2026-03-15-2320-SPEC-rebuild-R13-full-integration-verify.md`

---

## Task File to Create

Write ONE task file:
- `.deia/hive/tasks/2026-03-15-TASK-R13-full-integration-verify.md`

---

## Deliverables Required

The task must deliver:

1. **Full hivenode test run**
   - Command: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/ -v`
   - Expected: All tests pass (baseline: 969+)
   - Capture: Full output with pass/fail counts by module

2. **Full browser test run**
   - Command: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run`
   - Expected: All tests pass (baseline: 1122+)
   - Capture: Full output with pass/fail counts by file

3. **Import verification**
   - No import errors across any module
   - All modules load cleanly

4. **Regression documentation**
   - Any failures documented with:
     - Module affected
     - Error message
     - Root cause if identifiable
     - Fix recommendations

5. **Final report**
   - Pass/fail counts by module
   - Comparison to baseline (969 hivenode, 1122 browser)
   - Green light for commit OR list of blocking issues

---

## Test Baselines

From memory (2026-03-14 state):
- **Hivenode:** 969 tests passing (includes 248 PHASE-IR tests)
- **Browser:** 1122 tests passing (87 files, 1 skipped)
- **Known skips:** 1 test (acceptable)

---

## Constraints

- **No code changes.** This is a verification-only task. Run tests, document results.
- **TDD exception:** This is pure testing, no implementation.
- **Response file mandatory:** All 8 sections required.
- **Model:** Sonnet (for comprehensive test analysis)

---

## Files to Reference

The bee should NOT read all test files. The bee should:
1. Run the two test commands
2. Parse the output
3. Report results

---

## Acceptance Criteria (copy to task)

- [ ] `python -m pytest tests/hivenode/ -v` — all tests pass (target: 969+)
- [ ] `cd browser && npx vitest run` — all tests pass (target: 1122+)
- [ ] No import errors across any module
- [ ] Any regressions documented and fix recommendations provided
- [ ] Final pass/fail counts reported by module

---

## Notes for Q33N

- This is a **verification task**, not an implementation task.
- The bee will run tests, parse output, and write a comprehensive report.
- If any tests fail, the bee documents the failures but does NOT fix them (that would be a follow-up fix task).
- If failures are found, you (Q33N) will need to create fix tasks after this verification completes.

---

## Expected Output from Bee

Response file in `.deia/hive/responses/` with:
- Full test output summaries for both suites
- Pass/fail counts
- Any error messages or tracebacks
- Comparison to baseline
- Green light status OR list of blocking issues

---

**Q33N: Write the task file and return for my review. Do NOT dispatch yet.**
