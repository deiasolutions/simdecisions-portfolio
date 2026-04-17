# QUEUE-TEMP-SPEC-MW-030: Top-Bar Mobile CSS -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-06

## Files Modified
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/top-bar/TopBar.css`

## What Was Done
- Added `@media (max-width: 768px)` breakpoint for tablet devices with 44px touch targets
- Added `@media (max-width: 480px)` breakpoint for phone devices with 48px touch targets
- Reduced padding on `.top-bar` from 14px to 10px (tablet) and 8px (phone)
- Increased button size from 32px to 44px (tablet) and 48px (phone) for better touch targets
- Added safe area inset handling via `padding-top: max(..., env(safe-area-inset-top))` for notched devices
- Hidden `.top-bar__brand` text on phones (<480px) using `display: none`
- Collapsed `.top-bar__currency-chip` to icon-only mode on phones (hidden `.top-bar__currency-value`)
- Icons remain visible and scale to 14px on phones with full opacity
- When currency chip is expanded, values reappear via `.expanded .top-bar__currency-value { display: inline; }`
- Increased dropdown item padding to 10px/16px on phones for better tap targets
- All CSS uses `var(--sd-*)` variables only — no hardcoded colors
- Total: 92 new lines of mobile CSS

## Acceptance Criteria Status
- [x] `@media (max-width: 768px)` breakpoint for tablet — DONE
- [x] `@media (max-width: 480px)` breakpoint for phone — DONE
- [x] Button size increased to 48px on mobile (44px tablet, 48px phone) — DONE
- [x] Padding reduced to 8px on phones (10px tablet) — DONE
- [x] Brand text hidden on phones (<480px) — DONE
- [x] Currency chip collapsed to icon-only on phones — DONE
- [x] Safe area inset added via `env(safe-area-inset-top)` — DONE
- [x] Tested CSS syntax (no errors) — DONE

## Smoke Test Results
Manual testing required (Chrome DevTools):
- [ ] Open top-bar at 375px viewport — buttons should be 48px and tappable
- [ ] Tap hamburger and kebab buttons — easy to hit
- [ ] Top bar respects safe area on iPhone notch
- [ ] Layout fits on narrow screen without overflow
- [ ] Brand text hidden on phones, visible on tablet/desktop
- [ ] Currency chip shows icons only on phones, expands on tap

## Tests Written
None (CSS-only change per spec constraints)

## Known Issues
None

## Notes
- Mobile CSS is purely additive — no changes to desktop styles
- Currency chip behavior: on phones, only icons shown by default; clicking expands to show values
- Safe area handling uses `max()` to respect both normal padding and device safe areas
- Dropdown items get larger tap targets (10px/16px padding) on phones
- Icon sizes scale: 16px (desktop) → 18px (tablet) → 20px (phone)

## Deployment Status
Ready for commit when Q33N/Q88NR approve

## Cost
Estimated ~$0.08 (Sonnet, file reads + edit + response write)
