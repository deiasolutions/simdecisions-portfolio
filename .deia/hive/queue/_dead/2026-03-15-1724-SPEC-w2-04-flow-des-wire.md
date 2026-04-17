# SPEC: Wire flow designer to DES engine load then simulate then stream

## Priority
P1.00

## Model Assignment
sonnet

## Objective
Wire flow designer to DES simulation engine: load a flow, call /sim/start, events stream back to browser. Connect the flow designer run button to the DES engine routes. Display sim results in a results pane.

## Acceptance Criteria
- [ ] Run button calls /sim/start with current flow
- [ ] Simulation events stream to browser
- [ ] Results displayed in pane
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1724-SPEC-w2-04-flow-des-wire", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1724-SPEC-w2-04-flow-des-wire", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-1724-SPEC-w2-04-flow-des-wire", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] python -m pytest tests/hivenode/test_des_routes.py -v
- [ ] No new test failures
