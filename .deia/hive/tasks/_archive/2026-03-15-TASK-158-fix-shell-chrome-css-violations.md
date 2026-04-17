# TASK-158: Fix Hardcoded Colors in ShellTabBar + WorkspaceBar

## Objective

Fix 4 CSS Rule violations (hardcoded rgba values) in shell chrome components to comply with Hard Rule #3: NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`).

## Context

During the shell chrome port verification (Briefing 2026-03-15-BRIEFING-shell-chrome-menubar), all components were found to be successfully ported and all tests pass. However, 4 hardcoded rgba() values were found that violate Hard Rule #3.

The shiftcenter project has a complete CSS variable system defined in `browser/src/shell/shell-themes.css` with shadow, surface, and accent variables across all themes (dark-purple, dark-blue, light, dark-gray, terminal).

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (lines 113-117 for shadow variables, line 146 for accent-subtle)

## Deliverables

- [ ] Fix ShellTabBar.tsx line 150: Replace `rgba(0, 0, 0, 0.15)` with `var(--sd-shadow-sm)`
- [ ] Fix WorkspaceBar.tsx line 57: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)`
- [ ] Fix WorkspaceBar.tsx line 146: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)`
- [ ] Fix WorkspaceBar.tsx line 230: Replace `rgba(0,0,0,0.5)` with `var(--sd-shadow-xl)`
- [ ] All existing tests continue to pass (60 tests)
- [ ] No other rgba/rgb/hex color codes remain in ShellTabBar.tsx or WorkspaceBar.tsx

## Specific Changes Required

### ShellTabBar.tsx:150
**BEFORE:**
```typescript
boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
```

**AFTER:**
```typescript
boxShadow: 'var(--sd-shadow-sm)',
```

**Note:** `--sd-shadow-sm` is defined as `0 2px 8px rgba(0, 0, 0, 0.3)` in shell-themes.css. The shadow size differs (4px vs 2px), but this is the closest semantic match. If visual inspection shows the shadow is too subtle, create a follow-up task to define a new `--sd-shadow-menu` variable.

---

### WorkspaceBar.tsx:57
**BEFORE:**
```typescript
e.currentTarget.style.background = 'rgba(139,92,246,0.06)';
```

**AFTER:**
```typescript
e.currentTarget.style.background = 'var(--sd-accent-subtle)';
```

**Note:** `--sd-accent-subtle` is defined as `rgba(139, 92, 246, 0.1)` in default theme (line 146). Opacity differs (0.06 vs 0.1), but this is the correct semantic variable for subtle accent backgrounds.

---

### WorkspaceBar.tsx:146
**BEFORE:**
```typescript
background: 'rgba(139,92,246,0.06)',
```

**AFTER:**
```typescript
background: 'var(--sd-accent-subtle)',
```

**Note:** Same as line 57 fix.

---

### WorkspaceBar.tsx:230
**BEFORE:**
```typescript
boxShadow: '0 8px 28px rgba(0,0,0,0.5)',
```

**AFTER:**
```typescript
boxShadow: 'var(--sd-shadow-xl)',
```

**Note:** `--sd-shadow-xl` is defined as `0 8px 32px rgba(0,0,0,0.4)`. Size is close (28px → 32px, opacity 0.5 → 0.4). This is the correct semantic variable for large shadows on floating elements.

## Test Requirements

- [ ] Tests written FIRST (TDD) — **N/A** (tests already exist)
- [ ] All existing tests pass after changes
- [ ] Edge cases covered:
  - [ ] All 5 themes render correctly (dark-purple, dark-blue, light, dark-gray, terminal)
  - [ ] Menu dropdowns still have visible shadows
  - [ ] Undo/redo buttons still have visible hover state
  - [ ] Theme picker modal still has visible shadow

**Smoke test:**
```bash
cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/WorkspaceBar.test.tsx
```

Expected: 3 test files, 60 tests passing, 0 failures.

**CSS compliance check:**
```bash
grep -n -E "(#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|hsl\()" "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx" "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx"
```

Expected: No matches (exit code 1).

## Constraints

- No file over 500 lines (current: ShellTabBar 236, WorkspaceBar 428 — both compliant)
- CSS: var(--sd-*) only (this task enforces the rule)
- No stubs (no new code, only replacements)
- Do NOT modify MenuBar.tsx (it has no violations)
- Do NOT modify shell-themes.css (CSS variable definitions may contain rgba — that's allowed)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-158-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Heartbeat Requirement

POST heartbeats to `http://localhost:8420/build/heartbeat` every 3 minutes:
```json
{
  "task_id": "TASK-158",
  "status": "running",
  "model": "haiku",
  "message": "fixing CSS violations"
}
```

## Success Criteria

**Task is COMPLETE when:**
- All 4 rgba() calls replaced with var(--sd-*) equivalents
- All 60 tests still pass
- CSS compliance check returns no matches
- Response file has all 8 sections

**Task FAILS if:**
- Any test breaks
- New violations introduced
- Response file missing sections
