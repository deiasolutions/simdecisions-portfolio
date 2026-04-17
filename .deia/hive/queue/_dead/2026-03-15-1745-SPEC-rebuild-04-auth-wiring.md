# SPEC: Rebuild auth/identity wiring (ra96it OAuth + JWKS + hivenode auth)

## Priority
P0.20

## Model Assignment
sonnet

## Objective
Re-apply auth wiring changes from TASK-136, TASK-137, TASK-138 that were lost in a git reset. This is the most complex rebuild — multiple files across ra96it, hivenode, and browser.

### TASK-136 changes (ra96it GitHub OAuth + JWKS)
- `ra96it/models.py` — add github_id, provider, email_verified columns to User model
- `ra96it/schemas.py` — add OAuth Pydantic schemas
- `ra96it/config.py` — add GitHub OAuth settings, mode setting, allowed_origins
- `ra96it/services/jwt.py` — add provider, provider_id, display_name parameters
- `ra96it/main.py` — register oauth, jwks, dev_login routers

### TASK-137 changes (browser auth adapter)
- `browser/src/apps/index.ts` — add AuthAdapter import and registerApp call

### TASK-138 changes (hivenode JWKS cache)
- `hivenode/dependencies.py` — add JWKS cache initialization, update verify_jwt
- `hivenode/config.py` — add ra96it_jwks_url setting
- `hivenode/main.py` — import JWKSCache, initialize in lifespan
- `hivenode/routes/auth.py` — fix identity route default mode
- `tests/hivenode/conftest.py` — add JWKS cache in fixtures
- `tests/hivenode/test_auth_routes.py` — add 6 new test cases

## Recovery Sources
Read ALL of these — they describe the changes:
- `.deia/hive/responses/20260315-TASK-136-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-137-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-138-RESPONSE.md`
- `.deia/hive/tasks/2026-03-15-TASK-136-ra96it-github-oauth-jwks.md`
- `.deia/hive/tasks/2026-03-15-TASK-137-browser-auth-primitive-login-egg.md`
- `.deia/hive/tasks/2026-03-15-TASK-138-hivenode-jwks-cache-family-aud.md`

Feature inventory: `FEAT-137` (323 tests)

Also reference platform source if response files lack detail:
- `platform/ra96it/` for OAuth/JWKS patterns
- `platform/efemera/src/efemera/auth/` for hivenode auth patterns

**CRITICAL: Read surviving test files — they define the expected behavior:**
- `tests/hivenode/test_auth_routes.py` — shows the auth endpoints and expected responses (at HEAD, plus 6 new tests from TASK-138 that need re-adding)
- `browser/src/primitives/auth/__tests__/` — LoginPage and authStore tests (check if these exist or were modifications)
- `browser/src/services/identity/__tests__/identityService.test.ts` — identity service behavior spec (was modified, now at HEAD)

**Also read the surviving source files:**
- `ra96it/services/audit.py` — was modified, check current state
- `browser/src/apps/authAdapter.tsx` — was modified, check what apps/index.ts needs

## Acceptance Criteria
- [ ] ra96it models have github_id, provider, email_verified columns
- [ ] ra96it has OAuth schemas in schemas.py
- [ ] ra96it config has GitHub OAuth settings
- [ ] ra96it main.py registers oauth, jwks, dev_login routers
- [ ] hivenode has JWKS cache in dependencies.py
- [ ] hivenode config has ra96it_jwks_url
- [ ] hivenode lifespan initializes JWKSCache
- [ ] browser/src/apps/index.ts has AuthAdapter registered
- [ ] All existing auth tests pass
- [ ] New auth tests from TASK-138 pass (6 tests)
- [ ] No import errors on startup

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-04-auth-wiring", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-04-auth-wiring", "files": ["ra96it/models.py", "ra96it/schemas.py", "ra96it/config.py", "ra96it/services/jwt.py", "ra96it/main.py", "browser/src/apps/index.ts", "hivenode/dependencies.py", "hivenode/config.py", "hivenode/main.py", "hivenode/routes/auth.py"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
