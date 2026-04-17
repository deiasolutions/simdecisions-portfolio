# SPEC: Find and port kanban board component (BL-071)

## Priority
P0.80

## Model Assignment
sonnet

## Objective
Find the kanban board component in the platform repo and port it to shiftcenter. BL-071. The kanban should be a pane-compatible applet that renders columns (To Do, In Progress, Done) with draggable cards. Source: find in platform. Target: browser/src/apps/kanban/.

## Acceptance Criteria
- [ ] Kanban board component ported
- [ ] Columns render with cards
- [ ] Drag and drop between columns works
- [ ] Registered as a pane applet
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1519-SPEC-w1-16-kanban-board", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/kanban/
- [ ] No new test failures
