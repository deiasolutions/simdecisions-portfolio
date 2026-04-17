# SPEC: Notification-Pane Badges + Swipe

## Priority
P2

## Depends On
MW-014

## Objective
Add unread badge rendering to the notification pane and mobile-nav icon, plus swipe gestures for dismiss and archive actions.

## Context
Users need visual feedback for unread notifications:
- Badge on mobile-nav icon (red dot with unread count)
- Badge on each notification (blue dot for unread)
- Swipe-to-dismiss gesture (swipe left → dismiss notification)
- Swipe-to-archive gesture (swipe right → archive notification)
- Haptic feedback on swipe completion (if supported)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` — pane from MW-014
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/notificationStore.ts` — store from MW-014
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeBack.ts` — swipe gesture pattern from MW-012
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNavHub.tsx` — nav hub for badge placement

## Acceptance Criteria
- [ ] Unread badge on mobile-nav icon: red circle with white count (e.g., "5")
- [ ] Unread badge on each notification: blue dot (8px diameter) next to title
- [ ] Badge updates in real-time when notification is marked read
- [ ] `useSwipeNotification` hook for swipe gestures (based on useSwipeBack pattern)
- [ ] Swipe left (>50% width) → dismiss notification (remove from list, update count)
- [ ] Swipe right (>50% width) → archive notification (move to archive, update count)
- [ ] Visual feedback: notification card follows finger during swipe (translate transform)
- [ ] Swipe cancel: if distance < 50% → snap back to original position
- [ ] Haptic feedback: if Navigator.vibrate available → vibrate(50) on swipe complete
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (badge rendering, swipe gestures, haptics) + 2 E2E tests
- [ ] Accessible: badge has aria-label (e.g., "5 unread notifications")

## Smoke Test
- [ ] Open notification-pane → unread notifications have blue dot badge
- [ ] Mobile-nav icon shows red badge with count "3"
- [ ] Swipe left on notification → dismiss animation, notification removed, badge count decrements
- [ ] Swipe right on notification → archive animation, notification archived
- [ ] Swipe 30% left, release → snap back (no dismiss)
- [ ] On device with haptics: swipe complete → vibration

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeNotification.ts` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNavHub.tsx` (modify — add badge)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/__tests__/useSwipeNotification.test.ts`
- TDD: tests first
- Max 100 lines for hook
- Max 50 lines for badge CSS
- Max 150 lines for tests
- Badge must be CSS-only (no icon libs)
- Haptic feedback: check for Navigator.vibrate (graceful fallback if unsupported)
