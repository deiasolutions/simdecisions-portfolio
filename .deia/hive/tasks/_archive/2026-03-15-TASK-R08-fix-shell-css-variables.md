# TASK-R08: Fix CSS var violations in ShellTabBar + WorkspaceBar

**Priority:** P0.40
**Original:** TASK-158 (shell chrome CSS fixes)
**Rebuild Batch:** 02
**Date:** 2026-03-15

---

## Objective

Replace hardcoded `rgba()` values in `ShellTabBar.tsx` and `WorkspaceBar.tsx` with CSS variables to comply with Hard Rule #3 (NO HARDCODED COLORS).

---

## Context

After `git reset --hard HEAD`, CSS variable replacements from TASK-158 were lost. Both files now contain hardcoded `rgba()` values that violate the project's strict CSS variable requirement.

**What was lost:**
- ShellTabBar.tsx line ~150: boxShadow with hardcoded rgba
- WorkspaceBar.tsx line ~57: hover background with hardcoded rgba
- WorkspaceBar.tsx line ~146: active pane indicator with hardcoded rgba
- WorkspaceBar.tsx line ~230: menu boxShadow with hardcoded rgba

All tests passed after the original fix — this is a pure CSS compliance task with no behavior changes.

**Dependencies:**
- This task is INDEPENDENT of all other rebuild tasks (browser-side only)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx` (current state with violations)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx` (current state with violations)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-158-RESPONSE.md` (original fix details)

---

## Deliverables

### 1. Fix ShellTabBar.tsx (1 location)

- [ ] Line ~150: Find `boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'`
- [ ] Replace with: `boxShadow: 'var(--sd-shadow-sm)'`

### 2. Fix WorkspaceBar.tsx (3 locations)

- [ ] Line ~57: Find `e.currentTarget.style.background = 'rgba(139,92,246,0.06)'` (in UndoRedoButtons hover handler)
- [ ] Replace with: `e.currentTarget.style.background = 'var(--sd-accent-subtle)'`

- [ ] Line ~146: Find `background: 'rgba(139,92,246,0.06)'` (in ActivePaneIndicator style object)
- [ ] Replace with: `background: 'var(--sd-accent-subtle)'`

- [ ] Line ~230: Find `boxShadow: '0 8px 28px rgba(0,0,0,0.5)'` (in ThemeToggle menu)
- [ ] Replace with: `boxShadow: 'var(--sd-shadow-xl)'`

### 3. Verify Complete Compliance

- [ ] Run grep to verify NO hex/rgb/rgba values remain:
  ```bash
  grep -n -E "(#[0-9a-fA-F]{3,6}|rgb\(|rgba\()" \
    "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx" \
    "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx"
  ```
- [ ] Expected: Exit code 1 (no matches) or empty output

---

## Test Requirements

### Tests Written FIRST (TDD)
- [ ] No new tests needed — existing tests verify component behavior

### All Tests Pass
- [ ] Run shell component tests:
  ```bash
  cd browser && npx vitest run \
    src/shell/components/__tests__/ShellTabBar.test.tsx \
    src/shell/components/__tests__/WorkspaceBar.test.tsx
  ```
- [ ] Expected: **All tests PASSING** (14 ShellTabBar + 21 WorkspaceBar = 35 tests)

### Visual Regression Check (Optional)
- [ ] If you want to verify visual rendering (not required):
  ```bash
  cd browser && npm run dev
  ```
- [ ] Check that shadows and hover states render correctly in browser

---

## Constraints

- No file over 500 lines (both files are well under this limit)
- **CSS variables ONLY** — this is Hard Rule #3, strictly enforced
- No behavior changes — this is a pure CSS compliance fix
- Do NOT add new CSS variables — use existing ones from `shell-themes.css`

---

## Acceptance Criteria

- [x] ShellTabBar.tsx line 150: `rgba(0, 0, 0, 0.15)` → `var(--sd-shadow-sm)`
- [x] WorkspaceBar.tsx line 57: `rgba(139,92,246,0.06)` → `var(--sd-accent-subtle)`
- [x] WorkspaceBar.tsx line 146: `rgba(139,92,246,0.06)` → `var(--sd-accent-subtle)`
- [x] WorkspaceBar.tsx line 230: `rgba(0,0,0,0.5)` → `var(--sd-shadow-xl)`
- [x] All 35 shell component tests pass
- [x] grep verification shows zero hardcoded color values
- [x] No new CSS variables created (used existing ones)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R08-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary (include grep output)
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Haiku (simple find-replace task)
**Estimated Duration:** 5 minutes
**Depends On:** None (independent browser-side task)
