# SPEC: Tree-Browser Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to tree-browser primitive to make it touch-friendly and responsive on tablets and phones.

## Context
The tree-browser component (`browser/src/primitives/tree-browser/TreeBrowser.tsx`) is the generic tree navigation UI (used for channels, members, file trees). Desktop CSS is at `browser/src/primitives/tree-browser/tree-browser.css`. Mobile requires:
- Larger touch targets for tree rows (48px minimum)
- Reduced padding, optimized spacing
- Simplified node rendering (smaller icons, less indent)
- Hide search bar on very narrow screens
- Safe area handling

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/tree-browser.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/TreeBrowser.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Increase `.tree-node-row` padding from 6px to 12px vertically on mobile (min 48px touch target)
- [ ] Reduce `.tree-node-label` font size from 14px to 13px on mobile
- [ ] Reduce tree indent per level from default to smaller value on mobile
- [ ] Hide `.tree-browser-search` on phones (<480px) — search takes too much space
- [ ] Add bottom padding for safe area: `padding-bottom: env(safe-area-inset-bottom)` on `.tree-browser-body`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open tree-browser on 375px viewport — rows are tappable (48px min height)
- [ ] Tap a tree node — easy to hit, no mis-taps
- [ ] Expand/collapse nodes — chevron icon is tappable
- [ ] Scroll to bottom — safe area padding visible on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/tree-browser.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 80 lines of new CSS
