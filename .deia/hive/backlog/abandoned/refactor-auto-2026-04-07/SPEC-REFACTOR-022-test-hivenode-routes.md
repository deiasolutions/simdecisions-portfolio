---
id: REFACTOR-022
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-013
---
# SPEC-REFACTOR-022: Test Hivenode Routes — All Endpoints Respond Correctly

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-013

## Intent
Test every FastAPI route in hivenode. For routes that can be tested without a running server (via TestClient), test them. For routes requiring external services, verify the code is syntactically correct and imports resolve.

## Files to Read First
- `.deia/hive/refactor/inventory-routes.json` — route list from REFACTOR-010
- `hivenode/main.py` — app setup and router includes
- `hivenode/routes/` — all route modules

## Acceptance Criteria
- [ ] For each route in inventory-routes.json:
  - Module imports cleanly? (yes/no)
  - Route handler defined? (yes/no)
  - TestClient test exists? (yes/no, with path)
  - TestClient result (pass/fail/skip)
- [ ] File created: `.deia/hive/refactor/test-results-routes.json`
- [ ] Summary: X routes tested, Y passing, Z failing, W skipped

## Constraints
- You are in EXECUTE mode. Run tests and write results. Do NOT enter plan mode.
- Use httpx TestClient for route testing where possible
- If server required, mark as "requires-server" and verify code-level correctness only
- No git operations
