# SPEC: Wire DES events to canvas tokens move nodes light up

## Priority
P1.05

## Model Assignment
sonnet

## Objective
Wire DES simulation events to canvas visualization: tokens move along edges, active nodes light up, resources change color based on utilization. Uses animation system from w1-07.

## Acceptance Criteria
- [ ] Token animations follow simulation events
- [ ] Active nodes highlight during simulation
- [ ] Resource nodes show utilization colors
- [ ] Animation playback controls work
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-2103-SPEC-w2-05-des-canvas-visual", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-05-des-canvas-visual", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-05-des-canvas-visual", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/
- [ ] No new test failures
