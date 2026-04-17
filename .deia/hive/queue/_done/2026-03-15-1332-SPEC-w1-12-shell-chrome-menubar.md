# SPEC: Port shell chrome MenuBar + ShellTabBar + WorkspaceBar

## Priority
P0.60

## Model Assignment
sonnet

## Objective
Port 3 shell chrome components (~906 lines): MenuBar (app menu with File/Edit/View/Help), ShellTabBar (workspace tabs), WorkspaceBar (workspace selector). Source: platform shell/components/. Target: browser/src/shell/components/.

## Acceptance Criteria
- [ ] MenuBar component ported with menu structure
- [ ] ShellTabBar component ported
- [ ] WorkspaceBar component ported
- [ ] All use var(--sd-*) CSS variables
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1332-SPEC-w1-12-shell-chrome-menubar", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/components/__tests__/
- [ ] No new test failures
