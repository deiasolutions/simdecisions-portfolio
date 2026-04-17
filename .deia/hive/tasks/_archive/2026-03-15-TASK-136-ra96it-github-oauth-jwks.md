# TASK-136: Port GitHub OAuth + JWKS into ra96it

## Objective
Port GitHub OAuth flow and dev-login bypass from platform/efemera into ra96it service, add JWKS endpoint for public key distribution, upgrade JWT claims to family-wide audience.

## Context
The platform repo (`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\`) has a fully working GitHub OAuth system with 13+ tests. ra96it already has RS256 JWT, bcrypt, MFA, and refresh token rotation. This task ports the OAuth code into ra96it and adds JWKS for cross-app JWT verification.

**Key platform patterns to preserve:**
- State encoding: `base64(JSON({origin, nonce}))`
- Allowed origins list (updated for deiasolutions family domains)
- Admin elevation via `ADMIN_GITHUB_LOGINS` env var (comma-separated GitHub handles)
- Dev-login bypass: only available when `is_local_mode and not GITHUB_CLIENT_ID`
- MFA optional for OAuth users (GitHub already verified email)

**Key ra96it patterns to preserve:**
- RS256 JWT (already in `ra96it/services/jwt.py`)
- Bcrypt password hashing (already in `ra96it/services/password.py`)
- Audit logging via `ra96it/services/audit.py`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\auth\routes.py` (lines 60-247: GitHub OAuth, lines 250-275: dev-login)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\auth\models.py` (User model with github_id, provider)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\test_github_oauth.py` (13 OAuth tests to port)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\config.py` (current settings)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\models.py` (User model to extend)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\services\jwt.py` (existing RS256 JWT)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\main.py` (route registration)

## Deliverables

### Backend Code
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\oauth.py` — Port GitHub OAuth endpoints from platform:
  - GET `/oauth/github/login?origin=<url>` — returns GitHub auth URL with state
  - GET `/oauth/github/callback?state=<state>&code=<code>` — exchanges code, creates/updates user, redirects with JWT
  - POST `/oauth/github/exchange` (body: `{code, origin}`) — SPA code exchange, returns JSON with JWT
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\jwks.py` — JWKS endpoint:
  - GET `/.well-known/jwks.json` — returns RS256 public key in JWK format (RFC 7517)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\dev_login.py` — Dev-login bypass (local mode only):
  - GET `/dev-login/available` — returns `{available: bool}`
  - POST `/dev-login` — mints JWT for local-user (only when `mode=local` and no `GITHUB_CLIENT_ID`)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\services\github.py` — GitHub API client:
  - `exchange_code_for_token(code: str, redirect_uri: str) -> str` — calls GitHub OAuth token endpoint
  - `get_user_profile(access_token: str) -> dict` — calls GitHub user API
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\models.py`:
  - Add `github_id: Mapped[Optional[str]]` (unique, indexed)
  - Add `provider: Mapped[str]` (default="email", check constraint: email/github/bot/local)
  - Add `email_verified: Mapped[bool]` (default=False)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\schemas.py`:
  - Add `OAuthCallbackRequest(code: str, state: str, origin: str | None)`
  - Add `OAuthExchangeRequest(code: str, origin: str | None)`
  - Add `OAuthTokenResponse(access_token: str, user: UserResponse, github_token: str | None, github_scopes: str | None)`
  - Add `DevLoginAvailableResponse(available: bool)`
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\config.py`:
  - Add `github_client_id: Optional[str]`
  - Add `github_client_secret: Optional[str]`
  - Add `github_redirect_uri: str = "http://localhost:8021/oauth/github/callback"`
  - Add `frontend_url: str = "http://localhost:5174"`
  - Add `admin_github_logins: str = ""` (comma-separated)
  - Add `mode: str = "local"` (local/remote/cloud)
  - Add `allowed_origins: list[str]` property that returns the deiasolutions family domains
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\services\jwt.py`:
  - Add `provider: str | None = None` param to `create_access_token()`
  - Add `provider_id: str | None = None` param (github_id for GitHub users)
  - Add `display_name: str | None = None` param
  - Add `scope: str = "chat"` param (default: chat, options: chat/terminal/api)
  - Update `jwt_audience` default from `"shiftcenter"` to `"deiasolutions"` (family-wide)
  - Include all extra claims in payload
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\main.py`:
  - Register oauth, jwks, dev_login routers
  - Keep existing register, login, mfa, token routers

### Tests (TDD — write tests FIRST)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\tests\test_oauth.py` — Port 13+ OAuth tests from platform:
  - `test_github_login_url` — validates state encoding, returns GitHub auth URL
  - `test_github_callback_creates_new_user` — exchanges code, creates user with github_id, returns JWT
  - `test_github_callback_updates_existing_user_by_github_id` — finds user by github_id, updates email/display_name
  - `test_github_callback_links_existing_email_user` — finds user by email, sets github_id, upgrades provider
  - `test_github_callback_redirects_with_token` — validates redirect URL format
  - `test_github_callback_validates_state_origin` — rejects unauthorized origins
  - `test_github_callback_handles_missing_code` — returns error redirect
  - `test_github_callback_handles_github_error` — returns error redirect
  - `test_github_exchange_returns_json_token` — SPA code exchange
  - `test_admin_elevation_via_github_login` — user in ADMIN_GITHUB_LOGINS gets tier=admin
  - `test_oauth_user_email_verified_true` — GitHub users are auto-verified
  - `test_oauth_user_mfa_optional` — GitHub users can skip MFA (email already verified by GitHub)
  - `test_github_callback_invalid_state_format` — rejects malformed state
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\tests\test_jwks.py`:
  - `test_jwks_endpoint_returns_valid_jwk` — validates JWK structure (kty, use, alg, n, e)
  - `test_jwks_public_key_verifies_jwt` — create JWT with private key, verify with JWKS public key
  - `test_jwks_caching` — validates JWKS response includes cache headers
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\tests\test_dev_login.py`:
  - `test_dev_login_available_when_local_no_github` — mode=local, no GITHUB_CLIENT_ID → available=true
  - `test_dev_login_unavailable_when_github_configured` — GITHUB_CLIENT_ID set → available=false
  - `test_dev_login_unavailable_when_cloud_mode` — mode=cloud → available=false
  - `test_dev_login_mints_jwt_for_local_user` — POST /dev-login returns valid JWT with sub=local-user
  - `test_dev_login_rejects_when_unavailable` — 403 when mode=cloud or GITHUB_CLIENT_ID set

### Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All 21+ tests pass (13 OAuth + 3 JWKS + 5 dev-login)
- [ ] Mock GitHub API calls (use `httpx.AsyncClient` with `transport=httpx.MockTransport`)
- [ ] Test both local and cloud modes
- [ ] Test admin elevation
- [ ] Test state validation (nonce replay protection)
- [ ] Test email verified flag for OAuth users
- [ ] Edge cases: invalid state, missing code, GitHub API errors, unauthorized origins

### Environment Variables (New)
```bash
# GitHub OAuth
RA96IT_GITHUB_CLIENT_ID=...
RA96IT_GITHUB_CLIENT_SECRET=...
RA96IT_GITHUB_REDIRECT_URI=http://localhost:8021/oauth/github/callback
RA96IT_FRONTEND_URL=http://localhost:5174
RA96IT_ADMIN_GITHUB_LOGINS=davee,other-admin

# Mode (local/remote/cloud)
RA96IT_MODE=local
```

## Constraints
- No file over 500 lines (Rule 4)
- NO STUBS (Rule 6) — every function fully implemented
- TDD (Rule 5) — tests first, then implementation
- All file paths must be absolute (Rule 8)
- Port existing code — do NOT rewrite from scratch (Briefing directive)
- Use bcrypt for password hashing (already in ra96it, NOT SHA-256 like platform)
- Keep RS256 JWT (already in ra96it, NOT HS256 like platform)
- Keep existing refresh token rotation + MFA patterns
- OAuth users: email_verified=True, mfa optional (GitHub already verified)

## Acceptance Criteria
- [ ] GET `/.well-known/jwks.json` returns valid JWK with RS256 public key
- [ ] GET `/oauth/github/login?origin=http://localhost:5174` returns GitHub auth URL with base64-encoded state
- [ ] GET `/oauth/github/callback?state=<valid>&code=<valid>` creates user, returns redirect with JWT in query param
- [ ] POST `/oauth/github/exchange` (body: `{code, origin}`) returns JSON with JWT, user, github_token
- [ ] GitHub users created with: `provider="github"`, `email_verified=True`, `github_id=<github_user_id>`
- [ ] User in `ADMIN_GITHUB_LOGINS` gets `tier="admin"` on OAuth login
- [ ] GET `/dev-login/available` returns `{available: true}` when `mode=local` and no `GITHUB_CLIENT_ID`
- [ ] POST `/dev-login` returns JWT for local-user (only when dev-login available)
- [ ] JWT claims include: `sub`, `email`, `tier`, `provider`, `provider_id`, `display_name`, `scope`, `iat`, `exp`, `iss=ra96it`, `aud=deiasolutions`
- [ ] All 21+ tests pass
- [ ] No hardcoded secrets in source
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-136-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
