# TASK-135: ra96it SSO Phase 3 — Wire ShiftCenter to ra96it

## Objective

Wire ShiftCenter's backend and frontend to the ra96it federation service. Update JWT verification to validate ra96it tokens (fetch JWKS), add auth middleware for protected routes, integrate LoginPage with token exchange flow, preserve dev-mode bypass on localhost.

## Context

This is Phase 3 (final phase) of the ra96it SSO federation system:
1. **Phase 1 (TASK-133):** Login page + auth store (browser-only) — COMPLETE
2. **Phase 2 (TASK-134):** ra96it service (backend, separate repo) — COMPLETE
3. **Phase 3 (this task):** Wire ShiftCenter to ra96it (backend + frontend integration)

After this task:
- ShiftCenter backend validates ra96it JWTs via JWKS
- ShiftCenter frontend exchanges Efemera tokens for ra96it tokens
- Protected routes redirect unauthenticated users to /login
- Dev mode still bypasses auth on localhost

## Dependencies

- **TASK-133** (LoginPage + authStore) — MUST be complete
- **TASK-134** (ra96it service) — MUST be complete and deployed/running
- **Efemera GitHub OAuth** (already exists) — provides initial identity

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — verify_jwt() and verify_jwt_or_local() (lines 161-264)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — HivenodeConfig (lines 50-52, 166-172)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — from TASK-133
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — from TASK-133
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-14-2200-SPEC-ra96it-sso-federation.md` — full spec

## Deliverables

### Backend Updates (hivenode)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — verify_jwt()
  - Change issuer check from `"ra96it"` to `"ra96it.com"` (match spec)
  - Change audience check from `"shiftcenter"` to `"deiasolutions"` (family scope)
  - Fetch JWKS from ra96it service: `GET {ra96it_url}/.well-known/jwks.json`
  - Cache JWKS in memory (refresh every 6 hours or on verification failure)
  - Use PyJWT with JWKS to verify signature
  - Keep existing exception handling (ExpiredSignatureError, InvalidSignatureError, etc.)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — HivenodeConfig
  - Add `ra96it_url: Optional[str] = None` field (default: `"http://localhost:8421"` for local, `"https://ra96it.com"` for cloud)
  - Update `get_ra96it_public_key()` to fetch from JWKS instead (or keep for backward compat)
  - Add `get_ra96it_jwks_url() -> str` method (returns `{ra96it_url}/.well-known/jwks.json`)

- [ ] Add `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\services\jwks_cache.py` — JWKS caching
  - `fetch_jwks(url: str) -> dict` — fetch JWKS from URL, cache in-memory
  - `get_jwks(url: str) -> dict` — return cached JWKS or fetch if expired/missing
  - `verify_jwt_with_jwks(token: str, jwks_url: str, issuer: str, audience: str) -> dict` — verify JWT using JWKS
  - Cache TTL: 6 hours
  - Use httpx for HTTP calls (async)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` — auth routes
  - Keep existing routes: `/auth/verify`, `/auth/whoami`, `/auth/identity`
  - All routes now validate ra96it JWTs (via updated verify_jwt)
  - `/auth/identity` still bypasses on local mode (verify_jwt_or_local)

- [ ] Add auth middleware (optional — if time permits)
  - Middleware that checks JWT on all /api/* routes
  - Returns 401 if JWT missing/invalid
  - Bypasses on local mode
  - Excludes public routes: /health, /auth/*, /.well-known/*

### Frontend Updates (browser)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
  - Add `exchangeEfemeraToken(efemeraToken: string) -> Promise<string>` — call ra96it `/token/exchange`, return ra96it JWT
  - Add `validateToken(token: string) -> Promise<boolean>` — call ra96it `/token/validate`
  - Add `refreshAuthToken() -> Promise<string>` — placeholder (returns current token, future: refresh logic)
  - Update `isAuthenticated()` to check token expiry (decode JWT, check `exp` claim)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
  - GitHub OAuth button: redirect to `{ra96itUrl}/authorize?app=shiftcenter&redirect={currentUrl}`
  - On return from OAuth: extract token from URL param, save to localStorage
  - Dev-login button: generate dev token locally (keep existing behavior)
  - Show authenticated state: display user email and display_name from JWT claims
  - Add "Logout" button: calls `deleteAuthToken()`, redirects to /login

- [ ] Add `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\authService.ts` — Auth API client
  - `exchangeToken(efemeraToken: string) -> Promise<TokenResponse>` — POST to ra96it /token/exchange
  - `validateToken(token: string) -> Promise<ValidateResponse>` — POST to ra96it /token/validate
  - `getUserInfo(token: string) -> Promise<UserInfoResponse>` — GET ra96it /userinfo with Authorization header
  - Use fetch() or httpx wrapper

- [ ] Add HTTP interceptor for auth headers
  - Attach `Authorization: Bearer {token}` header to all hivenode API calls
  - Read token from authStore.loadAuthToken()
  - Skip on /auth/* routes (avoid infinite loop)
  - Redirect to /login on 401 response

### Environment Configuration

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.env.example`
  - Add `HIVENODE_RA96IT_URL=http://localhost:8421` (for local dev)
  - Add `HIVENODE_RA96IT_URL=https://ra96it.com` (comment for production)

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\.env.example`
  - Add `VITE_RA96IT_URL=http://localhost:8421` (for local dev)
  - Add `VITE_RA96IT_URL=https://ra96it.com` (comment for production)

### Documentation

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\AUTH.md` — auth documentation
  - Explain ra96it federation architecture
  - Explain token flow: Efemera → ra96it → ShiftCenter
  - Explain dev mode bypass
  - Explain JWT claims structure
  - Explain JWKS verification
  - Explain how to run locally (need ra96it service running)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 18 tests across all test files

### Test Files

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_jwks_cache.py`
  - Test fetch_jwks() success
  - Test fetch_jwks() failure (network error)
  - Test JWKS caching (second call doesn't refetch)
  - Test JWKS expiry (refetch after TTL)
  - Test verify_jwt_with_jwks() success
  - Test verify_jwt_with_jwks() invalid signature
  - Test verify_jwt_with_jwks() expired token

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_ra96it_integration.py`
  - Test verify_jwt() with valid ra96it JWT
  - Test verify_jwt() with invalid signature
  - Test verify_jwt() with expired JWT
  - Test verify_jwt() with wrong issuer
  - Test verify_jwt() with wrong audience
  - Test verify_jwt_or_local() bypasses on local mode
  - Test verify_jwt_or_local() requires JWT on cloud mode

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authService.test.ts`
  - Test exchangeToken() success
  - Test exchangeToken() network error
  - Test validateToken() success
  - Test getUserInfo() success
  - Test getUserInfo() 401 error

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage-integration.test.tsx`
  - Test GitHub OAuth button redirects to ra96it (mock)
  - Test dev-login button generates dev token
  - Test authenticated state shows user info
  - Test logout button clears token
  - Test token exchange flow (mock ra96it API)

## Acceptance Criteria

- [ ] `verify_jwt()` validates ra96it JWTs via JWKS
- [ ] `verify_jwt()` accepts issuer: "ra96it.com" and audience: "deiasolutions"
- [ ] `verify_jwt_or_local()` still bypasses auth on localhost
- [ ] JWKS fetched from ra96it service and cached (6-hour TTL)
- [ ] LoginPage GitHub OAuth button redirects to ra96it /authorize
- [ ] Token exchange flow works: Efemera token → ra96it token → localStorage
- [ ] All hivenode API calls include `Authorization: Bearer {token}` header
- [ ] 401 responses redirect to /login
- [ ] Dev mode still works without ra96it running (localhost bypass)
- [ ] Authenticated state shows user email and display_name
- [ ] Logout button clears token and redirects to /login
- [ ] All 18+ tests pass
- [ ] No file over 500 lines
- [ ] No stubs — all functions fully implemented
- [ ] Documentation updated with ra96it integration

## Constraints

- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **TDD.** Tests first, then implementation. No exceptions.
- **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies.
- **No hardcoded URLs.** Use environment variables for ra96it URL.
- **Dev mode must still work.** `verify_jwt_or_local()` bypasses on localhost.
- **No breaking changes.** Existing routes must continue to work.

## Implementation Notes

### JWKS Caching Strategy

```python
# In-memory cache with TTL
_jwks_cache = {
    "url": None,
    "jwks": None,
    "fetched_at": None,
    "ttl": 6 * 60 * 60  # 6 hours in seconds
}

async def get_jwks(url: str) -> dict:
    now = time.time()
    if _jwks_cache["url"] == url and _jwks_cache["jwks"] and (now - _jwks_cache["fetched_at"]) < _jwks_cache["ttl"]:
        return _jwks_cache["jwks"]

    # Fetch fresh JWKS
    jwks = await fetch_jwks(url)
    _jwks_cache["url"] = url
    _jwks_cache["jwks"] = jwks
    _jwks_cache["fetched_at"] = now
    return jwks
```

### JWT Verification with JWKS

Use PyJWT's `PyJWKClient`:

```python
from jwt import PyJWKClient, decode

jwks_client = PyJWKClient(jwks_url)
signing_key = jwks_client.get_signing_key_from_jwt(token)

payload = decode(
    token,
    signing_key.key,
    algorithms=["RS256"],
    audience="deiasolutions",
    issuer="ra96it.com"
)
```

### HTTP Interceptor Pattern (Frontend)

```typescript
// In authStore.ts or httpClient.ts
const originalFetch = window.fetch;
window.fetch = async (url, options) => {
  // Skip auth routes
  if (url.includes('/auth/')) {
    return originalFetch(url, options);
  }

  // Attach auth header
  const token = loadAuthToken();
  if (token) {
    options.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    };
  }

  const response = await originalFetch(url, options);

  // Redirect on 401
  if (response.status === 401 && !window.location.pathname.includes('/login')) {
    window.location.href = '/login';
  }

  return response;
};
```

Or use axios/httpx interceptors if available.

### OAuth Redirect Flow

1. User clicks "Login with GitHub" button
2. Frontend redirects to: `https://ra96it.com/authorize?app=shiftcenter&redirect=https://code.shiftcenter.com/callback`
3. ra96it redirects to Efemera GitHub OAuth
4. User authorizes, Efemera redirects back to ra96it
5. ra96it issues JWT, redirects back to: `https://code.shiftcenter.com/callback?token={jwt}`
6. Frontend extracts token from URL param, saves to localStorage
7. Frontend redirects to /chat or wherever user was going

### Dev Mode URL Override

In dev mode (`HIVENODE_MODE=local`), ra96it URL should be `http://localhost:8421`. In production, `https://ra96it.com`.

Frontend reads from `VITE_RA96IT_URL` env var.

### Backward Compatibility

Existing code that uses `verify_jwt()` should continue to work. The only change is the JWKS fetch (instead of loading public key from file). If ra96it is not running, local mode bypass still works via `verify_jwt_or_local()`.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-135-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — pytest/vitest output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
