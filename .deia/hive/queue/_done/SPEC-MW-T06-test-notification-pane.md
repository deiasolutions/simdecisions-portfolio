# SPEC: TEST — Notification-Pane Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the NotificationPane component that validates notification rendering, badge counts, swipe actions, tap-to-navigate, and polling with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-014/MW-015/MW-016 implementation.

Test coverage must include:
- Component render: notification list displays
- Badge count: unread count displayed correctly
- Swipe-to-dismiss: swipe right → mark as read, swipe left → delete
- Tap-to-navigate: tap notification → action executed
- Read/unread states: visual distinction between read and unread
- Timestamp display: relative time formatting
- Empty state: "No notifications" message
- Polling: new notifications fetched every 30 seconds
- Persistence: notification state saved to localStorage

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S06-notification-pane.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/status-bar/__tests__/StatusBar.test.tsx` — test patterns (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:74` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/notification-pane/__tests__/NotificationPane.test.tsx` (Jest + React Testing Library)
- [ ] 10+ test cases covering: render, badge, swipe, tap, states, timestamp, empty, polling, persistence
- [ ] Test render: 5 notifications displayed in list
- [ ] Test badge count: unread count "3" displayed on badge
- [ ] Test swipe right: swipe gesture marks notification as read, badge decrements
- [ ] Test swipe left: swipe gesture deletes notification, badge decrements
- [ ] Test tap-to-navigate: click notification → onNavigate callback called with action_url
- [ ] Test read/unread: unread notification has bold title, read has muted text
- [ ] Test timestamp: "2 min ago" formatting for recent notifications
- [ ] Test empty state: 0 notifications → "No notifications" message displayed
- [ ] Test polling: jest.useFakeTimers() → advance 30s → fetch called again
- [ ] Test persistence: mark as read → localStorage `mw_notifications` updated
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test NotificationPane.test.tsx` → 10+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts 5 notifications displayed
- [ ] Check test_badge() → asserts badge count === 3
- [ ] Check test_swipe_right() → asserts read state updated, badge decremented
- [ ] Check test_polling() → asserts fetch called after 30s
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S06

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/__tests__/NotificationPane.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 250 lines for test file
- Use @testing-library/react for component testing
- Use jest.useFakeTimers() for polling tests
- Use fireEvent for swipe gesture simulation
- Mock localStorage and fetch API
- No implementation code in this task — tests only
- Tests must be runnable even if `NotificationPane.tsx` doesn't exist yet (import should handle missing module gracefully)
