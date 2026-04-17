# BRIEFING: TASK-231 — Seamless Pane Borders Verification

**Date:** 2026-03-17
**From:** Q33NR
**To:** Q33N
**Model:** Haiku
**Priority:** P1

---

## Objective

Verify that the existing seamless pane border functionality works correctly in Wave 4 Product Polish (BL-002, task 4.3). Adjacent panes configured with `seamlessEdges` in their EGG layout should render without visible borders between them, creating a unified visual surface.

---

## Context from Q88N

This is a **verification task**, not a build-from-scratch task. The implementation already exists in `PaneChrome.tsx` (lines 73-88). The logic reads `node.meta.seamlessEdges` (per-edge boolean control: top/right/bottom/left) and removes borders and border-radius on seamless edges.

Two EGG files are known to use seamless splits:
- `eggs/chat.egg.md` — seamless split between chat output and terminal
- `eggs/canvas.egg.md` — seamless borders between panes

The task is to verify this works end-to-end with real EGG layouts, identify any visual glitches (shadows leaking, gaps, etc.), and add tests to ensure seamless edges behave correctly.

---

## Source Spec

`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.3

---

## Key Files to Reference

- `browser/src/shell/components/PaneChrome.tsx` — Seamless edge logic (lines 73-88)
- `browser/src/shell/components/shell.css` — Shell layout styles
- `eggs/chat.egg.md` — Uses seamless split
- `eggs/canvas.egg.md` — Uses seamless borders

---

## Deliverables (from spec)

- [ ] Verify seamlessEdges config in EGG files produces borderless adjacent panes
- [ ] Verify non-seamless edges still show proper borders with focus color
- [ ] Verify border-radius is removed only on seamless edges (not all corners)
- [ ] Verify focused pane highlight (`--sd-border-focus`) still works on non-seamless edges
- [ ] Test with chat.egg.md: chat output and terminal should appear as one surface
- [ ] Fix any visual glitches (shadows leaking through seamless edges, gaps, etc.)
- [ ] Add test: seamless edges remove border/radius, non-seamless keep them
- [ ] Run: `cd browser && npx vitest run src/shell/`

---

## Instructions for Q33N

1. **Read the existing implementation** in `PaneChrome.tsx` to understand how seamlessEdges logic works.
2. **Read the EGG files** (`chat.egg.md`, `canvas.egg.md`) to understand the expected seamless layout configurations.
3. **Write a task file** for a single bee (haiku model) to:
   - Verify end-to-end behavior with the existing EGG layouts
   - Add tests to `browser/src/shell/components/__tests__/` to ensure seamless edges behave correctly
   - Fix any visual glitches found (shadows, gaps, etc.)
   - Run all shell tests and confirm pass
4. **Task file requirements:**
   - Absolute file paths
   - Test requirements: specify test count and scenarios
   - CSS: var(--sd-*) only (Rule 3)
   - TDD: tests first, then implementation (Rule 5)
   - No stubs (Rule 6)
   - Response file: 8-section template (BOOT.md)
5. **Return the task file to me (Q33NR) for review BEFORE dispatching the bee.**

---

## Constraints

- No file over 500 lines (Rule 4)
- CSS: `var(--sd-*)` only — no hardcoded colors (Rule 3)
- TDD: tests first (Rule 5)
- No stubs (Rule 6)
- All file paths must be absolute (Rule 8)

---

## Expected Output

One task file in `.deia/hive/tasks/2026-03-17-TASK-231-seamless-pane-borders.md` ready for bee dispatch after Q33NR review.
