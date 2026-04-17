# SPEC: Mobile-Nav Nested Hub Structure

## Priority
P2

## Depends On
MW-T05, MW-V02, MW-V03

## Objective
Build the mobile navigation hub structure with nested drill-down navigation, breadcrumb trails, parent/child navigation hierarchy, and safe area handling for notched devices.

## Context
The mobile-nav replaces the desktop menu bar with a touch-optimized hub-and-spoke navigation pattern. Users start at a home hub with primary destinations (conversation, notifications, queue, diff-viewer, settings) and can drill down into nested views. Navigation must be:
- Touch-optimized (48px minimum tap targets)
- Safe area aware (respects notches on iPhone X+, Android cutouts)
- Breadcrumb-driven (always show path back to home)
- Animated transitions (slide-in from right for drill-down, slide-out for back)
- Persistent FAB integration (FAB visible at all nav levels)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell layout structure
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNav.tsx` — existing mobile nav component (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx` — FAB component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/constants.ts` — Z_LAYERS for stacking context
- Material Design Navigation Drawer guidelines
- iOS Human Interface Guidelines for Navigation

## Acceptance Criteria
- [ ] `MobileNavHub` component with home hub view (5+ primary destinations)
- [ ] Primary destinations: Conversation, Notifications, Queue, Diff Viewer, Settings
- [ ] Nested navigation support: drill-down to child views (e.g., Queue → Active, Queue → Done)
- [ ] Breadcrumb trail at top of nav (Home > Queue > Active)
- [ ] Touch-optimized: 48px minimum tap target, 16px padding between items
- [ ] Safe area aware: env(safe-area-inset-top), env(safe-area-inset-bottom) applied
- [ ] Slide animations: slide-in (drill-down), slide-out (back), 250ms cubic-bezier easing
- [ ] Hub state persisted in localStorage (last visited path)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 12+ unit tests (navigation state, breadcrumbs, safe area) + 3 E2E tests
- [ ] Accessible: ARIA labels, focusable, keyboard navigable (arrow keys)

## Smoke Test
- [ ] On mobile viewport (375px): nav hub visible with 5 primary destinations
- [ ] Tap "Queue" → drill-down animation, breadcrumb shows "Home > Queue"
- [ ] Tap "Active" (child) → breadcrumb shows "Home > Queue > Active"
- [ ] Tap "Home" in breadcrumb → back to home hub
- [ ] On iPhone X viewport: safe area insets applied (no UI under notch)
- [ ] FAB remains visible and fixed during navigation

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNavHub.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/mobile-nav-hub.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/__tests__/MobileNavHub.test.tsx`
- TDD: tests first
- Max 400 lines for component
- Max 150 lines for CSS
- Max 200 lines for tests
- Use React.memo for performance
- No external UI libs — CSS-only animation
- localStorage key: `sd:mobile_nav_path`
