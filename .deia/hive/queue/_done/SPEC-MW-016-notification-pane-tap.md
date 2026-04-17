# SPEC: Notification-Pane Tap-to-Navigate

## Priority
P2

## Depends On
MW-015

## Objective
Implement tap-to-navigate functionality for notifications: tapping a notification marks it as read and navigates to the relevant context (e.g., build details, inventory item, error log).

## Context
Notifications should be actionable:
- Tap notification → mark as read + navigate to context
- Build event notification → navigate to build details pane (queue-pane with filter)
- Inventory update notification → navigate to feature detail view
- System alert notification → navigate to error log or settings
- Navigation uses RTD bus events (`bus.dispatch({ type: 'navigate', target: '...' })`)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` — pane from MW-014/015
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/notificationStore.ts` — store from MW-014
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell navigation handling

## Acceptance Criteria
- [ ] Tap notification → `notificationStore.markRead(id)` called
- [ ] Tap notification → `bus.dispatch({ type: 'navigate', target: '...' })` called
- [ ] Navigation target based on notification type:
  - build_event → queue-pane (filter by bee_id or task_id)
  - inventory_update → feature detail view (filter by feature_id)
  - system_alert → error log or settings
- [ ] Visual feedback: notification card highlights on tap (200ms)
- [ ] Navigation happens after mark-read completes (async, no race conditions)
- [ ] If navigation fails: show toast error (do not mark as read)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 8+ unit tests (tap handling, mark read, navigation) + 2 E2E tests
- [ ] Accessible: notification cards are buttons (semantic HTML) with aria-label

## Smoke Test
- [ ] Tap build_event notification → marked as read, navigate to queue-pane with filter
- [ ] Tap inventory_update notification → marked as read, navigate to feature detail
- [ ] Tap system_alert notification → marked as read, navigate to error log
- [ ] Badge count decrements after tap (unread → read)
- [ ] Tap notification with invalid target → toast error, notification NOT marked as read

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/notificationStore.ts` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/__tests__/NotificationPane.test.tsx` (modify)
- No new files
- TDD: tests first
- Max 100 lines of changes to NotificationPane.tsx
- Max 50 lines of changes to notificationStore.ts
- Use semantic HTML: notification cards must be <button> elements (not <div>)
- Navigation must be idempotent (tapping twice does not navigate twice)
