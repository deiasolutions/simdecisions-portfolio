# SPEC: Port shell chrome remaining (6 small components)

## Priority
P0.70

## Model Assignment
haiku

## Objective
Port 6 remaining shell chrome components (~281 lines): NotificationModal, ShortcutsPopup, LayoutSwitcher, PinnedPaneWrapper, MaximizedOverlay, dragDropUtils. Source: platform shell/. Target: browser/src/shell/components/.

## Acceptance Criteria
- [ ] All 6 components ported
- [ ] Tests written and passing
- [ ] No regressions in existing shell tests

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1402-SPEC-w1-14-shell-chrome-remaining", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/
- [ ] No new test failures
