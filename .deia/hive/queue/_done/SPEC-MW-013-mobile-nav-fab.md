# SPEC: Mobile-Nav FAB Integration

## Priority
P2

## Depends On
MW-012

## Objective
Integrate the Quick Actions FAB with the mobile navigation hub so the FAB is visible and accessible at all navigation levels, with smart positioning that avoids overlapping nav content.

## Context
The FAB must remain accessible during navigation:
- Fixed position at bottom-right (or bottom-center for landscape)
- FAB z-index must be above nav pane (but below modals)
- FAB position adjusts on landscape orientation (center bottom instead of right)
- FAB respects safe area insets (iPhone notch, Android cutouts)
- FAB does not obscure nav items when nav is open

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx` — FAB component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNavHub.tsx` — nav hub from MW-011
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/constants.ts` — Z_LAYERS
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell layout

## Acceptance Criteria
- [ ] FAB positioned via CSS Grid or absolute positioning (fixed, bottom-right)
- [ ] FAB z-index: above nav pane (Z_LAYERS.FAB > Z_LAYERS.MOBILE_NAV)
- [ ] Responsive positioning: portrait (bottom-right), landscape (bottom-center)
- [ ] Safe area aware: bottom offset = 16px + env(safe-area-inset-bottom)
- [ ] FAB does not obscure nav items: nav has bottom padding equal to FAB height + margin
- [ ] FAB remains visible when nav is open (no CSS conflicts)
- [ ] FAB remains visible when nav is drilling down (animation does not clip FAB)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 8+ unit tests (positioning, z-index, safe area) + 2 E2E tests
- [ ] Accessible: FAB remains keyboard-focusable at all nav levels

## Smoke Test
- [ ] On mobile viewport (portrait): FAB visible at bottom-right
- [ ] Tap "Queue" (nav drill-down) → FAB remains visible and accessible
- [ ] On landscape (812x375): FAB moves to bottom-center
- [ ] On iPhone X: FAB bottom offset = 16px + safe-area-inset-bottom (~34px)
- [ ] Open nav, scroll to bottom → FAB does not overlap last nav item

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/mobile-nav-hub.css` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` (modify FAB placement)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/constants.ts` (add Z_LAYERS.FAB if missing)
- No new files — modify existing
- TDD: tests first
- Max 50 lines CSS changes
- Max 30 lines Shell.tsx changes
- Use CSS Grid or position: fixed (not float)
- FAB z-index must be numeric constant (not magic number)
