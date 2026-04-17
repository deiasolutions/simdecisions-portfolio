# Q33N Response: BL-208 Task File Ready for Review

**Date:** 2026-03-18
**Task:** BL-208 App Directory Sort (Re-Queue)
**Status:** READY FOR Q33NR REVIEW

---

## Task File Created

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BL-208-APP-DIRECTORY-SORT.md`

---

## What the Task File Contains

### Objective
Sort EGGs within each section (core/tools/fun) so BUILT apps appear before STUB apps. Add visual distinction for stub apps.

### Scope
- **Single file to modify (logic):** `AppsHome.tsx` — add sort logic after grouping
- **Single file to modify (styling):** `AppsHome.css` — add stub card opacity class
- **Single file to modify (tests):** `AppsHome.test.tsx` — add 3 new sort tests

### Key Requirements Specified

1. **Sort logic:** After grouping eggs by section, sort each section's array by status field (BUILT before STUB)
2. **Visual distinction:** Reduce opacity on stub cards (recommended Option A: add `.apps-home-card--stub` class with `opacity: 0.6`)
3. **TDD:** Write 3 new tests BEFORE implementing sort logic
4. **No regressions:** All existing 10 tests must still pass

### Test Requirements

The task file includes 3 complete test examples (pseudo-code):
- Test 1: Verify BUILT apps render before STUB apps within each section
- Test 2: Verify stub cards have visual styling applied
- Test 3: Verify sort works correctly across all sections simultaneously

### Constraints Applied

- No file over 500 lines (current files: AppsHome.tsx 99 lines, AppsHome.css 93 lines)
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — full implementation required
- TDD — tests first, then code

### Model Assignment

**Haiku** — straightforward sort logic, clear requirements, well-scoped task

---

## Files Q33NR Should Review

1. `.deia/hive/tasks/2026-03-18-TASK-BL-208-APP-DIRECTORY-SORT.md` (task file)

---

## Why This Task Will Succeed (vs Previous Failure)

### Previous Failure Root Cause
Previous bee misread the requirement and thought "grouping by section" (which already existed) was the same as "sorting by status within sections" (which was missing).

### How This Task File Prevents Repeat

1. **Crystal clear objective:** "After grouping, sort each group's array by status field. BUILT before STUB."
2. **Exact code location:** Points to lines 38-52 in AppsHome.tsx where sort must be added
3. **Example implementation:** Provides pseudo-code showing exactly where and how to add the sort
4. **Explicit tests:** Shows 3 complete test examples that verify sort behavior
5. **Visual distinction requirement:** Explicit guidance on adding CSS class for stub cards

---

## Questions for Q33NR Before Dispatch

1. **Visual distinction approach:** I recommended Option A (reduce card opacity for stubs). Do you want a different approach (badge label change, "Coming Soon" text, etc.)?

2. **Dispatch confirmation:** Ready to dispatch Haiku bee after your approval?

---

## Next Steps (Pending Q33NR Approval)

1. Q33NR reviews task file
2. Q33NR approves or requests corrections
3. Q33N dispatches Haiku bee with command:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BL-208-APP-DIRECTORY-SORT.md --model haiku --role bee --inject-boot
   ```
4. Bee completes work, writes response file
5. Q33N reviews bee response, reports to Q33NR
6. Q33NR reports to Q88N

---

**Q33N awaiting Q33NR review and approval to dispatch.**
