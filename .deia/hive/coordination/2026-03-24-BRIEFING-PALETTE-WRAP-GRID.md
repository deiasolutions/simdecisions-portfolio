# BRIEFING: Canvas2 Palette Wrapping Grid Layout

**To:** Q33N
**From:** Q33NR
**Date:** 2026-03-24
**Priority:** P1
**Model Assignment:** haiku

---

## Objective

Convert the NodePalette component's embedded mode from a single-column vertical list to a wrapping icon grid layout with overflow scroll, and fix all hardcoded rgba() color violations.

---

## Context from Q88N

When NodePalette renders in embedded mode (inside sidebar adapter for canvas2), all 18 items stack in a single column. The sidebar panel is ~240px wide but each button is 40px — massive wasted space. Items that overflow the pane are not visible.

This is a simple CSS layout fix + color CSS violations cleanup. No complex logic, no new features.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts`

---

## What Needs to Change

### 1. Embedded Style (lines ~270-273)
Change from `flexDirection: 'column'` to `flexWrap: 'wrap'` with row direction. Add:
- `alignContent: 'flex-start'`
- `overflowY: 'auto'`

### 2. Hardcoded Color Violations
Fix ALL rgba() colors in NodePalette.tsx:
- Line 209: `rgba(139,92,246,0.3)` border colors
- Line 210: `rgba(139,92,246,0.15)` and `rgba(139,92,246,0.1)` backgrounds
- Line 226: `rgba(139,92,246,0.2)` tooltip border
- Line 229: `rgba(0,0,0,0.3)` box-shadow
- Line 265: `rgba(0,0,0,0.4)` floating shadow
- Line 286: `rgba(139,92,246,0.1)` divider

All must become `var(--sd-*)` CSS variables. Check `theme.ts` for appropriate variable names.

### 3. Dividers in Embedded Mode
Add full-width separator between sections (tools, process nodes, annotations) using `width: '100%'` flex items.

---

## Acceptance Criteria

- [ ] Embedded palette renders as a wrapping grid (flex-wrap)
- [ ] Overflow scrolls vertically
- [ ] Zero hardcoded rgba() colors — all use var(--sd-*) CSS variables
- [ ] Floating mode (non-embedded) still works as before (single column)
- [ ] Drag-and-drop still works from grid items
- [ ] Tooltips still appear on hover
- [ ] Tests pass (regression tests for drag-drop, tooltip, color variables)

---

## Constraints

- **No file over 500 lines** (modularize if needed)
- **CSS: var(--sd-*) only** — no hex, no rgb(), no named colors (Rule 3)
- **No stubs** (Rule 6)
- **TDD** — write tests first, then implementation (Rule 5)

---

## Task File Requirements

Q33N should create:

1. **One task file** for this work (single bee, haiku model)
2. Task must specify absolute file paths (Rule 8)
3. Task must include test requirements:
   - Regression test: embedded mode renders wrapping grid
   - Regression test: floating mode still renders single column
   - Visual test or DOM test: verify no hardcoded colors in output
   - Regression test: drag-drop still works
   - Regression test: tooltips still appear

---

## Response Requirements

The bee must write a response file with all 8 mandatory sections (BOOT.md):
1. Header (task ID, title, status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (bullet list of concrete changes)
4. Test Results (test files run, pass/fail counts)
5. Build Verification (test/build output summary)
6. Acceptance Criteria (copy from task, mark [x] or [ ])
7. Clock / Cost / Carbon (all three required)
8. Issues / Follow-ups (edge cases, dependencies, next tasks)

---

## Notes

- This is a straightforward CSS fix. No architectural changes.
- The palette already has embedded/floating mode logic — we're just changing the flex layout for embedded mode.
- Color variable mappings should follow existing patterns in theme.ts (e.g., purple → `--sd-accent-primary`, shadows → `--sd-shadow-*`).
- If wrapping causes spacing issues, use gap property instead of margins.

---

## Q33N Deliverables to Q33NR

1. One task file in `.deia/hive/tasks/`
2. Summary of the task file for Q33NR review
3. Wait for Q33NR approval before dispatching bee
