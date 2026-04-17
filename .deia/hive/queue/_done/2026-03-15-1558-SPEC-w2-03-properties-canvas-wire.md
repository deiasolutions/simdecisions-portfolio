# SPEC: Wire properties panel to canvas select then edit then update

## Priority
P0.95

## Model Assignment
sonnet

## Objective
Wire properties panel to canvas: clicking a node on canvas opens its properties in the properties panel. Editing a property updates the node on canvas in real-time. Uses bus events: node:selected, node:property-changed.

## Acceptance Criteria
- [ ] Clicking canvas node opens properties panel
- [ ] Editing property updates canvas node
- [ ] Bus events connected correctly
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1558-SPEC-w2-03-properties-canvas-wire", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1558-SPEC-w2-03-properties-canvas-wire", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-1558-SPEC-w2-03-properties-canvas-wire", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/
- [ ] No new test failures
