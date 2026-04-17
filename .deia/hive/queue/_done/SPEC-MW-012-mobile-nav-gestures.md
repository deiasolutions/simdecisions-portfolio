# SPEC: Mobile-Nav Back Gesture + Drill-Down

## Priority
P2

## Depends On
MW-011

## Objective
Implement swipe-back gesture for mobile navigation (iOS-style edge swipe) and tap-to-drill-down navigation with animation feedback, velocity tracking, and cancel threshold.

## Context
Mobile users expect native-feeling gestures:
- Swipe from left edge → back to parent view (iOS edge swipe)
- Tap nav item → drill-down to child view (slide-in animation)
- Mid-swipe cancel: if swipe velocity is low or distance < 50%, cancel and snap back
- Visual feedback: nav pane follows finger during swipe, rubber-band effect at edges

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNavHub.tsx` — hub structure from MW-011
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/` — look for existing gesture hooks (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events for navigation
- React hooks for touch events (TouchEvent API)

## Acceptance Criteria
- [ ] `useSwipeBack` hook with TouchEvent handlers (touchstart, touchmove, touchend)
- [ ] Edge swipe detection: swipe must start within 20px of left edge
- [ ] Velocity tracking: measure swipe velocity (px/ms) to distinguish flick vs drag
- [ ] Distance threshold: if swipe distance > 50% viewport width OR velocity > 0.3px/ms → trigger back
- [ ] Cancel threshold: if distance < 50% AND velocity < 0.3px/ms → snap back to current view
- [ ] Visual feedback: nav pane follows finger (translate transform), 1:1 tracking
- [ ] Rubber-band effect: if already at home hub, allow slight overscroll then snap back
- [ ] Drill-down tap: tapping nav item triggers slide-in animation (250ms)
- [ ] Animation timing: cubic-bezier(0.4, 0.0, 0.2, 1) for smooth deceleration
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (gesture detection, velocity, thresholds) + 2 E2E tests
- [ ] Accessible: keyboard navigation (Escape = back, Enter = drill-down)

## Smoke Test
- [ ] On mobile viewport: swipe from left edge (>50% distance) → back animation triggered
- [ ] Swipe from left edge (20% distance) → snap back, no navigation
- [ ] Fast flick from left edge (high velocity) → back triggered immediately
- [ ] Tap "Queue" → drill-down animation (slide-in from right)
- [ ] At home hub, swipe left → rubber-band effect, no navigation

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeBack.ts` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/__tests__/useSwipeBack.test.ts`
- TDD: tests first
- Max 200 lines for hook
- Max 150 lines for tests
- No external gesture libs (no react-swipeable) — native TouchEvent API
- Use CSS transforms for 60fps animation (not position/margin)
- Debounce touchmove events (throttle to 16ms / 60fps)
