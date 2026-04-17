# SPEC: VERIFY Notification-Pane

## Priority
P2

## Depends On
MW-016

## Objective
Verify that the notification-pane system (data model, badges, swipe, tap-to-navigate) works correctly across all critical paths and edge cases.

## Context
This is a VERIFY task to ensure notification-pane is production-ready. All acceptance criteria from MW-014, MW-015, MW-016 must pass.

## Acceptance Criteria
- [ ] All unit tests pass (MW-014: 12, MW-015: 10, MW-016: 8) = 30 tests
- [ ] All E2E tests pass (MW-014: 3, MW-015: 2, MW-016: 2) = 7 tests
- [ ] Manual smoke test on 3+ viewports: iPhone SE, iPhone 14 Pro, iPad Mini
- [ ] Edge case: fetch notifications while offline → error state, retry button works
- [ ] Edge case: mark 50 notifications as read → unread count updates correctly
- [ ] Edge case: swipe notification while auto-refresh happens → no race condition
- [ ] Edge case: tap notification with invalid target → toast error, not marked as read
- [ ] Edge case: rapid taps on same notification (3 taps in 1 second) → only navigates once
- [ ] Performance: notification list with 100 items → smooth scrolling (60fps)
- [ ] Accessibility: keyboard navigation (Tab, Enter, Escape)

## Smoke Test
- [ ] Run all unit tests: `npm test -- notification-pane`
- [ ] Run all E2E tests: `npm run test:e2e -- notification-pane`
- [ ] Manual: fetch 50 notifications → list renders, unread badge shows correct count
- [ ] Manual: swipe left on 5 notifications → all dismissed, badge updates
- [ ] Manual: tap notification → navigate to correct context, marked as read

## Model Assignment
sonnet

## Constraints
- No new files — run existing tests
- If tests fail: fix the issue and re-run (do not mark complete until all tests pass)
- Document any edge cases found in response file
