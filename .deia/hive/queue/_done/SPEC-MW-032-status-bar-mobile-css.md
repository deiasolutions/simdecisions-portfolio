# SPEC: Status-Bar Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to status-bar primitive to make it touch-friendly and responsive on tablets and phones.

## Context
The status-bar component (`browser/src/primitives/status-bar/StatusBar.tsx`) is the bottom bar showing EGG name, currency, connection status. Desktop CSS is at `browser/src/primitives/status-bar/StatusBar.css`. Mobile requires:
- Reduced padding, optimized spacing
- Hide non-essential elements on narrow screens
- Responsive font sizes
- Safe area handling for notched devices

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/status-bar/StatusBar.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/status-bar/StatusBar.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Reduce `.status-bar` padding from 12px to 8px on mobile
- [ ] Reduce font size from 12px to 10px on mobile
- [ ] Hide `.currency-label` on phones (<480px) — already in CSS, verify
- [ ] Hide `.connection-label` on phones — already in CSS, verify
- [ ] Reduce `.egg-name` max-width from 200px to 120px on mobile — already in CSS, verify
- [ ] Add bottom padding for safe area: `padding-bottom: env(safe-area-inset-bottom)` on `.status-bar`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open status-bar on 375px viewport — content fits, readable
- [ ] EGG name truncated properly on narrow screen
- [ ] Currency value visible, label hidden
- [ ] Connection indicator visible, label hidden
- [ ] Status bar respects safe area on iPhone notch (bottom padding)

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/status-bar/StatusBar.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 60 lines of new CSS (most mobile rules already exist, just add safe area)
