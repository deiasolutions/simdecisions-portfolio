# SPEC-PALETTE-COLLAPSE

## Bugs
BUG-023

## Priority
P0

## Model
haiku

## Summary
Canvas components panel does not collapse to icon-only mode per spec. ResizeObserver and collapsed state exist in TreeBrowser but CSS styles for collapsed mode are missing or incomplete.

## Key Files
- `browser/src/primitives/tree-browser/TreeBrowser.tsx` — lines 32-44, ResizeObserver sets `collapsed` when width < 120px
- `browser/src/primitives/tree-browser/tree-browser.css` — needs `.tree-browser.collapsed` styles
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` — row rendering in collapsed mode

## Investigation Notes
- `collapsed` class is applied to root div (line 129 in TreeBrowser.tsx)
- Header and search are hidden when collapsed (lines 130-146)
- Missing: CSS rules to hide label text, show only icons in collapsed mode
- Missing: TreeNodeRow may not know about collapsed state to hide label

## Required Changes
1. Add `.tree-browser.collapsed` CSS: hide labels, search, show icons only
2. Ensure TreeNodeRow hides text and shows only icon when parent is collapsed
3. Verify ResizeObserver threshold (120px) is appropriate for palette pane width

## Tests Required
1. TreeBrowser applies `collapsed` class when container width < threshold
2. Labels hidden in collapsed mode
3. Icons still visible in collapsed mode
4. Expanding past threshold restores full labels

## Depends On
Nothing

## Acceptance Criteria
- [ ] TreeBrowser applies `collapsed` class when container width < 120px threshold
- [ ] CSS rules for `.tree-browser.collapsed` hide label text and show icons only
- [ ] TreeNodeRow renders only icon (no label text) when parent TreeBrowser is collapsed
- [ ] Header and search are hidden in collapsed mode
- [ ] Expanding past width threshold restores full labels and layout
- [ ] All 4 tests passing: collapsed class applied, labels hidden, icons visible, expand restores
- [ ] No hardcoded colors, only CSS variables (`var(--sd-*)`)
