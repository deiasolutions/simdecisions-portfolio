# SPEC: VERIFY Mobile-Nav

## Priority
P2

## Depends On
MW-013

## Objective
Verify that the mobile navigation system (hub structure, gestures, FAB integration) works correctly across all critical paths, edge cases, and device types.

## Context
This is a VERIFY task to ensure mobile-nav is production-ready. All acceptance criteria from MW-011, MW-012, MW-013 must pass, plus additional E2E tests for cross-device compatibility.

## Acceptance Criteria
- [ ] All unit tests pass (MW-011: 12, MW-012: 10, MW-013: 8) = 30 tests
- [ ] All E2E tests pass (MW-011: 3, MW-012: 2, MW-013: 2) = 7 tests
- [ ] Manual smoke test on 3+ viewports: iPhone SE (375x667), iPhone 14 Pro (393x852), iPad Mini (768x1024)
- [ ] Edge case: swipe-back at home hub → rubber-band effect (no crash)
- [ ] Edge case: drill-down to 5 levels deep → breadcrumb truncates gracefully
- [ ] Edge case: rapid swipe gestures (3+ swipes in 1 second) → no race conditions
- [ ] Edge case: landscape orientation → FAB repositions to center-bottom
- [ ] Edge case: FAB expanded while navigating → FAB menu stays above nav pane
- [ ] Performance: 60fps animations (check Chrome DevTools Performance tab)
- [ ] Accessibility: keyboard navigation works (Tab, Enter, Escape, Arrow keys)

## Smoke Test
- [ ] Run all unit tests: `npm test -- mobile-nav`
- [ ] Run all E2E tests: `npm run test:e2e -- mobile-nav`
- [ ] Manual: iPhone 14 Pro viewport → nav hub loads, swipe-back works, FAB visible
- [ ] Manual: iPad Mini landscape → FAB repositions to center-bottom
- [ ] Manual: rapid swipes (5 swipes in 2 seconds) → no crash, no UI jank

## Model Assignment
sonnet

## Constraints
- No new files — run existing tests
- If tests fail: fix the issue and re-run (do not mark complete until all tests pass)
- Document any edge cases found in response file
- If performance < 60fps: profile and optimize (mark as issue if cannot fix)
