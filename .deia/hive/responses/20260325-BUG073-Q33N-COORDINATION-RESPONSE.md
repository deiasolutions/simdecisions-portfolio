# BUG-073 Canvas2 Light Mode Fix — Q33N Coordination Response

**Status:** TASK FILE READY FOR REVIEW
**Date:** 2026-03-25
**Q33N Bot ID:** QUEEN-2026-03-25-BRIEFING-BUG073-can

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-25-TASK-BUG073-CANVAS2-LIGHT-MODE.md`

---

## Summary of Investigation

I read the briefing and investigated the canvas2 bug. I found the root causes:

### Root Cause Analysis

1. **Primary Issue:** `FlowCanvas.tsx` line 230 has `colorMode="dark"` hardcoded on the `<ReactFlow>` component. This prevents ReactFlow from responding to theme changes.

2. **Secondary Issues:**
   - MiniMap component (lines 253-259) has hardcoded `rgba(139,92,246,...)` colors
   - Background grid (line 241) uses `var(--sd-purple-dim)` which works but could use theme-aware token `var(--sd-grid-dot)`
   - ContextMenu.tsx has ~8 hardcoded rgba() colors
   - broadcast-highlights.css has 1 hardcoded cyan rgba

3. **Theme System:**
   - Light mode defined in `shell-themes.css` at `.hhp-root[data-theme="light"]` (lines 271-370)
   - Dark mode is default (lines 26-168)
   - All color tokens are already defined and theme-aware

### Files with Hardcoded Colors

I ran a grep search on the flow-designer directory and found **256KB of hardcoded colors** across the entire sim component tree. However, this task is scoped tightly to the canvas background issue only.

**In scope for this fix:**
- `FlowCanvas.tsx` — colorMode prop, MiniMap colors, Background grid
- `ContextMenu.tsx` — ~8 rgba colors
- `broadcast-highlights.css` — 1 cyan rgba

**Out of scope (documented for follow-up):**
- All 12 node components (PhaseNode, ResourceNode, CheckpointNode, etc.)
- Edge components (PhaseEdge, TokenEdge)
- Mode overlays (DesignMode, ConfigureMode, etc.)
- Properties panels
- Collaboration overlays
- Checkpoint managers
- Animation overlays

---

## Task File Details

### Deliverables

1. **Fix FlowCanvas colorMode** — Dynamic theme detection via MutationObserver watching `.hhp-root[data-theme]`
2. **Fix MiniMap colors** — Replace 4 hardcoded rgba with CSS variables
3. **Fix Background grid** — Use `var(--sd-grid-dot)` theme token
4. **Fix ContextMenu** — Replace rgba colors with CSS variables
5. **Fix broadcast-highlights.css** — Use `var(--sd-cyan-dimmest)`
6. **Tests** — 4 test cases for theme switching behavior

### Test Strategy

- **Unit tests:** `FlowCanvas.theme.test.tsx` with 4 test cases:
  1. Default dark mode
  2. Light mode when `data-theme="light"`
  3. Dynamic theme switching
  4. Other themes (depth, monochrome) use dark mode
- **Smoke test:** Manual verification at `http://localhost:5173/?egg=canvas2`

### Scope Control

The task explicitly tells the bee:
- "This is a P1 bug, not a major refactor. Keep scope tight."
- "Do NOT rewrite the entire canvas system."
- "If you find extensive hardcoded colors in node components, document them in Issues / Follow-ups but DO NOT fix them in this task."
- "Focus on the main canvas background, grid, and minimap."

---

## Acceptance Criteria

- [ ] FlowCanvas.tsx dynamically reads theme from `.hhp-root[data-theme]`
- [ ] colorMode prop on `<ReactFlow>` is dynamic, not hardcoded
- [ ] MiniMap colors use CSS variables, not hardcoded rgba
- [ ] Background grid color uses `var(--sd-grid-dot)`
- [ ] ContextMenu colors use CSS variables
- [ ] broadcast-highlights.css uses CSS variables
- [ ] All hardcoded rgba() colors in canvas2 files are replaced (or documented if kept for shadows)
- [ ] Open http://localhost:5173/?egg=canvas2 and switch to light mode — canvas background changes to light
- [ ] Switch to dark mode — canvas background changes to dark
- [ ] Nodes, edges, and grid remain visible and readable in both modes
- [ ] `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FlowCanvas.theme.test.tsx` — all tests pass
- [ ] `cd browser && npx vitest run` — no test regressions

---

## Recommended Model Assignment

**Haiku** — This is a straightforward color replacement task with clear acceptance criteria. Total estimated changes: ~15 lines + 1 test file (~80 lines). Haiku is sufficient.

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-25-TASK-BUG073-CANVAS2-LIGHT-MODE.md --model haiku --role bee --inject-boot
```

---

## Follow-Up Work (Not in This Task)

After this fix lands, there are 200+ files with hardcoded colors across the sim component tree:
- 12 node types
- Edge components
- Mode overlays
- Properties panels
- Collaboration components
- Checkpoint managers

These should be addressed in a separate sweep task, not in this P1 bug fix.

---

## Q33NR Review Checklist

Before approving dispatch, verify:
- [ ] Task file has all 8 deliverables clearly defined
- [ ] Test requirements include both unit tests and smoke test
- [ ] Acceptance criteria are concrete and verifiable
- [ ] Scope is tight (canvas background, grid, minimap, context menu only)
- [ ] Constraints enforced (TDD, no stubs, CSS variables only, absolute paths)
- [ ] Response file format specified (8 sections)
- [ ] Model assignment is appropriate (Haiku)
- [ ] Dispatch command is correct

---

**AWAITING Q33NR APPROVAL TO DISPATCH BEE**
