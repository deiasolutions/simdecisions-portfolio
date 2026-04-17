# BRIEFING: BUG-073 Canvas2 Light Mode Fix

**Date:** 2026-03-25
**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-BUG073-canvas2)
**To:** Q33N (Queen Coordinator)
**Priority:** P1
**Model Assignment:** Sonnet

---

## Objective

Fix the canvas2 EGG so the canvas background responds to light/dark color mode changes. Currently the canvas stays dark regardless of theme selection. Replace all hardcoded colors with CSS variable tokens.

---

## Problem

On canvas2 EGG, switching to light color mode does not update the canvas background color. The canvas stays dark regardless of theme selection.

**Root Cause (likely):** Hardcoded colors or missing CSS variable usage in FlowCanvas/drawing-canvas components.

**Project Convention:** All CSS must use `var(--sd-*)` tokens — no hex, no rgb(), no named colors (Rule 3).

---

## Context from Q88N

This is a P1 bug fix for the canvas2 EGG. Users report that when they toggle from dark mode to light mode, the canvas background stays dark. This makes the canvas unusable in light mode. The grid/dot pattern should also respond to theme changes, and node shapes must remain readable in both themes.

The canvas2 EGG is a simulation flow designer with multiple node types (PhaseNode, ResourceNode, CheckpointNode, SplitNode, JoinNode, QueueNode, CalloutNode, StickyNoteNode, and annotation nodes).

---

## Files to Investigate First

### EGG Definition
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`

### Canvas Components (likely sources of hardcoded colors)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\DesignMode.tsx`

### UI Components (may contain hardcoded colors)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowToolbar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx`

### Node Components (all 12 node types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\PhaseNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\ResourceNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\CheckpointNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\SplitNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\JoinNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\QueueNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\CalloutNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\StickyNoteNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\AnnotationRectNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\AnnotationEllipseNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\AnnotationTextNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\AnnotationImageNode.tsx`

### Properties Panel
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`

### Hooks
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts`

---

## Expected Deliverables

Your task is to write task files for bee(s) to fix this bug. The task files must include:

1. **Canvas background fix:** Make FlowCanvas background respond to theme changes (light/dark).
2. **Grid/dot pattern fix:** Make grid or dot pattern respond to theme changes.
3. **Node readability:** Ensure all node types remain readable in both light and dark modes.
4. **Color token compliance:** Replace ALL hardcoded colors (hex, rgb(), named colors) with `var(--sd-*)` tokens.
5. **Tests:** Write tests verifying theme-aware styling works (if feasible via TDD).
6. **Manual smoke test:** Verify http://localhost:5173/?egg=canvas2 switches correctly between light/dark modes.

---

## Acceptance Criteria (from Spec)

- [ ] Open http://localhost:5173/?egg=canvas2 and switch to light mode — canvas background changes to light
- [ ] Switch to dark mode — canvas background changes to dark
- [ ] Nodes, edges, and grid remain visible and readable in both modes
- [ ] `cd browser && npx vitest run` — no test regressions

---

## Constraints

1. **TDD:** Write tests first, then implementation (except pure CSS).
2. **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
3. **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies.
4. **CSS: `var(--sd-*)` only.** No hex, no rgb(), no named colors. MANDATORY.
5. **All file paths must be absolute** in task files.
6. **8-section response file** required from each bee.

---

## Smoke Test

- [ ] `cd browser && npx vitest run src/apps/sim/` — all sim tests pass
- [ ] `cd browser && npx vitest run` — no regressions across full suite

---

## Your Next Steps (Q33N)

1. **Read the files listed above.** Understand the current implementation.
2. **Identify all hardcoded colors.** Search for hex codes, rgb(), rgba(), named colors.
3. **Write task file(s)** for bee(s) to:
   - Replace hardcoded colors with CSS tokens
   - Ensure canvas background reacts to theme changes
   - Ensure grid/dot pattern reacts to theme changes
   - Test theme switching
4. **Return task file(s) to me (Q33NR) for review.** Do NOT dispatch bees yet.
5. **After I approve**, dispatch the bee(s).

---

## Notes

- This is a P1 bug, not a major refactor. Keep scope tight: fix the color issue, ensure theme switching works, move on.
- If you find extensive hardcoded colors across many files, consider breaking into 2-3 bee tasks (e.g., Canvas core + Node components + Properties panel).
- Do NOT create new CSS token variables without checking the existing theme system first.

---

## Model Assignment

Use **Sonnet** for this briefing response (you). Assign bee tasks to **Haiku** or **Sonnet** based on complexity.

---

**END BRIEFING**
