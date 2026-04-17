# TASK-138: Wire Hivenode to ra96it JWTs via JWKS Cache

## Objective
Add JWKS caching to hivenode for dynamic public key retrieval, upgrade JWT verification to accept family-wide audience, keep local mode bypass working.

## Context
Hivenode currently uses a static public key (`ra96it_public_key`) to verify JWTs. This task adds a JWKS cache that fetches ra96it's `/.well-known/jwks.json` endpoint, caches the public key, auto-refreshes on expiry or signature failure, and falls back to static key when JWKS unreachable.

The JWT audience claim is being upgraded from `"shiftcenter"` (app-specific) to `"deiasolutions"` (family-wide), so verification must accept both during the transition.

**Key patterns to preserve:**
- `verify_jwt_or_local()` still bypasses auth on localhost (Rule: dev mode works without ra96it)
- `verify_jwt()` always requires JWT (used by node routes)
- Static public key remains as fallback when JWKS endpoint unreachable

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (lines 161-263: verify_jwt, verify_jwt_or_local)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings: ra96it_public_key, ra96it_public_key_path)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` (auth routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\lib\auth.ts` (reference for token structure)

## Deliverables

### Backend Code
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\services\jwks_cache.py`:
  - Class `JWKSCache`:
    - `__init__(jwks_url: str, static_fallback_key: str | None, ttl_seconds: int = 3600)`
    - `async get_public_key() -> str` — returns cached key or fetches from JWKS endpoint
    - `async _fetch_jwks() -> dict` — GET `jwks_url`, parse JSON, extract first key from `keys` array
    - `_jwk_to_pem(jwk: dict) -> str` — convert JWK (n, e) to PEM format using `cryptography` library
    - `async refresh()` — force-refresh JWKS (called on signature verification failure)
    - Cache state: `_cached_key: str | None`, `_cached_at: datetime | None`
    - TTL logic: if cache age > ttl_seconds, fetch fresh
    - Fallback: if JWKS fetch fails, use `static_fallback_key`
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`:
  - Import `JWKSCache`
  - Instantiate global cache: `_jwks_cache = JWKSCache(settings.ra96it_jwks_url, settings.ra96it_public_key, ttl_seconds=3600)`
  - Update `verify_jwt()`:
    - Use `await _jwks_cache.get_public_key()` instead of static `settings.get_ra96it_public_key()`
    - Accept `aud="deiasolutions"` OR `aud="shiftcenter"` (transition period)
    - On `jwt.InvalidSignatureError`: call `await _jwks_cache.refresh()`, retry once
  - Keep `verify_jwt_or_local()` unchanged (still bypasses auth on localhost)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`:
  - Add `ra96it_jwks_url: str = "https://ra96it.com/.well-known/jwks.json"`
  - Keep `ra96it_public_key` and `ra96it_public_key_path` (fallback when JWKS unreachable)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py`:
  - GET `/auth/identity` — return provider info from JWT claims (`provider`, `provider_id`, `display_name`, `scope`)

### Tests (TDD — write tests FIRST)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\services\__tests__\test_jwks_cache.py`:
  - `test_jwks_cache_fetches_on_first_call` — mock JWKS endpoint, verify fetch on first `get_public_key()`
  - `test_jwks_cache_returns_cached_key_within_ttl` — fetch once, call again within TTL, verify no second fetch
  - `test_jwks_cache_refreshes_after_ttl_expires` — wait > TTL, verify refetch
  - `test_jwks_cache_converts_jwk_to_pem` — provide JWK with n/e, verify PEM output format
  - `test_jwks_cache_fallback_on_fetch_failure` — mock JWKS endpoint error, verify fallback to static key
  - `test_jwks_cache_refresh_forces_fetch` — call `refresh()`, verify immediate fetch regardless of TTL
  - `test_jwks_cache_handles_empty_keys_array` — JWKS response with `{keys: []}` → fallback
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_routes.py` (extend existing):
  - `test_verify_jwt_accepts_deiasolutions_audience` — JWT with `aud="deiasolutions"` → 200
  - `test_verify_jwt_accepts_shiftcenter_audience_legacy` — JWT with `aud="shiftcenter"` → 200
  - `test_verify_jwt_rejects_wrong_audience` — JWT with `aud="other"` → 401
  - `test_verify_jwt_refreshes_on_signature_failure` — mock JWKS cache, return stale key, verify refresh + retry
  - `test_verify_jwt_or_local_bypasses_on_localhost` — mode=local → 200 without JWT
  - `test_verify_jwt_or_local_requires_jwt_on_cloud` — mode=cloud → 401 without JWT
  - `test_auth_identity_returns_provider_info` — JWT with provider/provider_id/display_name → echoed in response

### Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All 14+ tests pass (7 JWKS cache + 7 auth routes)
- [ ] Mock JWKS endpoint using `httpx.AsyncClient` with `httpx.MockTransport`
- [ ] Test TTL expiry (use time mocking or short TTL + sleep)
- [ ] Test fallback to static key on JWKS fetch failure
- [ ] Test both `aud="deiasolutions"` and `aud="shiftcenter"` acceptance
- [ ] Test local mode bypass (no JWT required)
- [ ] Edge cases: empty JWKS keys array, network timeout, malformed JWK

## Constraints
- No file over 500 lines (Rule 4)
- NO STUBS (Rule 6) — every function fully implemented
- TDD (Rule 5) — tests first, then implementation
- All file paths must be absolute (Rule 8)
- Keep `verify_jwt_or_local()` bypass on localhost (dev mode must work without ra96it)
- Static public key remains as fallback (JWKS unreachable should not break local dev)
- Accept both `aud="shiftcenter"` (legacy) and `aud="deiasolutions"` (new) during transition

## Acceptance Criteria
- [ ] hivenode `verify_jwt()` fetches public key from JWKS cache (not static config)
- [ ] JWKS cache fetches from ra96it `/.well-known/jwks.json` on first call
- [ ] JWKS cache returns cached key within TTL (no redundant fetches)
- [ ] JWKS cache auto-refreshes after TTL expires
- [ ] JWKS cache force-refreshes on `jwt.InvalidSignatureError`, retries verification once
- [ ] JWKS cache falls back to static public key when JWKS endpoint unreachable
- [ ] `verify_jwt()` accepts `aud="deiasolutions"` OR `aud="shiftcenter"`
- [ ] `verify_jwt_or_local()` still bypasses auth when `mode=local`
- [ ] `verify_jwt_or_local()` requires JWT when `mode=cloud` or `mode=remote`
- [ ] GET `/auth/identity` returns provider info from JWT claims
- [ ] All 14+ tests pass
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-138-RESPONSE.md`

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
