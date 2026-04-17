# SPEC: Wire governance GovernanceProxy shows approval modal

## Priority
P1.30

## Model Assignment
haiku

## Objective
Wire GovernanceProxy: when gate_enforcer returns warn or ask disposition, show approval modal to user. User can approve or reject. Result fed back to gate_enforcer.

## Acceptance Criteria
- [ ] Approval modal appears on warn/ask dispositions
- [ ] User can approve or reject
- [ ] Result propagated to gate_enforcer
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-16-1007-SPEC-w2-10-governance-visual", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-16-1007-SPEC-w2-10-governance-visual", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-16-1007-SPEC-w2-10-governance-visual", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/
- [ ] No new test failures
