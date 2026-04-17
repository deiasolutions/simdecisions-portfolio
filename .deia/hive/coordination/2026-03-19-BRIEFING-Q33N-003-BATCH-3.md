# BRIEFING: Q33N-003 — Batch 3 Task Files (Staged)

**From:** Q33NR
**To:** Q33N-003
**Date:** 2026-03-19
**Priority:** P1

---

## Your Role

You are Q33N-003 (Queen Coordinator). Read `.deia/BOOT.md` and `.deia/HIVE.md` first. Your job: write 3 task files to the STAGING folder, then STOP.

## IMPORTANT: Output Location

Write task files to: `.deia/hive/queue/_stage/`
**NOT** to `.deia/hive/tasks/`
These are staged — they must NOT be picked up by the queue runner.

## What You Must Produce

### Item 1: TASK-233 (Theme Verified)
- **File:** `.deia/hive/queue/_stage/2026-03-19-TASK-233-THEME-VERIFIED.md`
- **What it does:** Scan all browser CSS and TSX files for hardcoded colors (hex, rgb, named colors) and replace with `var(--sd-*)` CSS variables. Verify theme consistency.
- **Context:** ShiftCenter uses a design token system. All colors must use `var(--sd-*)` variables defined in `browser/src/shell/themes/shell-themes.css`. Previous work (March 17) was reverted. Some hardcoded colors may have crept back in during browser recovery.
- **Files to read first:**
  - `browser/src/shell/themes/shell-themes.css` (design tokens)
  - `browser/src/primitives/canvas/CanvasApp.tsx` (known prior offender — had `#fef3c7`, fixed in RB4)
- **Files bee may modify:** Any `.tsx`, `.ts`, or `.css` file in `browser/src/` that contains hardcoded colors — but MAX 10 files
- **Files bee must NOT modify:** `shell-themes.css` itself (tokens are correct), any backend files, any test files (unless tests assert hardcoded colors)
- **Model:** haiku
- **Deliverable:** List of all files scanned, all hardcoded colors found, all replacements made. If zero found, document the verification.
- **Minimum tests:** 0 (verification task — but if colors are changed, existing tests must still pass)
- **Risk:** LOW

### Item 2: TASK-231 (Seamless Pane Borders)
- **File:** `.deia/hive/queue/_stage/2026-03-19-TASK-231-SEAMLESS-PANE-BORDERS.md`
- **What it does:** Remove double borders between adjacent shell panes. When two panes sit side-by-side, their borders should collapse into a single 1px line, not double up to 2px.
- **Context:** Shell panes are rendered by `PaneChrome.tsx`. Each pane has a border. When two panes are adjacent in a split, both borders render = 2px gap. The fix is CSS-only: use border-collapse logic (e.g., only apply border-right/border-bottom, or use negative margins, or use gap on the parent flexbox).
- **Files to read first:**
  - `browser/src/shell/components/PaneChrome.tsx`
  - `browser/src/shell/components/PaneChrome.css` (or `.module.css`)
  - `browser/src/shell/Shell.tsx` (parent layout)
  - `browser/src/shell/components/SplitContainer.tsx` (if exists — handles split layout)
- **Files bee may modify:** Max 3 files
  - `browser/src/shell/components/PaneChrome.tsx` (or its CSS)
  - `browser/src/shell/components/SplitContainer.tsx` (or its CSS)
  - Related CSS modules
- **Files bee must NOT modify:** Any primitive code, any backend files, any adapter files
- **Model:** haiku
- **Minimum tests:** 3 (verify border renders, verify no double border in split, verify single pane still has border)
- **Risk:** LOW (CSS only)

### Item 3: BUG-029 (Stage App Add Warning)
- **File:** `.deia/hive/queue/_stage/2026-03-19-TASK-BUG029-STAGE-APP-ADD-WARNING.md`
- **What it does:** When a user tries to add/drop an app onto a pane that already has an app, show a confirmation warning instead of silently replacing.
- **Context:** The stage manages app placement in panes. Currently, dropping an app onto an occupied pane replaces the existing app without warning. The fix: detect occupied pane, show confirmation dialog (or toast), only replace if confirmed.
- **Files to read first:**
  - `browser/src/shell/actions/layout.ts` (moveAppOntoOccupied and related functions)
  - `browser/src/shell/Shell.tsx` (drop handling)
  - `browser/src/shell/components/PaneChrome.tsx` (pane rendering)
- **Files bee may modify:** Max 3 files
  - `browser/src/shell/actions/layout.ts`
  - Related shell component for confirmation UI
  - Test file for the confirmation logic
- **Files bee must NOT modify:** Any primitive code, any backend files, any adapter files
- **Model:** haiku
- **Minimum tests:** 5 (occupied pane detected, warning shown, confirm replaces, cancel preserves, empty pane no warning)
- **Risk:** LOW

## Critical Rules for Every Task File

1. **Explicit "Files You May Modify" section** with absolute paths
2. **Explicit "Files You Must NOT Modify" section**
3. **TDD test requirements** with minimum test counts
4. **Build verification commands** with absolute paths
5. **8-section response template** requirement
6. **No stubs allowed** — every function complete
7. **Max files per task as specified above**

## When Done

Write a completion report to `.deia/hive/responses/20260319-Q33N-003-BATCH-3-TASK-FILES.md` listing all 3 task files and their status.

Then STOP. Do NOT dispatch bees. Do NOT move files out of `_stage`.
