# SPEC: Top-Bar Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to top-bar primitive to make it touch-friendly and responsive on tablets and phones.

## Context
The top-bar component (`browser/src/primitives/top-bar/TopBar.tsx`) is the main navigation bar at the top of the app. Desktop CSS is at `browser/src/primitives/top-bar/TopBar.css`. Mobile requires:
- Larger touch targets for buttons (48px minimum)
- Reduced padding, optimized spacing
- Hide non-essential elements on narrow screens (brand text, currency details)
- Responsive layout for narrow screens
- Safe area handling for notched devices

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/top-bar/TopBar.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/top-bar/TopBar.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Increase `.top-bar__button` size from 32px to 48px on mobile (touch target)
- [ ] Reduce `.top-bar` padding from 14px to 8px on mobile
- [ ] Hide `.top-bar__brand` text on phones (<480px) — show icon only if applicable
- [ ] Hide expanded `.top-bar__currency-chip` details on phones — show icon only
- [ ] Add top padding for safe area: `padding-top: env(safe-area-inset-top)` on `.top-bar`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open top-bar on 375px viewport — buttons are tappable (48px min)
- [ ] Tap menu button, settings button — easy to hit
- [ ] Top bar respects safe area on iPhone notch (top padding)
- [ ] Layout fits on narrow screen without overflow

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/top-bar/TopBar.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 80 lines of new CSS
