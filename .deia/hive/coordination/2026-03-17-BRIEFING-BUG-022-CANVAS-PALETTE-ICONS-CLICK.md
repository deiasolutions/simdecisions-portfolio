# BRIEFING: BUG-022 — Canvas Components Panel Icons and Click Handling

**To:** Q33N
**From:** Q88NR
**Date:** 2026-03-17
**Spec:** `.deia/hive/queue/2026-03-17-SPEC-TASK-BUG022-canvas-components-panel-plain.md`
**Model Assignment:** Haiku
**Priority:** P0

---

## Problem

The Canvas components/palette panel (tree-browser with paletteAdapter) shows a plain text list with no visible icons. Clicking items does nothing — no drag initiation, no place-on-canvas behavior.

## Root Causes (Verified by Q88NR Code Review)

### Issue 1: Icon Display
**Current state:**
- `paletteAdapter.ts` lines 29-44 provide icon characters: '◉', '◈', '●', '○', '◆', '⊢', '⊣', '▭'
- `TreeNodeRow.tsx` line 82 renders: `<span className={tree-node-icon ${node.icon}} />`
- **Problem:** TreeNodeRow expects a CSS class, but receives a Unicode character. The character is added as a className (invalid), so nothing renders.

**Fix required:**
- TreeNodeRow must handle both CSS class icons AND text/Unicode icons
- If `node.icon` is a single character or starts with emoji/Unicode range, render as text content
- If `node.icon` is a CSS class identifier, apply as className

### Issue 2: Click Behavior
**Current state:**
- `TreeNodeRow.tsx` lines 33-38: clicking a palette node calls `onSelect(node.id, node)` — this only selects the node in the tree
- Palette nodes have `draggable: true` and drag handlers work (lines 46-61), but user must manually drag
- **Problem:** No automatic "click to place" or "click to initiate drag" behavior

**Spec requirement:** "Clicking a component places it on canvas or starts drag"

**Options to clarify with Q88N:**
1. **Click-to-drag mode:** Click palette node → cursor changes to "placing" mode → user clicks canvas to drop
2. **Click-to-place:** Click palette node → node instantly appears at canvas center or last mouse position
3. **Keep drag-only:** Palette items are drag-only (current behavior is correct, spec is wrong)

**Q88NR decision (mechanical):** The spec says "clicking a component places it on canvas or starts drag." This is ambiguous. Q33N must create TWO subtasks:
- **Subtask A (BEE-A):** Fix icon rendering (Issue 1) — mandatory P0
- **Subtask B (BEE-B):** Implement click-to-place at canvas center — simplest interpretation of spec

If Q88N wants click-to-drag mode instead, he will say so after reviewing BEE-B results.

---

## Files to Review (Q33N Read These First)

### Core files:
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` (96 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (114 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (527 lines)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (290 lines — read config)

### Supporting files:
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (TreeNodeData interface)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (to understand onSelect flow)

---

## Deliverables for Q33N

### Task File A (TASK-BUG-022-A): Fix Icon Rendering
**Objective:** Palette component icons display visually in the tree-browser

**Deliverables:**
- Modify `TreeNodeRow.tsx` to detect icon type (CSS class vs text/Unicode)
- Render Unicode icons as text content, CSS class icons as className
- All 8 palette icons render correctly: ◉, ◈, ●, ○, ◆, ⊢, ⊣, ▭
- Tests: TreeNodeRow with both icon types (CSS class + Unicode)

**Test requirements:**
- Unit test: TreeNodeRow with `icon: "◉"` renders `<span>◉</span>`
- Unit test: TreeNodeRow with `icon: "icon-task"` renders `<span className="tree-node-icon icon-task" />`
- Integration test: paletteAdapter → TreeBrowser → all icons visible

**Acceptance:**
- [ ] TreeNodeRow handles both CSS class and Unicode icons
- [ ] All 8 palette component types show icons in components panel
- [ ] Tests pass (min 3 tests for icon rendering)

**Model:** Haiku
**Priority:** P0

---

### Task File B (TASK-BUG-022-B): Click to Place on Canvas
**Objective:** Clicking a palette node places it at canvas center

**Deliverables:**
- Add `onClick` handler to palette nodes (in TreeBrowser or TreeNodeRow)
- When palette node is clicked, publish bus message: `palette:node-click` with nodeType
- CanvasApp subscribes to `palette:node-click`, creates node at canvas center (or viewport center)
- Tests: Click palette node → bus message sent → canvas receives + creates node

**Test requirements:**
- Unit test: palette node click publishes bus message with nodeType
- Integration test: full flow (palette click → canvas node created)
- Edge case: no canvas active → message ignored (no crash)

**Acceptance:**
- [ ] Clicking a palette component places it on canvas at viewport center
- [ ] Bus event `palette:node-click` defined and published
- [ ] CanvasApp handles `palette:node-click` event
- [ ] Tests pass (min 3 tests: bus publish, canvas receive, integration)

**Model:** Haiku
**Priority:** P0

---

## Constraints (from BOOT.md)

- No file over 500 lines (modularize if needed)
- CSS: `var(--sd-*)` only, no hardcoded colors
- TDD: tests first
- No stubs

---

## Q33N Next Steps

1. Read all 6 files listed above
2. Write TASK-BUG-022-A.md and TASK-BUG-022-B.md (two separate tasks)
3. Return task files to Q88NR for review
4. **Do NOT dispatch bees yet** — wait for Q88NR approval

---

## Q88NR Review Checklist (For My Own Use)

When Q33N returns task files, verify:
- [ ] Both task files present (A and B)
- [ ] File paths are absolute (Windows format)
- [ ] Test requirements specify exact scenarios (not vague "test it")
- [ ] Deliverables match spec acceptance criteria
- [ ] No CSS class names are hardcoded colors
- [ ] No file would exceed 500 lines
- [ ] Response file template requirement included
- [ ] No stubs in acceptance criteria

If all pass: approve dispatch.
If 1-2 issues: return to Q33N with corrections.
If >2 issues after 2 cycles: approve with ⚠️ APPROVED_WITH_WARNINGS.

---

**End of briefing.**
