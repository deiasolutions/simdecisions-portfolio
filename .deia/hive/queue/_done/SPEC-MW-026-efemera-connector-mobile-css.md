# SPEC: Efemera-Connector Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to efemera-connector primitive to make it touch-friendly and responsive on tablets and phones.

## Context
The efemera-connector component (`browser/src/primitives/efemera-connector/EfemeraConnector.tsx`) is the two-tab UI for Efemera channels and members. Desktop CSS is at `browser/src/primitives/efemera-connector/efemera-connector.css`. Mobile requires:
- Larger touch targets for tab buttons (48px minimum)
- Optimized spacing, reduced padding
- Safe area handling for notched devices
- Responsive layout for narrow screens

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/efemera-connector/efemera-connector.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/efemera-connector/EfemeraConnector.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Increase `.efemera-connector-tab` size from 40px to 48px on mobile (touch target)
- [ ] Reduce `.efemera-connector-tabs` padding from 8px to 4px on mobile
- [ ] Add bottom padding for safe area: `padding-bottom: env(safe-area-inset-bottom)` on `.efemera-connector-content`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open efemera-connector on 375px viewport — tabs are tappable (48px min)
- [ ] Tap Channels tab — switches view, easy to hit
- [ ] Tap Members tab — switches view, easy to hit
- [ ] Scroll content to bottom — safe area padding visible on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/efemera-connector/efemera-connector.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 60 lines of new CSS
