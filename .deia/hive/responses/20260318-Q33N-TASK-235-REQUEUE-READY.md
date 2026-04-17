# Q33N Report: TASK-235-REQUEUE Task File Ready for Review

**Task:** Wire PaneLoader into AppFrame (TASK-235 Re-Queue)
**Q33N:** QUEEN-2026-03-18-BRIEFING-TASK-235-l
**Date:** 2026-03-18
**Status:** Task file written, awaiting Q33NR review

---

## Summary

Task file created for re-queue of TASK-235. The original bee created PaneLoader.tsx and wrote tests, but the AppFrame.tsx modifications never landed. PaneLoader exists in the codebase but is never imported or used.

**Task file location:**
`.deia\hive\tasks\2026-03-18-TASK-235-REQUEUE-wire-pane-loader.md`

---

## Problem Analysis

### What Went Wrong in Original TASK-235
- **Bee claimed:** Modified AppFrame.tsx from 59 lines to 86 lines with loading logic
- **Git reality:** AppFrame.tsx is still 59 lines with ZERO loading logic
- **What exists:** PaneLoader.tsx (57 lines, 8 passing tests)
- **What's missing:** AppFrame.tsx import and usage of PaneLoader

### Root Cause
The bee's response file (`20260317-TASK-235-RESPONSE.md`) claimed to modify AppFrame.tsx, but those changes never got committed or saved. The file exists at exactly the same state as before the task.

---

## Task File Contents

### Objective
Modify AppFrame.tsx to import and use the existing PaneLoader component.

### Key Requirements
1. **Import PaneLoader** from './PaneLoader'
2. **Add loading state** with useState/useEffect hooks
3. **100ms delay** before showing loader (prevents flash)
4. **150ms timer** to mark component ready
5. **Reset state** when appType changes
6. **Never show loader** for 'empty' appType

### Files to Modify
- **ONLY:** `browser/src/shell/components/AppFrame.tsx`
- **DO NOT modify:** PaneLoader.tsx, PaneLoader.test.tsx, AppFrame.loading.test.tsx (all already correct)

### Test Requirements
- AppFrame.loading.test.tsx: 8/8 pass (currently 0/8 because AppFrame has no loading logic)
- PaneLoader.test.tsx: 8/8 pass (already passing, must not regress)
- shell/ suite: no regressions

### Constraints
- No file over 500 lines (AppFrame.tsx currently 59, keep under 150)
- CSS: var(--sd-*) only
- No stubs
- No modifications to existing working files

---

## Model Assignment

**sonnet** — Frontend timing logic requires careful state management.

---

## Files Referenced in Task

### Files to Read (bee must read these first)
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx` (current, no loading logic)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneLoader.tsx` (existing, works)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\AppFrame.loading.test.tsx` (tests to pass)

### Files to Modify
- `browser/src/shell/components/AppFrame.tsx` — ONLY this file

### Files to NOT Touch
- PaneLoader.tsx — already exists and works
- PaneLoader.test.tsx — 8 tests already passing
- AppFrame.loading.test.tsx — tests already written and correct

---

## Acceptance Criteria (from task file)

- [ ] AppFrame.tsx imports PaneLoader
- [ ] Loading spinner shows when pane is mounting (after 100ms delay)
- [ ] No flash on fast loads (<100ms)
- [ ] Loading hidden for 'empty' appType
- [ ] Loading resets when appType changes
- [ ] AppFrame.loading.test.tsx: 8/8 pass
- [ ] PaneLoader.test.tsx: 8/8 pass (no regression)
- [ ] No new test failures in shell/ suite
- [ ] No hardcoded colors in AppFrame.tsx
- [ ] AppFrame.tsx stays under 150 lines

---

## Task File Quality Checklist

✅ **Objective:** Clear one-sentence objective
✅ **Context:** Explains what exists vs what's missing
✅ **Files to Read:** All 3 files listed with absolute paths
✅ **Files to Modify:** ONLY AppFrame.tsx specified
✅ **Technical Requirements:** Detailed loading state logic specified
✅ **Deliverables:** 10 concrete deliverables listed
✅ **Test Requirements:** 3 test commands with expected results
✅ **Constraints:** All 6 BOOT.md constraints included
✅ **Acceptance Criteria:** 10 specific criteria
✅ **No stubs:** No placeholders or TODOs
✅ **No hardcoded colors:** CSS var(--sd-*) only specified
✅ **File size limits:** AppFrame.tsx keep under 150 lines (currently 59)
✅ **Response requirements:** 8-section template included
✅ **Model assignment:** sonnet (appropriate for timing logic)
✅ **Priority:** P1 (re-queue)
✅ **Re-queue metadata:** Links to original spec and response

---

## Expected Outcome

After bee completes:
- AppFrame.tsx will have loading state logic (~80-100 lines total)
- All 8 tests in AppFrame.loading.test.tsx will pass
- All 8 tests in PaneLoader.test.tsx will still pass
- No regressions in shell/ test suite
- PaneLoader will be imported and used in production code

---

## Next Steps (awaiting Q33NR approval)

1. **Q33NR reviews this task file** for:
   - Missing deliverables
   - Vague acceptance criteria
   - File paths correctness
   - Constraint completeness
   - Test requirements clarity

2. **If corrections needed:** Q33N fixes and returns task file

3. **If approved:** Q33N dispatches bee with:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py \
     .deia/hive/tasks/2026-03-18-TASK-235-REQUEUE-wire-pane-loader.md \
     --model sonnet --role bee --inject-boot
   ```

4. **When bee completes:** Q33N reviews response file and reports to Q33NR

---

## Priority Justification

**P1** — This is a re-queue to fix incomplete work from a previous task. PaneLoader component exists but is dead code (never used). Tests exist but fail because AppFrame has no loading logic. This is a loose end that needs closing.

---

**Ready for Q33NR review.**
