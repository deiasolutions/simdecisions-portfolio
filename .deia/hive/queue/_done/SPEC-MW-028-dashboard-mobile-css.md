# SPEC: Dashboard Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to dashboard primitive (bottom bar with model selector, currency display) to make it touch-friendly and responsive.

## Context
The dashboard bar (`browser/src/primitives/dashboard/DashboardBar.tsx`) has desktop CSS at `browser/src/primitives/dashboard/dashboard.css`. Mobile requires:
- Larger touch targets for buttons (48px minimum)
- Reduced padding, optimized spacing
- Hide non-essential elements on narrow screens
- Responsive dropdown positioning
- Safe area handling

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/dashboard/dashboard.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/dashboard/DashboardBar.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Increase `.dashboard-model-chooser-trigger` padding to min 48px touch target on mobile
- [ ] Reduce `.dashboard-bar` height from 32px to auto (let content flow) on mobile
- [ ] Hide `.dashboard-bar-status` on phones (<480px) — already done in CSS but verify
- [ ] Hide `.dashboard-model-chooser-provider` on phones — already done but verify
- [ ] Add bottom padding for safe area: `padding-bottom: env(safe-area-inset-bottom)` on `.dashboard-bar`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open dashboard on 375px viewport — model chooser button is tappable
- [ ] Tap model chooser — dropdown opens, options are 48px min height
- [ ] Tap currency display — if interactive, touch-optimized
- [ ] Bottom bar respects safe area on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/dashboard/dashboard.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 80 lines of new CSS
