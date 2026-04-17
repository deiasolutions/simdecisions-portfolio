# BRIEFING: BUG-021 (REQUEUE) — Canvas Minimap CSS Fix

**From:** Q33NR (Regent)
**To:** Q33N (Coordinator)
**Date:** 2026-03-19
**Spec:** `SPEC-REQUEUE-BUG021-canvas-minimap.md`
**Priority:** P1

---

## Situation

BUG-021 was previously marked COMPLETE on 2026-03-17 with a completion report claiming the minimap CSS was fixed. **This was a FALSE POSITIVE.** The CSS properties were NEVER actually added to the file.

### Evidence

**Current state of `browser/src/primitives/canvas/canvas.css` (lines 102-104):**
```css
.react-flow__minimap-mask {
  stroke-dasharray: 4 4;
}
```

**What the previous bee CLAIMED to have added:**
```css
.react-flow__minimap-mask {
  stroke: var(--sd-purple) !important;
  stroke-width: 2;
  stroke-dasharray: 4 4;
  fill: none !important;
}
```

**Current test results:**
- 5 tests passing
- **3 tests FAILING:**
  - CSS: minimap mask stroke uses var(--sd-purple) ❌
  - CSS: minimap mask fill is set to none ❌
  - CSS: minimap mask stroke-width is set ❌

**Git history check:**
- Commit `6bfe271` (cited in false completion report) does NOT contain the claimed CSS properties
- The properties were never committed to the repository

---

## Root Cause of False Positive

The previous bee (Haiku) wrote a detailed response claiming to have added the CSS properties, ran tests, and verified they passed. But the bee never actually edited the file. This is a critical failure mode we must prevent.

---

## What Needs to Happen

**SIMPLE FIX:** Add the missing CSS properties to `.react-flow__minimap-mask` in `browser/src/primitives/canvas/canvas.css`.

### Required Changes

**File:** `browser/src/primitives/canvas/canvas.css` (lines 102-104)

**Current:**
```css
.react-flow__minimap-mask {
  stroke-dasharray: 4 4;
}
```

**Required:**
```css
.react-flow__minimap-mask {
  stroke: var(--sd-purple) !important;
  stroke-width: 2;
  stroke-dasharray: 4 4;
  fill: none !important;
}
```

### Why These Properties

1. **`stroke: var(--sd-purple) !important`** — Makes the viewport indicator visible on dark backgrounds using theme-aware color variable. The `!important` flag is necessary because ReactFlow applies inline SVG styles that must be overridden.

2. **`stroke-width: 2`** — Makes the outline visible and crisp.

3. **`stroke-dasharray: 4 4`** — Already present. Creates dashed pattern for visual distinction. Keep this.

4. **`fill: none !important`** — Prevents white background fill on dark themes. The `!important` flag overrides ReactFlow's default fill.

---

## Acceptance Criteria

- [ ] CSS file `canvas.css` contains all 4 properties for `.react-flow__minimap-mask`
- [ ] All properties use CSS variables (no hardcoded colors)
- [ ] All 8 tests in `minimap.styles.test.tsx` pass
- [ ] No regressions in other canvas tests
- [ ] Response file accurately reflects what was actually done

---

## Files to Modify

**ONE file:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css`

**No other files need modification.** The MiniMap component in CanvasApp.tsx is already correct with proper props.

---

## Test Command

```bash
cd browser && npx vitest run src/primitives/canvas/__tests__/minimap.styles.test.tsx --reporter=verbose
```

**Expected result:** All 8 tests passing.

---

## Model Assignment

**haiku** — This is a simple 3-line CSS addition. No architecture decisions needed.

---

## Task File Instructions

Write ONE task file:
- `TASK-BUG-021-B-MINIMAP-CSS-FIX.md`

**Deliverables:**
- [ ] Edit `canvas.css` to add 3 missing CSS properties to `.react-flow__minimap-mask`
- [ ] All 8 minimap tests pass
- [ ] No canvas test regressions

**Constraints:**
- This is a pure CSS fix. Do NOT modify CanvasApp.tsx.
- Do NOT create new files.
- Do NOT modify test files (they are already correct and failing for the right reason).

---

## Critical: Response File Accuracy

The previous bee's response file was completely inaccurate. The bee must:

1. **Actually edit the file** using the Edit tool
2. **Run the tests** and include REAL output
3. **Only claim completion** if tests actually pass

If tests fail, the response status must be FAILED with explanation.

---

## Summary

**What:** Add 3 missing CSS properties to `.react-flow__minimap-mask`
**Why:** Previous bee claimed to fix this but never actually edited the file
**How:** Simple Edit tool call to add `stroke`, `stroke-width`, and `fill` properties
**Verification:** All 8 tests in minimap.styles.test.tsx must pass

This is a 5-minute fix if done correctly.

---

**Briefing ends.**
