# SPEC: Notification-Pane with Badges and Swipe Actions

## Priority
P1

## Objective
Design a notification pane component for the Mobile Workdesk that displays system notifications, build status, and hive updates with badge counts, swipe-to-dismiss, and tap-to-navigate actions.

## Context
The notification-pane is a destination hub in mobile-nav that aggregates notifications from:
- Build queue status (active bees, completed tasks, failures)
- System events (git push, deploy complete, test failures)
- Hive activity (new specs queued, dispatcher events)
- User mentions (in efemera channels, comments on tasks)

It must support:
- Notification badges on mobile-nav hub icon
- Swipe-to-dismiss individual notifications
- Tap-to-navigate (e.g., tap "Test failed" → navigate to test results)
- Read/unread states with visual distinction

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/status-bar/StatusBar.tsx` — status display patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/ProgressPane.tsx` — progress indicators
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_routes.py` — build status API endpoints
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:62` — task context

## Acceptance Criteria
- [ ] `NotificationPane` component with notification list rendering
- [ ] Data model: `{ id, type, title, body, timestamp, read, action_url }`
- [ ] Notification types: build, system, hive, mention (with icons)
- [ ] Badge count: unread count displayed on mobile-nav hub icon
- [ ] Swipe-to-dismiss: swipe notification right → mark as read, left → delete
- [ ] Tap-to-navigate: tap notification → execute action (navigate to URL, open modal, etc.)
- [ ] Read/unread visual states: bold title for unread, muted text for read
- [ ] Timestamp display: relative time ("2 min ago", "1 hour ago", "Yesterday")
- [ ] Empty state: "No notifications" with friendly icon
- [ ] Polling: fetch new notifications every 30 seconds (WebSocket fallback)
- [ ] Persistence: notification state saved to localStorage `mw_notifications`
- [ ] Accessibility: ARIA live region for new notifications, screen reader announcements
- [ ] 10+ unit tests + 2 E2E tests (swipe-to-dismiss, tap-to-navigate, badge update)

## Smoke Test
- [ ] Open notification pane → list of 5 notifications renders
- [ ] Unread badge shows "3" on mobile-nav hub icon
- [ ] Swipe notification right → marked as read, badge decrements to "2"
- [ ] Swipe notification left → deleted, badge decrements to "1"
- [ ] Tap notification → navigate to linked content (e.g., test results page)
- [ ] New notification arrives → badge increments, ARIA announcement

## Model Assignment
sonnet

## Depends On
None (Phase 0 spec)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/notification-pane.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/__tests__/NotificationPane.test.tsx`
- TDD: tests first
- Max 350 lines for component
- Max 100 lines for CSS
- Max 150 lines for tests
- CSS variables only, no hardcoded colors
- No external notification libs — custom polling + localStorage
- No stubs — full swipe gesture handling and navigation logic
