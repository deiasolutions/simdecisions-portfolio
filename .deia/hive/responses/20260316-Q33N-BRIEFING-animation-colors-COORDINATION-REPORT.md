# Q33N Coordination Report: Animation Colors Fix

**From:** Q33N (coordinator)
**To:** Q33NR (regent)
**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-animation-colors-fix.md

---

## Task File Created

**File:** `.deia/hive/tasks/2026-03-16-TASK-148-animation-colors-fix.md`
**Model Assignment:** Haiku (as specified in briefing)
**Scope:** Fix hardcoded colors in 6 animation components

---

## Investigation Summary

### 6 Animation Components Identified

All located in `browser/src/apps/sim/components/flow-designer/animation/`:

1. **TokenAnimation.tsx** (117 lines)
   - Violation: Imports `colors.purple` from `theme.ts`
   - Fix: Use `var(--sd-purple)` default prop

2. **CheckpointFlash.tsx** (143 lines)
   - Violations: `colors.purple`, `colors.text`, inline rgba with hex interpolation
   - Fix: Use `var(--sd-purple)`, `var(--sd-text-primary)`, CSS variables for shadows

3. **NodePulse.tsx** (79 lines)
   - Violations: `colors.purple`, hex-to-RGB parsing (lines 22-24), computed rgba values
   - Fix: Use `var(--sd-purple)`, remove parseInt logic, use CSS alpha variants

4. **QueueBadge.tsx** (79 lines)
   - Violations: `colors.red`, `colors.text`, computed rgba box-shadow
   - Fix: Use `var(--sd-red)`, `var(--sd-text-primary)`, CSS shadow variables

5. **ResourceBar.tsx** (93 lines)
   - Violations: `colors.green`, `colors.bgTerminal`, `colors.text`, `colors.red`, `colors.orange`, inline rgba
   - Fix: Use `var(--sd-green)`, `var(--sd-surface-alt)`, etc., CSS shadow variables

6. **SimClock.tsx** (192 lines)
   - Violations: Multiple `colors.*` references (11 instances), inline rgba, hex with alpha suffix
   - Fix: Replace all with corresponding `var(--sd-*)` variables

### CSS Variables Available

From `shell-themes.css` (671 lines), the following CSS variables are available:

**Colors:**
- `--sd-purple`, `--sd-purple-dim`, `--sd-purple-dimmer`, `--sd-purple-dimmest`
- `--sd-green`, `--sd-green-dim`, `--sd-green-dimmer`, `--sd-green-dimmest`
- `--sd-orange`, `--sd-orange-dim`, `--sd-orange-dimmer`
- `--sd-red`, `--sd-red-dim`, `--sd-red-dimmer`
- `--sd-cyan`, `--sd-cyan-dim`, `--sd-cyan-dimmer`
- `--sd-text-primary`, `--sd-text-secondary`, `--sd-text-muted`
- `--sd-surface`, `--sd-surface-alt`, `--sd-bg`
- `--sd-border`, `--sd-border-hover`, `--sd-border-subtle`

**Shadows:**
- `--sd-shadow-sm`, `--sd-shadow-md`, `--sd-shadow-lg`, `--sd-shadow-xl`, `--sd-shadow-2xl`

**Glows:**
- `--sd-purple-glow`, `--sd-green-glow`, `--sd-orange-glow`, `--sd-cyan-glow`

All CSS variables support 5 themes: default (dark purple), depth, light, monochrome, high-contrast.

### Source of Violations

The root cause is `browser/src/apps/sim/lib/theme.ts` (37 lines) which exports hardcoded hex/rgb values:

```typescript
export const colors = {
  bg: "#0e0a1a",
  purple: "#8b5cf6",
  purpleDim: "rgba(139,92,246,0.15)",
  green: "#22c55e",
  // ... 31 total hardcoded color values
}
```

This file should NOT be used by components. It appears to be legacy from platform port.

### Test Coverage

Existing test file: `browser/src/apps/sim/components/flow-designer/__tests__/animation.test.tsx` (222 lines)
- 17 total tests (14 active, 3 skipped)
- Tests all 6 animation components
- Line 120 explicitly checks for rgb values — must be updated to accept CSS variables

---

## Task File Breakdown

The task file specifies:

### Deliverables
1. Remove `theme.ts` imports from all 6 components
2. Replace 50+ hardcoded color references with CSS variables
3. Update test expectations for CSS variables
4. Verify all 17 animation tests pass + 1122 browser tests pass

### Specific Mappings Provided
For each component, the task file lists:
- Exact line numbers of violations
- Old value → New value mappings
- Which CSS variable to use for each replacement

### Edge Cases Documented
1. Drop-shadow filters with alpha
2. Gradient stops with transparency (use `transparent` keyword)
3. Box-shadow with rgba (use `--sd-shadow-*` variables)
4. Dynamic rgba construction (use CSS variables with alpha variants)

### Constraints
- TDD: Update tests FIRST, then fix components
- No hex, no rgb(), no named colors (except `transparent`)
- All 6 files stay under 500 lines (currently 117-192 lines each)

---

## Acceptance Criteria

From the spec (SPEC-task-148-animation-colors.md):
- [ ] All 6 animation components use CSS variables only
- [ ] No hardcoded hex, rgb(), or named colors remain
- [ ] All animation tests pass
- [ ] All browser tests pass

All criteria are covered in the task file.

---

## Risk Assessment

**Low risk:**
- All changes are mechanical replacements
- Test coverage already exists (17 tests)
- CSS variables already defined and in use elsewhere
- No new functionality, pure refactor

**Potential issues:**
- Drop-shadow filter syntax with CSS variables (edge case documented)
- Test may need adjustment for CSS variable matching (documented in task)

---

## Ready for Review

Q33NR, please review the task file:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-148-animation-colors-fix.md`

If approved, I will dispatch a Haiku bee to execute the task.

---

## Files Referenced

**Task file:**
- `.deia/hive/tasks/2026-03-16-TASK-148-animation-colors-fix.md` (NEW)

**Components to modify (6):**
- `browser/src/apps/sim/components/flow-designer/animation/TokenAnimation.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/CheckpointFlash.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/NodePulse.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/QueueBadge.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/ResourceBar.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/SimClock.tsx`

**Test file to update (1):**
- `browser/src/apps/sim/components/flow-designer/__tests__/animation.test.tsx`

**Reference files (read-only):**
- `browser/src/shell/shell-themes.css` (CSS variable source)
- `browser/src/apps/sim/lib/theme.ts` (legacy hardcoded colors, DO NOT USE)

---

**Next Step:** Await Q33NR approval before dispatching bee.
