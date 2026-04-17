# Q33N-003 Batch 3 Task Files — COMPLETE

**Date:** 2026-03-19
**Bot ID:** QUEEN-2026-03-19-BRIEFING-Q33N-003-B
**Model:** Sonnet
**Status:** COMPLETE

---

## Task Files Written (3 total)

All task files written to staging folder: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\`

### 1. TASK-233: Theme Verified
**File:** `2026-03-19-TASK-233-THEME-VERIFIED.md`
**Objective:** Scan all browser CSS/TSX files for hardcoded colors, replace with `var(--sd-*)` variables
**Model:** haiku
**Max Files:** 10
**Min Tests:** 0 (verification task, but existing tests must pass)
**Risk:** LOW

**Key sections:**
- Files to read: `shell-themes.css` (design tokens), `CanvasApp.tsx` (known prior offender)
- Strategy: grep scan for hex/rgb/named colors → replace with CSS variables
- Constraints: MAX 10 files modified (prioritize by occurrence count if more)
- Build verification: vitest + npm build
- 8-section response template required

### 2. TASK-231: Seamless Pane Borders
**File:** `2026-03-19-TASK-231-SEAMLESS-PANE-BORDERS.md`
**Objective:** Remove double borders between adjacent shell panes (collapse 2px → 1px shared border)
**Model:** haiku
**Max Files:** 3
**Min Tests:** 3
**Risk:** LOW

**Key sections:**
- Files to read: `PaneChrome.tsx`, `SplitContainer.tsx`
- Strategy: CSS-only fix using parent `gap` + selective borders OR border-collapse logic
- Deliverables: single pane still has border, split panes have single shared border, seamless edges still work
- Test file: `PaneChrome.seamless-borders.test.tsx`
- Build verification: PaneChrome tests + shell tests + npm build
- 8-section response template required

### 3. TASK-BUG029: Stage App Add Warning
**File:** `2026-03-19-TASK-BUG029-STAGE-APP-ADD-WARNING.md`
**Objective:** Show confirmation warning when dropping app onto occupied pane (prevent silent replacement)
**Model:** haiku
**Max Files:** 3
**Min Tests:** 5
**Risk:** LOW

**Key sections:**
- Files to read: `layout.ts` (MOVE_APP action), `Shell.tsx`, `PaneChrome.tsx`
- Strategy: Add `pendingReplace` state + confirmation dialog component
- Deliverables: warning shown for occupied panes (center zone only), "Replace"/"Cancel" buttons
- Exception: empty panes, tabbed panes, and split zones do NOT show warning
- Test file: `ReplaceConfirmDialog.test.tsx`
- Build verification: shell tests + npm build
- 8-section response template required

---

## Task File Quality Checklist

All 3 task files include:

✅ **Explicit "Files You May Modify" section** with absolute paths and max file counts
✅ **Explicit "Files You Must NOT Modify" section**
✅ **TDD test requirements** with minimum test counts and test file names
✅ **Build verification commands** with absolute paths
✅ **8-section response template** requirement
✅ **No stubs allowed** constraint
✅ **Max files per task** enforced (10, 3, 3)
✅ **Absolute file paths** throughout
✅ **Model assignment** (all haiku)
✅ **Risk level** (all LOW)

---

## Critical Rules Compliance

✅ All file paths are absolute (start with `C:\Users\davee\...`)
✅ TDD requirement explicit in every task
✅ NO STUBS constraint in every task
✅ NO HARDCODED COLORS constraint in every task
✅ 500-line file limit constraint in every task
✅ 8-section response template required in every task
✅ Build verification commands with absolute paths
✅ Minimum test counts specified
✅ Max files per task specified and enforced

---

## Output Location

Task files written to: `.deia\hive\queue\_stage\`

**NOT** written to: `.deia\hive\tasks\` (these are STAGED — queue runner must NOT pick them up)

---

## Next Steps

1. Q33NR reviews these 3 task files
2. If approved, Q33NR moves them from `_stage/` to `queue/` or dispatches directly
3. If corrections needed, Q33NR specifies changes and Q33N revises

---

## Files Created

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\2026-03-19-TASK-233-THEME-VERIFIED.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\2026-03-19-TASK-231-SEAMLESS-PANE-BORDERS.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\2026-03-19-TASK-BUG029-STAGE-APP-ADD-WARNING.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-Q33N-003-BATCH-3-TASK-FILES.md` (this file)

---

## Summary

- **Task files written:** 3
- **Files staged:** 3 (in `_stage/`, not in `queue/`)
- **Total task file lines:** ~800 (avg ~267 lines per task)
- **Models assigned:** haiku (all 3)
- **Total min tests:** 8 (0 + 3 + 5)
- **Total max files:** 16 (10 + 3 + 3)
- **Risk:** LOW (all 3)

All task files ready for Q33NR review.
