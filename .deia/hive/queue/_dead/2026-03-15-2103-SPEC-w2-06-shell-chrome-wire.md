# SPEC: Wire shell chrome menu renders tabs switch spotlight opens

## Priority
P1.10

## Model Assignment
haiku

## Objective
Wire shell chrome components: MenuBar renders with working menu items, ShellTabBar switches between workspaces, spotlight overlay opens with Ctrl+Shift+P. Connect to shell reducer actions.

## Acceptance Criteria
- [ ] MenuBar renders with menu items
- [ ] Tab switching works
- [ ] Spotlight overlay opens/closes
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-2103-SPEC-w2-06-shell-chrome-wire", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-06-shell-chrome-wire", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-06-shell-chrome-wire", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/
- [ ] No new test failures
