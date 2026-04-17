# SPEC: Port shell chrome GovernanceProxy + SpotlightOverlay + PaneMenu

## Priority
P0.65

## Model Assignment
haiku

## Objective
Port 3 shell chrome components (~361 lines): GovernanceProxy (approval modal for gate_enforcer), SpotlightOverlay (command palette overlay), PaneMenu (right-click context menu for panes). Source: platform shell/. Target: browser/src/shell/components/.

## Acceptance Criteria
- [ ] GovernanceProxy ported
- [ ] SpotlightOverlay ported
- [ ] PaneMenu ported
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1402-SPEC-w1-13-shell-chrome-governance", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/components/__tests__/
- [ ] No new test failures
