# COORDINATION REPORT: Shell Chrome MenuBar + ShellTabBar + WorkspaceBar

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-15
**Briefing:** 2026-03-15-BRIEFING-shell-chrome-menubar
**Status:** PORT ALREADY COMPLETE — CSS VIOLATIONS FOUND

---

## Executive Summary

All three shell chrome components have ALREADY been ported to shiftcenter:
- MenuBar.tsx (423 lines) — COMPLETE, tests passing
- ShellTabBar.tsx (236 lines) — COMPLETE, tests passing
- WorkspaceBar.tsx (428 lines) — COMPLETE, tests passing

All 60 tests pass (303 + 253 + 304 test lines across 3 test files).

**HOWEVER:** 4 CSS Rule violations found (hardcoded rgba values). This blocks acceptance.

---

## Files Verified

### Target Components (shiftcenter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (423 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx` (236 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx` (428 lines)

### Test Files (shiftcenter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (303 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ShellTabBar.test.tsx` (253 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\WorkspaceBar.test.tsx` (304 lines)

### Source Components (platform)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\MenuBar.tsx` (430 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ShellTabBar.tsx` (233 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\WorkspaceBar.jsx` (243 lines)

---

## Test Results

```bash
cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/WorkspaceBar.test.tsx
```

**Result:** ✓ 3 test files, 60 tests passed, 0 failures

Test breakdown:
- MenuBar.test.tsx: 29 tests ✓
- ShellTabBar.test.tsx: 16 tests ✓
- WorkspaceBar.test.tsx: 15 tests ✓

---

## CSS Violations (HARD RULE #3)

**Rule:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.

**Violations Found:**

1. **ShellTabBar.tsx:150**
   ```typescript
   boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
   ```
   → Must use `var(--sd-shadow-*)` variable

2. **WorkspaceBar.tsx:57** (inline style mutation)
   ```typescript
   e.currentTarget.style.background = 'rgba(139,92,246,0.06)';
   ```
   → Must use `var(--sd-surface-accent)` or similar

3. **WorkspaceBar.tsx:146** (style object)
   ```typescript
   background: 'rgba(139,92,246,0.06)',
   ```
   → Must use `var(--sd-surface-accent)` or similar

4. **WorkspaceBar.tsx:230** (style object)
   ```typescript
   boxShadow: '0 8px 28px rgba(0,0,0,0.5)',
   ```
   → Must use `var(--sd-shadow-*)` variable

---

## File Size Compliance (HARD RULE #4)

All files are under the 500-line soft limit:
- MenuBar.tsx: 423 lines ✓
- ShellTabBar.tsx: 236 lines ✓
- WorkspaceBar.tsx: 428 lines ✓

---

## Acceptance Criteria Status

From spec `2026-03-15-1332-SPEC-w1-12-shell-chrome-menubar`:

- [x] MenuBar component ported with menu structure
- [x] ShellTabBar component ported
- [x] WorkspaceBar component ported
- [ ] **All use var(--sd-*) CSS variables** — BLOCKED: 4 violations found
- [x] Tests written and passing

**BLOCKED on CSS violations.**

---

## Recommended Action

**Option A: Create fix task for existing violations**
Write a single task file to fix the 4 CSS violations:
- TASK-158: Fix hardcoded colors in ShellTabBar + WorkspaceBar

**Option B: Accept as-is and defer**
Mark briefing as complete, log CSS violations as tech debt, defer to backlog.

**Option C: Reject port and re-do**
Reject the existing port, create a fresh task to re-port with correct CSS.

**Q33N Recommendation:** **Option A** — the port is functionally complete and all tests pass. The CSS violations are minor and easily fixed in a single haiku task (15 min). Creating a fix task is the most efficient path.

---

## Task File Draft (if Option A approved)

I have prepared a draft task file:
- File: `.deia\hive\tasks\2026-03-15-TASK-158-fix-shell-chrome-css-violations.md`
- Target: Fix 4 hardcoded rgba() calls in ShellTabBar.tsx and WorkspaceBar.tsx
- Model: haiku (simple search-and-replace task)
- Estimated duration: 10-15 minutes

**Awaiting Q33NR approval to write and dispatch this task.**

---

## Questions for Q33NR

1. **Approve Option A?** (fix task for CSS violations)
2. **Which CSS variables should replace the rgba values?**
   - For `rgba(0,0,0,0.15)` shadow → `var(--sd-shadow-sm)` or define new?
   - For `rgba(0,0,0,0.5)` shadow → `var(--sd-shadow-lg)` or define new?
   - For `rgba(139,92,246,0.06)` accent → `var(--sd-surface-accent)` or define new?
3. **Should I check theme files for existing shadow/surface variables before creating task?**

---

## Next Steps (pending Q33NR decision)

**If Option A approved:**
1. Q33NR clarifies which CSS variables to use
2. Q33N writes TASK-158 with specific variable mappings
3. Q33N returns TASK-158 to Q33NR for review
4. Q33NR approves
5. Q33N dispatches haiku bee with TASK-158
6. Bee fixes violations, runs tests, writes response
7. Q33N reviews response, reports to Q33NR
8. Q33NR marks briefing complete

**If Option B or C approved:**
Q33NR provides alternate instructions.

---

**Awaiting Q33NR direction.**
