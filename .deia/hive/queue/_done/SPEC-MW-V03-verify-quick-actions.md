# VERIFY: Quick-Actions FAB Integration

## Priority
P1

## Depends On
MW-007

## Objective
Comprehensive verification of QuickActions FAB: FAB component, mic button, keyboard button, animations, accessibility, and command execution flow.

## Context
MW-006 and MW-007 built the QuickActions FAB. This task verifies it works correctly end-to-end with real user interactions, animations, and error cases.

This is a VERIFY task — focused on testing, not building new features.

Files to verify:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions/QuickActions.tsx`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions/MicButton.tsx`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions/KeyboardButton.tsx`

## Acceptance Criteria
- [ ] E2E test: click FAB → expand → click mic → start listening → mock transcript → command executes
- [ ] E2E test: click FAB → expand → click keyboard → type command → submit → executes
- [ ] E2E test: click outside FAB when expanded → collapses
- [ ] Animation test: expand/collapse animations run smoothly (no jank, <16ms frame time)
- [ ] Accessibility test: tab navigation through FAB and action buttons
- [ ] Accessibility test: screen reader announces button states correctly
- [ ] Mobile test: touch FAB → touch mic → works on mobile viewport
- [ ] Mobile test: swipe down on expanded FAB → closes
- [ ] Error test: mic permission denied → shows error, offers keyboard fallback
- [ ] Integration test file: `browser/src/primitives/quick-actions/QuickActions.integration.test.tsx`
- [ ] All integration tests pass

## Smoke Test
- [ ] Run `npm test QuickActions.integration.test.tsx` — all tests pass
- [ ] Manual test: click FAB → expand animation smooth → click mic → listening state shows
- [ ] Manual test: click keyboard → modal opens → type command → executes
- [ ] Manual test (mobile emulator): touch FAB → touch mic → works

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/quick-actions/QuickActions.integration.test.tsx` (new file)
- 8-12 E2E test cases covering full FAB flow
- Max 300 lines for integration tests
- Use real component rendering (not shallow)
- Mock voice input and command execution
- Test output: clear pass/fail with animation performance metrics
