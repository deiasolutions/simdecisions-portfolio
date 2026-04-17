# SPEC: Settings Mobile CSS

## Priority
P2

## Objective
Add mobile CSS to settings UI to make it touch-friendly and responsive on tablets and phones.

## Context
The settings panel (`browser/src/primitives/settings/SettingsPanel.tsx`) has desktop CSS at `browser/src/primitives/settings/settings.css`. Mobile requires:
- Larger touch targets for buttons and tabs (48px minimum)
- Reduced padding, optimized spacing
- Scrollable modal on narrow screens
- Responsive input fields and dropdowns
- Safe area handling

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/settings/settings.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/settings/SettingsPanel.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Increase `.sd-settings-panel__tab` padding to min 48px touch target on mobile
- [ ] Reduce `.sd-settings-panel__content` max-height to fit mobile screens (e.g., 60vh)
- [ ] Increase button heights: `.sd-key-manager__btn` min 48px on mobile
- [ ] Add bottom padding for safe area: `padding-bottom: env(safe-area-inset-bottom)` on `.sd-settings-panel__content`
- [ ] Make `.sd-settings-modal__backdrop` padding smaller on mobile (12px instead of 20px)
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open settings on 375px viewport — modal fits screen, scrollable
- [ ] Tap tabs — easy to hit (48px targets)
- [ ] Tap buttons (Add Key, Save, Delete) — touch-optimized
- [ ] Scroll content — safe area padding at bottom

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/settings/settings.css`
- CSS only — no JSX changes
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 100 lines of new CSS
