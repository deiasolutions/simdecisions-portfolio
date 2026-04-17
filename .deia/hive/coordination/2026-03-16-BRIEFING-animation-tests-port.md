# BRIEFING: Port Animation Test Suite

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Spec:** `.deia/hive/queue/2026-03-15-2312-SPEC-task-147-animation-tests.md`
**Model Assignment:** haiku

---

## Objective

Port the 17-test animation test suite from platform repo. The spec notes that a test file may already exist at the wrong location — your job is to verify, relocate if needed, and ensure all 17 tests pass.

---

## Context

### From Spec
- **Priority:** P0.65
- **Task File:** `.deia/hive/tasks/2026-03-15-TASK-147-animation-tests.md`
- **Acceptance Criteria:**
  - [ ] Animation test file at correct location under `flow-designer/__tests__/`
  - [ ] All 17 animation tests pass
  - [ ] No regressions in other browser tests

### Source Location (Platform)
The platform repo is located at `C:\Users\davee\OneDrive\Documents\GitHub\platform\`. Animation tests are likely under:
- `platform/simdecisions-2/src/__tests__/` (frontend test structure)
- Or `platform/efemera/src/flow_designer/__tests__/` (if exists)

### Target Location (ShiftCenter)
Animation test file should land at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\flow-designer\__tests__\animation.test.ts`

(Note: verify whether `flow-designer/` exists in `browser/src/`. May be under different primitive name.)

### Key Constraints
- **17 tests** must be present and passing
- Port the tests AS-IS unless dependencies are missing
- If dependencies (e.g., test utilities, mocks) are missing, flag them in the task file
- Follow TDD: tests first, then implementation (but in this case, tests ARE the implementation)
- All browser tests must remain green: `cd browser && npx vitest run` (currently 1122 passing, 0 failures)

---

## Your Job

1. **Search for existing animation test file** in `browser/src/` (may be misplaced)
2. **Read platform source** to locate the 17-test animation suite
3. **Write task file** for a BEE to:
   - Port or relocate the animation test file
   - Verify all 17 tests pass
   - Check for regressions
4. **Return the task file to Q33NR for review**

Do NOT dispatch the bee yet. Return task file first.

---

## Response Format

When you return, include:
- Path to task file written
- Summary of what the bee will do
- Any blockers or missing dependencies you found
- Estimated test count (should be 17)

---

## Notes

- The spec says "test file may already exist at wrong location" — investigate this first before porting from platform
- If animation tests are NOT in platform, search browser/src/ for any `animation.test.ts` or similar
- If animation logic is NOT in ShiftCenter yet, flag NEEDS_DAVE (cannot port tests for nonexistent code)
