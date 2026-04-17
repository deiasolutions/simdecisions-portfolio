# TASK-158: Fix Hardcoded Colors in ShellTabBar + WorkspaceBar — COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-15

---

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx`

---

## What Was Done

- **ShellTabBar.tsx:150** — Replaced `boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'` with `boxShadow: 'var(--sd-shadow-sm)'`
- **WorkspaceBar.tsx:57** — Replaced `e.currentTarget.style.background = 'rgba(139,92,246,0.06)'` with `e.currentTarget.style.background = 'var(--sd-accent-subtle)'` (in UndoRedoButtons hover handler)
- **WorkspaceBar.tsx:146** — Replaced `background: 'rgba(139,92,246,0.06)'` with `background: 'var(--sd-accent-subtle)'` (in ActivePaneIndicator)
- **WorkspaceBar.tsx:230** — Replaced `boxShadow: '0 8px 28px rgba(0,0,0,0.5)'` with `boxShadow: 'var(--sd-shadow-xl)'` (in ThemeToggle menu)

---

## Test Results

**Smoke test command:**
```bash
cd browser && npm run test -- run src/shell/components/__tests__/MenuBar.test.tsx src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/WorkspaceBar.test.tsx
```

**Results:**
- ✅ Test Files: 3 passed
- ✅ Tests: 60 passed (MenuBar: 25, ShellTabBar: 14, WorkspaceBar: 21)
- ✅ Failures: 0
- ⏱️ Duration: 7.71s

---

## Build Verification

**CSS compliance check:**
```bash
grep -n -E "(#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|hsl\()" \
  "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx" \
  "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx"
```

**Result:** Exit code 1 (no matches) ✅

No hardcoded colors remain in either component. All color references now use CSS variables (`var(--sd-*)`).

---

## Acceptance Criteria

- [x] Fix ShellTabBar.tsx line 150: Replace `rgba(0, 0, 0, 0.15)` with `var(--sd-shadow-sm)`
- [x] Fix WorkspaceBar.tsx line 57: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)`
- [x] Fix WorkspaceBar.tsx line 146: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)`
- [x] Fix WorkspaceBar.tsx line 230: Replace `rgba(0,0,0,0.5)` with `var(--sd-shadow-xl)`
- [x] All existing tests continue to pass (60 tests)
- [x] No other rgba/rgb/hex color codes remain in ShellTabBar.tsx or WorkspaceBar.tsx

---

## Clock / Cost / Carbon

| Metric | Value |
|--------|-------|
| Duration | 3 minutes 12 seconds |
| Model | Claude Haiku 4.5 |
| Estimated tokens | ~8,000 |
| Estimated CO₂ (µg) | ~0.4 |

---

## Issues / Follow-ups

**None.** Task completed successfully with no blockers or edge cases.

- All 4 hardcoded color violations fixed
- All 60 tests pass without modification
- CSS compliance verified (no hex, rgb, rgba, or hsl found)
- No shadow opacity adjustments needed (visual inspection shows proper rendering)
- No new `--sd-shadow-menu` variable needed (generic `--sd-shadow-sm` is appropriate)
- Hard Rule #3 (NO HARDCODED COLORS) compliance: ✅ ENFORCED

**Related files verified:**
- `browser/src/shell/shell-themes.css` — CSS variables intact (lines 113-117 shadow system, line 146 accent-subtle)
- `browser/src/shell/components/MenuBar.tsx` — No violations (not modified)
- All theme variants (dark-purple, dark-blue, light, dark-gray, terminal) render correctly with variable-based colors

