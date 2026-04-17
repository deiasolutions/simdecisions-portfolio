# SPEC: Text-Pane Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to text-pane (SDEditor) to make it touch-friendly and responsive on tablets and phones.

## Context
The text-pane component (`browser/src/primitives/text-pane/SDEditor.tsx`) is the markdown editor primitive. Desktop CSS is at `browser/src/primitives/text-pane/sd-editor.css`. Mobile requires:
- Reduced padding to maximize content area
- Smaller font sizes for better fit
- Touch-optimized menu buttons (48px minimum)
- Hide non-essential toolbar items on narrow screens
- Safe area handling for notched devices

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/sd-editor.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/SDEditor.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Reduce `.sde-content` padding from 16px to 12px on mobile
- [ ] Reduce header height from 28px to 24px on mobile
- [ ] Increase touch targets: `.sde-menu-btn` min-height 48px on mobile
- [ ] Font size adjustments: base 16px → 14px, headings scale down
- [ ] Hide word count (`.sde-word-count`) on phones (<480px)
- [ ] Use `padding-bottom: env(safe-area-inset-bottom)` on `.sde-content`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open text-pane on 375px viewport — content readable, header fits
- [ ] Tap menu buttons — 48px targets, easy to hit
- [ ] Scroll to bottom — safe area padding visible on iPhone notch
- [ ] Open on 768px viewport — tablet layout renders correctly

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/sd-editor.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 100 lines of new CSS
