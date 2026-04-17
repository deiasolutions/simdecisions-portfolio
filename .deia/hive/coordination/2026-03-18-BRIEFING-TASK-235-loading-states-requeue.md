# BRIEFING: Wire PaneLoader into AppFrame (TASK-235 Re-Queue)

**To:** Q33N (Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18
**Spec:** `.deia/hive/queue/2026-03-18-SPEC-REQUEUE-TASK235-loading-states.md`

---

## Objective

Wire the existing PaneLoader component into AppFrame.tsx so panes show a loading spinner while their applet content is mounting.

---

## Context

### What Already Works
- `browser/src/shell/components/PaneLoader.tsx` — 57-line working spinner component (/, -, \, |)
- `browser/src/shell/components/__tests__/PaneLoader.test.tsx` — 8 passing tests
- `browser/src/shell/components/__tests__/AppFrame.loading.test.tsx` — 8 tests written but FAILING because AppFrame has no loading logic

### What's Missing
AppFrame.tsx currently has ZERO loading state logic. It renders apps immediately or shows "Unknown app type" error. The tests expect:
1. 100ms delay before showing loader (prevents flash on fast loads)
2. Loader shows when appType is set but component hasn't mounted
3. Loader hides when component renders
4. Loader never shows for 'empty' appType
5. Loading state resets when appType changes

### Why Re-Queued
Original bee (Sonnet) created PaneLoader and wrote tests, but the AppFrame.tsx modifications never landed. PaneLoader exists in the codebase but is never imported or used.

---

## Files to Read

**Read these first:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx` — current state (NO loading logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneLoader.tsx` — existing component (works, don't recreate)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\AppFrame.loading.test.tsx` — tests that expect loading behavior

---

## Deliverables

The bee must:
- [ ] Modify AppFrame.tsx to import and use PaneLoader
- [ ] Add loading state with 100ms delay before showing (prevents flash)
- [ ] Show PaneLoader when appType is set but component hasn't mounted
- [ ] Hide PaneLoader when component renders or when appType is 'empty'
- [ ] Reset loading state when appType changes
- [ ] Make all 8 tests in AppFrame.loading.test.tsx pass
- [ ] Keep all 8 tests in PaneLoader.test.tsx passing
- [ ] No regressions in other shell/ tests

---

## Test Requirements

**Target test files:**
```bash
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneLoader.test.tsx
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/AppFrame.loading.test.tsx
cd browser && npx vitest run --reporter=verbose src/shell/
```

Expected:
- PaneLoader.test.tsx: 8/8 pass
- AppFrame.loading.test.tsx: 8/8 pass (currently FAILING)
- No regressions in other shell/ tests

---

## Constraints

- **No file over 500 lines** (AppFrame.tsx currently 59 lines, should stay under 150)
- **CSS: var(--sd-*) only** (PaneLoader already compliant)
- **No stubs** — full implementation required
- **MUST modify AppFrame.tsx** — that's the entire point of this re-queue
- **Do NOT recreate PaneLoader.tsx** — it already exists and works

---

## Model Assignment

**sonnet** — Frontend logic with timing behavior requires careful state management.

---

## Priority

**P1** — Re-queue to fix incomplete work from previous task.

---

## Response File Requirements

Bee must write: `.deia/hive/responses/20260318-TASK-235-REQUEUE-RESPONSE.md`

All 8 sections required (see BOOT.md):
1. Header (task ID, status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (concrete changes)
4. Test Results (pass/fail counts)
5. Build Verification (test output summary)
6. Acceptance Criteria (copied from task, marked [x] or [ ])
7. Clock / Cost / Carbon (all three, never omit)
8. Issues / Follow-ups (edge cases, dependencies, next tasks)

---

## Previous Work Reference

- Original spec: `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-235-loading-states.md`
- Previous response: `.deia/hive/responses/20260317-TASK-235-RESPONSE.md`
- Failure reason: AppFrame.tsx changes never landed

---

## Q33N Instructions

1. Read all three files listed above
2. Write ONE task file for ONE bee (Sonnet)
3. Task file must specify AppFrame.tsx modifications in detail
4. Task file must reference existing PaneLoader.tsx (don't recreate)
5. Return task file to Q33NR for review before dispatch
6. Do NOT dispatch until Q33NR approves

---

**End of Briefing**
