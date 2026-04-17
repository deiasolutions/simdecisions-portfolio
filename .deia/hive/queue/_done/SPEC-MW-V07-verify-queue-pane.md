# SPEC: VERIFY Queue-Pane

## Priority
P2

## Depends On
MW-019

## Objective
Verify that the queue-pane system (fetch, display, actions) works correctly across all critical paths and edge cases.

## Context
This is a VERIFY task to ensure queue-pane is production-ready. All acceptance criteria from MW-017, MW-018, MW-019 must pass.

## Acceptance Criteria
- [ ] All unit tests pass (MW-017: 12, MW-018: 10, MW-019: 10) = 32 tests
- [ ] All E2E tests pass (MW-017: 3, MW-018: 2, MW-019: 2) = 7 tests
- [ ] Manual smoke test on 3+ viewports: iPhone SE, iPhone 14 Pro, iPad Mini
- [ ] Edge case: fetch queue while offline → error state, retry button works
- [ ] Edge case: cancel task while auto-refresh happens → no race condition
- [ ] Edge case: retry failed task → task re-queued, status updates correctly
- [ ] Edge case: view response for task with no response file → error toast
- [ ] Edge case: long-press on 100-item list → action menu appears, no UI jank
- [ ] Performance: queue list with 100 tasks → smooth scrolling (60fps)
- [ ] Accessibility: keyboard navigation (Tab, Enter, Escape)

## Smoke Test
- [ ] Run all unit tests: `npm test -- queue-pane`
- [ ] Run all E2E tests: `npm run test:e2e -- queue-pane`
- [ ] Manual: fetch 50 tasks → list renders, filter by "Active" works
- [ ] Manual: long-press active task → cancel action, confirmation dialog appears
- [ ] Manual: retry failed task → task re-queued, toast "Task retried"

## Model Assignment
sonnet

## Constraints
- No new files — run existing tests
- If tests fail: fix the issue and re-run (do not mark complete until all tests pass)
- Document any edge cases found in response file
