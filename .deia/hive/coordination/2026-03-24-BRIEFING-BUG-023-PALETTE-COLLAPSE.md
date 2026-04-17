# BRIEFING: BUG-023 — Palette Collapse to Icon-Only Mode

**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-PALETTE-COLLAP)
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Model:** haiku

---

## Objective

Fix BUG-023: Canvas components panel (TreeBrowser) does not collapse to icon-only mode when resized below 120px threshold. ResizeObserver and collapsed state logic exist, but CSS styles for collapsed mode are missing or incomplete.

---

## Context from Spec

The spec states:
- ResizeObserver exists in TreeBrowser (lines 32-44) and sets `collapsed` state when width < 120px
- `collapsed` class is applied to root div (line 129)
- Header and search are hidden when collapsed (lines 130-146)
- **MISSING:** CSS rules to hide label text and show only icons in collapsed mode
- **MISSING:** TreeNodeRow may not know about collapsed state to hide labels

---

## Key Files

From the spec:
- `browser/src/primitives/tree-browser/TreeBrowser.tsx` — lines 32-44 (ResizeObserver), line 129 (collapsed class)
- `browser/src/primitives/tree-browser/tree-browser.css` — needs `.tree-browser.collapsed` styles
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` — row rendering in collapsed mode

---

## Required Changes (from spec)

1. Add `.tree-browser.collapsed` CSS: hide labels, search, show icons only
2. Ensure TreeNodeRow hides text and shows only icon when parent is collapsed
3. Verify ResizeObserver threshold (120px) is appropriate for palette pane width

---

## Tests Required (from spec)

1. TreeBrowser applies `collapsed` class when container width < threshold
2. Labels hidden in collapsed mode
3. Icons still visible in collapsed mode
4. Expanding past threshold restores full labels

---

## Acceptance Criteria (from spec)

- [ ] TreeBrowser applies `collapsed` class when container width < 120px threshold
- [ ] CSS rules for `.tree-browser.collapsed` hide label text and show icons only
- [ ] TreeNodeRow renders only icon (no label text) when parent TreeBrowser is collapsed
- [ ] Header and search are hidden in collapsed mode
- [ ] Expanding past width threshold restores full labels and layout
- [ ] All 4 tests passing: collapsed class applied, labels hidden, icons visible, expand restores
- [ ] No hardcoded colors, only CSS variables (`var(--sd-*)`)

---

## Constraints

- **Model:** haiku (cost-efficient bug fix)
- **TDD:** Tests first, then implementation (Rule 5)
- **No hardcoded colors:** Only CSS variables `var(--sd-*)` (Rule 3)
- **No file over 500 lines** (Rule 4)
- **No stubs** (Rule 6)

---

## Your Job

1. Read the spec above and the key files listed
2. Write ONE task file for a bee to fix this bug
3. Return to Q33NR for review (do NOT dispatch yet)
4. After Q33NR approves, dispatch the bee
5. Review the bee's response file when complete
6. Report results to Q33NR

---

## Notes

- This is a P0 bug fix. Keep it simple and focused.
- The collapse logic exists. The CSS is missing.
- TreeNodeRow may need a prop or context to know about collapsed state.
- Test file should verify CSS class application AND visual behavior (labels hidden, icons visible).
