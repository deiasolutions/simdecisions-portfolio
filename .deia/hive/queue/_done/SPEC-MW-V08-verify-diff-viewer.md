# SPEC: VERIFY Diff-Viewer

## Priority
P2

## Depends On
MW-022

## Objective
Verify that the diff-viewer system (parsing, collapse, swipe) works correctly across all critical paths and edge cases.

## Context
This is a VERIFY task to ensure diff-viewer is production-ready. All acceptance criteria from MW-020, MW-021, MW-022 must pass.

## Acceptance Criteria
- [ ] All unit tests pass (MW-020: 12, MW-021: 10, MW-022: 10) = 32 tests
- [ ] All E2E tests pass (MW-020: 3, MW-021: 2, MW-022: 2) = 7 tests
- [ ] Manual smoke test on 3+ viewports: iPhone SE, iPhone 14 Pro, iPad Mini
- [ ] Edge case: parse diff with 50 files → all files render correctly
- [ ] Edge case: parse diff with malformed hunk header → graceful fallback (skip hunk)
- [ ] Edge case: collapse all files, then reload → collapsed state persisted
- [ ] Edge case: swipe line while scrolling → no accidental stage/unstage
- [ ] Edge case: rapid swipes (5 swipes in 2 seconds) → no race conditions
- [ ] Performance: diff with 1000 lines → smooth scrolling (60fps)
- [ ] Accessibility: keyboard navigation (Tab, Enter, Ctrl+S, Ctrl+U, Ctrl+E)

## Smoke Test
- [ ] Run all unit tests: `npm test -- diff-viewer`
- [ ] Run all E2E tests: `npm run test:e2e -- diff-viewer`
- [ ] Manual: load diff with 10 files → all files render, collapse/expand works
- [ ] Manual: swipe line left → line staged, checkmark appears
- [ ] Manual: reload page → staged lines remain staged

## Model Assignment
sonnet

## Constraints
- No new files — run existing tests
- If tests fail: fix the issue and re-run (do not mark complete until all tests pass)
- Document any edge cases found in response file
