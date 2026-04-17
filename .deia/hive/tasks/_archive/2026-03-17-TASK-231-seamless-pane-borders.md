# TASK-231: Seamless Pane Borders Verification

**Priority:** P1
**Wave:** 4 (Product Polish)
**Model:** Haiku
**Source:** `.deia/hive/coordination/2026-03-17-BRIEFING-TASK-231-seamless-pane-borders.md`

---

## Objective

Verify that the existing seamless pane border functionality works correctly end-to-end with real EGG layouts. Seamless edges should produce borderless adjacent panes, creating a unified visual surface between chat output and terminal (chat.egg.md) and between canvas panes (canvas.egg.md). Fix any visual glitches (shadows leaking, gaps, etc.) and enhance tests to ensure seamless edges behave correctly.

---

## Context

The implementation already exists in `PaneChrome.tsx` (lines 73-88). The logic reads `node.meta.seamlessEdges` (per-edge boolean control: top/right/bottom/left) and removes borders and border-radius on seamless edges.

Two EGG files use seamless splits:
- `chat.egg.md` — line 38: `"seamless": true` between chat output and terminal
- `canvas.egg.md` — line 74: `"seamless": true` between chat and terminal panes

Existing tests in `PaneChrome.test.tsx` cover basic seamless edge behavior (tests 13-20), but we need to verify end-to-end behavior with real EGG layouts and ensure all visual aspects work correctly.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (seamless edge logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` (seamless split config)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (seamless split config)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneChrome.test.tsx` (existing tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css` (shell styles)

---

## Deliverables

### 1. End-to-End Verification

- [ ] Verify `seamlessEdges` config in EGG files produces borderless adjacent panes
- [ ] Verify non-seamless edges still show proper borders with focus color (`var(--sd-border-focus)`)
- [ ] Verify border-radius is removed only on seamless edges (not all corners)
- [ ] Verify focused pane highlight still works on non-seamless edges
- [ ] Test with chat.egg.md: chat output and terminal should appear as one surface
- [ ] Test with canvas.egg.md: chat and terminal panes should appear as one surface

### 2. Visual Glitch Fixes

- [ ] Check for shadows leaking through seamless edges — fix if present
- [ ] Check for gaps between seamless panes — fix if present
- [ ] Ensure border transitions (focus/blur) work smoothly on seamless edges
- [ ] Verify no visual artifacts when resizing panes with seamless edges

### 3. Test Enhancements

- [ ] Add test: seamless right edge removes right border and right-side border-radius
- [ ] Add test: seamless bottom edge removes bottom border and bottom-side border-radius
- [ ] Add test: seamless left edge removes left border and left-side border-radius
- [ ] Add test: seamless top edge removes top border and top-side border-radius
- [ ] Add test: seamless edges with focused pane still show focus border on non-seamless edges
- [ ] Add test: multiple seamless edges (e.g., top + right) remove borders/radius correctly
- [ ] Run: `cd browser && npx vitest run src/shell/components/__tests__/PaneChrome.test.tsx`
- [ ] Verify all existing tests still pass (38 tests minimum)

---

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All new tests pass
- [ ] All existing tests still pass (38+ tests)
- [ ] Test count after additions: **45+ tests** (7 new tests minimum)
- [ ] Edge cases tested:
  - Single seamless edge (top, right, bottom, left)
  - Multiple seamless edges (top + right, bottom + left, etc.)
  - Seamless edges with focus state
  - Seamless edges with notification state
  - Non-seamless edges retain borders/radius

---

## Constraints

- No file over 500 lines (Rule 4)
- CSS: `var(--sd-*)` only — no hardcoded colors (Rule 3)
- TDD: tests first, then fixes if needed (Rule 5)
- No stubs (Rule 6)
- All file paths must be absolute (Rule 8)

---

## Acceptance Criteria

- [ ] Seamless edges remove border and border-radius on specified edges
- [ ] Non-seamless edges retain border (`1px solid var(--sd-border-subtle)`) and border-radius (4px)
- [ ] Focused pane shows focus border (`var(--sd-border-focus)`) on non-seamless edges only
- [ ] No visual glitches (shadows, gaps, artifacts) on seamless edges
- [ ] chat.egg.md renders with seamless split between chat output and terminal
- [ ] canvas.egg.md renders with seamless split between chat and terminal panes
- [ ] 45+ tests pass in `PaneChrome.test.tsx`
- [ ] No hardcoded colors in any modified files
- [ ] No files exceed 500 lines

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-231-RESPONSE.md`

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
