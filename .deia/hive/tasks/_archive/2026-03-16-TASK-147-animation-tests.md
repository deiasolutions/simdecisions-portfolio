# TASK-147: Port 17-test animation test suite

## Objective

Port the animation test suite from the platform repo to ShiftCenter. The test file should be created at the correct location in the primitives/canvas/animation layer.

---

## Context

### Test Source Location
Platform repo test file:
- **Path:** `C:/Users/davee/OneDrive/Documents/GitHub/platform/simdecisions-2/src/components/canvas/animation/__tests__/animation.test.tsx`
- **Content:** 18 tests (15 active, 3 skipped as pre-existing timing issues)
- **Test suites:** TokenAnimation (2), NodePulse (2), QueueBadge (3), ResourceBar (2), CheckpointFlash (1 skipped), SimClock (2), useAnimationFrame (2), hardcoded colors check (1)

### Target Location
ShiftCenter test file should be created at:
- **Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\animation\__tests__\animation.test.tsx`

### Component Status
All animation components and hooks are **already ported** in ShiftCenter:
- **Components:** TokenAnimation.tsx, NodePulse.tsx, QueueBadge.tsx, ResourceBar.tsx, CheckpointFlash.tsx, SimClock.tsx
- **Hook:** useAnimationFrame.ts
- **Location:** `browser/src/primitives/canvas/animation/`

All imports in the test file will resolve correctly.

---

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/platform/simdecisions-2/src/components/canvas/animation/__tests__/animation.test.tsx` — Source test file to port
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\animation\TokenAnimation.tsx` — To verify imports
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\animation\useAnimationFrame.ts` — To verify hook interface

---

## Deliverables

- [x] Test file created at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\animation\__tests__\animation.test.tsx`
- [x] All 18 tests ported (3 marked as `.skip` for pre-existing timing issues, as in source)
- [x] All imports resolve correctly
- [x] All tests pass: `cd browser && npx vitest run browser/src/primitives/canvas/animation/__tests__/animation.test.tsx`
- [x] No regressions in other browser tests: `cd browser && npx vitest run` (must remain at 1122 passed, 0 failures)

---

## Test Requirements

- [x] Tests written FIRST (this is a port — tests ARE the deliverable)
- [x] All 18 tests pass (15 active + 3 skipped)
- [x] Edge cases covered:
  - TokenAnimation: active vs inactive states
  - NodePulse: visibility toggle on isActive
  - QueueBadge: edge value (0, 5, 1500)
  - ResourceBar: utilization color change at 0.8 threshold
  - CheckpointFlash: animation completion callback (skipped — timing issue)
  - SimClock: precision formatting and pause state
  - useAnimationFrame: enable/disable toggle
  - Hardcoded colors: constraint verification

---

## Constraints

- No file over 500 lines (this test file will be ~227 lines — well under limit)
- CSS: var(--sd-*) only (test checks for var(--sd-red) in ResourceBar)
- No stubs — every test is a real assertion
- Do not modify existing animation component files

---

## Notes

### Pre-existing Skipped Tests
The platform source has 3 tests marked `.skip`:
1. NodePulse: "applies pulse animation when isActive=true" (line 53)
2. CheckpointFlash: "fires onAnimationComplete callback after animation" (line 120)
3. useAnimationFrame: "calls callback at ~60fps when enabled" (line 167)

These are marked as "Pre-existing animation timing issue" in the source. Port them as-is with the `.skip` prefix.

### Color Constraint Validation
The test at line 213-226 validates the "No hardcoded colors" constraint. It's a placeholder test that trusts manual review. Port it as-is.

---

## Response Requirements — MANDATORY

When you finish, write a response file at:
`.deia/hive/responses/20260316-TASK-147-RESPONSE.md`

The response MUST contain all 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created (absolute paths)
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test file run, pass/fail counts (must show all 15 active tests passing)
5. **Build Verification** — browser test suite output (must remain 1122 passed, 0 failures)
6. **Acceptance Criteria** — copy from task, mark [x] done or [ ] not done
7. **Clock / Cost / Carbon** — all three metrics
8. **Issues / Follow-ups** — any blockers, edge cases, or recommended next tasks

DO NOT skip any section.
