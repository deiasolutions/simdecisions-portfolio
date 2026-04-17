# BRIEFING: BUG-021 — Canvas Minimap White Visible Zone Fix

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Spec:** `.deia/hive/queue/2026-03-17-SPEC-TASK-BUG021-canvas-minimap-white-zone.md`

---

## Situation

The spec describes a Canvas minimap issue:
1. White visible-zone rectangle clashing with dark theme
2. Corner outline misalignment

---

## Code Review Findings

### ✅ ALREADY FIXED (Partially)

**File: `browser/src/primitives/canvas/canvas.css` (lines 101-107)**
```css
.react-flow__minimap-mask {
  stroke: var(--sd-purple) !important;
  stroke-width: 2;
  stroke-dasharray: 4 4;
  fill: none !important;
}
```
- Already uses `var(--sd-purple)` (theme-aware)
- Already has dashed stroke pattern

**File: `browser/src/primitives/canvas/CanvasApp.tsx` (lines 499-506)**
```tsx
<MiniMap
  nodeColor={getNodeColor}
  maskColor="var(--sd-glass-bg)"
  maskStrokeColor="var(--sd-purple-dim)"
  maskStrokeWidth={2}
  pannable
  zoomable
/>
```
- Already uses CSS variables for all colors
- `maskColor` = `var(--sd-glass-bg)`
- `maskStrokeColor` = `var(--sd-purple-dim)`

**File: `browser/src/primitives/canvas/__tests__/minimap.styles.test.tsx`**
- Already exists (158 lines, 7 tests)
- Tests verify CSS variable usage
- Tests reject hardcoded white colors

---

## Problem Analysis

**ISSUE:** The spec may be based on outdated code OR the minimap props conflict with the CSS override.

**ReactFlow MiniMap behavior:**
- Component accepts `maskStrokeColor` prop (CanvasApp.tsx line 502)
- CSS also overrides with `!important` (canvas.css line 103)
- **Potential conflict**: Prop uses `var(--sd-purple-dim)`, CSS uses `var(--sd-purple)`

**Corner outline misalignment:**
- Spec mentions this but code review shows no evidence
- May be a ReactFlow internal rendering issue
- May require checking actual DOM output in browser (not visible in code)

---

## Task Assignment for Q33N

Write 1-2 task files for **haiku**:

### Option A: VERIFY + CLOSE (if no actual bug)
If manual testing shows minimap is already correct:
- Task: Verify minimap in both light/dark themes
- Task: Verify corner outline alignment
- Task: Close BUG-021 as already fixed (by prior work)
- Output: Completion report stating when/how it was fixed

### Option B: FIX REMAINING ISSUES (if bugs still exist)
If manual testing reveals actual issues:

**TASK-BUG-021-A: Resolve maskStrokeColor conflict**
- Remove conflicting CSS `!important` override OR remove component prop
- Ensure single source of truth for stroke color
- Verify theme switching works (dark → light → dark)
- Test file: Expand existing `minimap.styles.test.tsx`

**TASK-BUG-021-B: Fix corner outline misalignment**
(Only if confirmed to exist)
- Investigate ReactFlow's mask SVG rendering
- May need to override `.react-flow__minimap-mask` positioning
- May need to adjust `stroke-linejoin` or `stroke-linecap` CSS props
- Add test to verify alignment

---

## Required Deliverables

Regardless of option chosen, Q33N must provide:

1. **Investigation report:**
   - Manual test results (screenshot or description)
   - Confirm whether "white zone" still exists
   - Confirm whether "corner misalignment" exists

2. **Task files:**
   - If bugs exist: separate task files per issue
   - If already fixed: 1 verification + close task

3. **Tests:**
   - Expand existing `minimap.styles.test.tsx` OR
   - Document that existing tests already cover the fix

4. **Absolute file paths** in all task files

---

## Constraints (from BOOT.md Rule 3)

- NO hardcoded colors (no hex, no rgb(), no named colors)
- Only CSS variables: `var(--sd-*)`
- Existing code already follows this — maintain compliance

---

## Smoke Test

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/minimap.styles.test.tsx
cd browser && npx vitest run
```

---

## Questions for Q33N

Before writing tasks, answer:

1. **Does the "white visible zone" bug still exist?**
   (Check CanvasApp.tsx lines 501-502 — props already use CSS variables)

2. **Does the "corner outline misalignment" bug exist?**
   (Check rendered DOM in browser — may be ReactFlow internal issue)

3. **Is this spec based on outdated code?**
   (CSS override added in canvas.css lines 101-107 with comment "BUG-021")

If all bugs are already fixed, the task is a **verification + closure task**, not a fix task.

---

## Next Steps

1. Q33N investigates current state (manual browser test or DOM inspection)
2. Q33N writes task file(s) based on findings
3. Q33N submits task files to `.deia/hive/tasks/`
4. Q88NR reviews and approves dispatch

**Model:** haiku
**Priority:** P0 (per spec)

---

**Regent signature:** Q88NR-bot
**Timestamp:** 2026-03-17T22:49:00Z
