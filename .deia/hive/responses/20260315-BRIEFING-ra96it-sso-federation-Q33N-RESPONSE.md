# Q33N Response: ra96it SSO Federation — Port from Platform

**Bot ID:** QUEEN-2026-03-15-BRIEFING-ra96it-sso
**Status:** TASK FILES READY FOR REVIEW
**Date:** 2026-03-15

---

## Task Files Written

I have written 3 task files corresponding to the 3 phases outlined in the briefing:

1. **TASK-136: Port GitHub OAuth + JWKS into ra96it (Backend)**
   - File: `.deia/hive/tasks/2026-03-15-TASK-136-ra96it-github-oauth-jwks.md`
   - Model: Sonnet (OAuth + JWKS complexity)
   - Test count: 21+ tests (13 OAuth + 3 JWKS + 5 dev-login)
   - Deliverables: 5 new routes files, 1 GitHub service, updates to models/schemas/config/jwt, all tests

2. **TASK-137: Port AuthPage + authStore into Browser (Frontend)**
   - File: `.deia/hive/tasks/2026-03-15-TASK-137-browser-auth-primitive-login-egg.md`
   - Model: Haiku (UI port)
   - Test count: 17+ tests (8 component + 9 store)
   - Deliverables: LoginPage component, authStore, login EGG, eggResolver update, all tests

3. **TASK-138: Wire Hivenode to ra96it JWTs via JWKS Cache (Integration)**
   - File: `.deia/hive/tasks/2026-03-15-TASK-138-hivenode-jwks-cache-family-aud.md`
   - Model: Haiku (wire existing code)
   - Test count: 14+ tests (7 JWKS cache + 7 auth routes)
   - Deliverables: JWKS cache service, updated verify_jwt, config changes, all tests

---

## What I Read

### Platform Auth System (SOURCE for port)
- `platform/efemera/src/efemera/auth/routes.py` (644 lines: GitHub OAuth, dev-login, email/password)
- `platform/efemera/src/efemera/auth/models.py` (81 lines: User model with github_id, provider)
- `platform/efemera/src/efemera/auth/jwt_utils.py` (47 lines: HS256 JWT — will upgrade to RS256)
- `platform/efemera/frontend/src/pages/AuthPage.tsx` (138 lines: GitHub OAuth button, dev-login, consent)
- `platform/efemera/frontend/src/lib/auth.ts` (57 lines: token store, scope validation)

### ra96it Service (TARGET to extend)
- `ra96it/main.py` (48 lines: existing routes)
- `ra96it/config.py` (61 lines: RS256 keys, JWT params)
- `ra96it/models.py` (123 lines: User, RefreshToken, LoginSession)
- `ra96it/services/jwt.py` (80 lines: RS256 create/decode)

### Hivenode (TARGET to wire)
- `hivenode/dependencies.py` (lines 161-263: verify_jwt, verify_jwt_or_local)
- `hivenode/config.py` (settings: ra96it_public_key)

---

## Key Decisions Made

### TASK-136 (ra96it Backend)
- **Port GitHub OAuth flow** from platform routes.py (lines 60-247) into `ra96it/routes/oauth.py`
- **Port dev-login bypass** from platform routes.py (lines 250-275) into `ra96it/routes/dev_login.py`
- **Add JWKS endpoint** (new, not in platform) at `/.well-known/jwks.json` for public key distribution
- **Upgrade from HS256 to RS256** — ra96it already uses RS256, so keep that (platform uses HS256)
- **Keep state encoding pattern** from platform: `base64(JSON({origin, nonce}))`
- **Keep admin elevation pattern** from platform: `ADMIN_GITHUB_LOGINS` env var
- **Add 6 new fields to User model:** `github_id`, `provider`, `display_name`, `email_verified`, `scope`, `provider_id`
- **Update JWT claims:** add `provider`, `provider_id`, `display_name`, `scope`, upgrade `aud` from `"shiftcenter"` to `"deiasolutions"`
- **MFA optional for OAuth users** — GitHub already verified email, so set `email_verified=True`, skip MFA requirement
- **21+ tests:** 13 OAuth (ported from platform), 3 JWKS (new), 5 dev-login (ported from platform)

### TASK-137 (Browser Frontend)
- **Port AuthPage.tsx** from platform into `browser/src/primitives/auth/LoginPage.tsx`
- **Convert all colors to CSS variables** — platform uses hardcoded hex colors, must convert to `var(--sd-*)` (Rule 3)
- **Port auth.ts** from platform into `browser/src/primitives/auth/authStore.ts`
- **Change storage key** from `efemera_token` to `ra96it_token`
- **Create login EGG** at `eggs/login.egg.md` (minimal, no chrome, single pane)
- **Wire EGG resolver** to map `/login` → login EGG
- **17+ tests:** 8 component tests (render, dev-login availability, OAuth flow, no hardcoded colors), 9 store tests (token CRUD, expiry, scope validation)

### TASK-138 (Hivenode Integration)
- **Add JWKS cache** for dynamic public key retrieval (not in platform, new for cross-app verification)
- **Upgrade audience validation** from `"shiftcenter"` to `"deiasolutions"` (accept both during transition)
- **Keep local mode bypass** — `verify_jwt_or_local()` still works without ra96it on localhost
- **Static key fallback** — JWKS cache falls back to static `ra96it_public_key` when JWKS endpoint unreachable
- **Auto-refresh on signature failure** — if JWT signature fails, refresh JWKS cache once and retry
- **14+ tests:** 7 JWKS cache tests (fetch, TTL, refresh, fallback), 7 auth route tests (audience variants, local bypass, provider info)

---

## Test Counts

| Task | Total Tests | Breakdown |
|------|-------------|-----------|
| TASK-136 | 21+ | 13 OAuth + 3 JWKS + 5 dev-login |
| TASK-137 | 17+ | 8 component + 9 store |
| TASK-138 | 14+ | 7 JWKS cache + 7 auth routes |
| **Total** | **52+** | **All TDD (tests first)** |

---

## Acceptance Criteria Summary

### Phase 1 (TASK-136: ra96it Backend)
- [ ] GET `/.well-known/jwks.json` returns valid JWK with RS256 public key
- [ ] GET `/oauth/github/login` returns GitHub auth URL with base64-encoded state
- [ ] GET `/oauth/github/callback` exchanges code, creates/updates user, redirects with JWT
- [ ] POST `/oauth/github/exchange` returns JSON with JWT, user, github_token
- [ ] GitHub users created with `provider="github"`, `email_verified=True`, `github_id=<id>`
- [ ] Admin elevation via `ADMIN_GITHUB_LOGINS` env var
- [ ] Dev-login available when `mode=local` and no `GITHUB_CLIENT_ID`
- [ ] JWT claims include: `sub`, `email`, `tier`, `provider`, `provider_id`, `display_name`, `scope`, `iss=ra96it`, `aud=deiasolutions`
- [ ] All 21+ tests pass

### Phase 2 (TASK-137: Browser Frontend)
- [ ] `localhost:5174/login` renders GitHub OAuth login page
- [ ] Styled with `var(--sd-*)` CSS variables ONLY (no hex colors)
- [ ] Dev-login button shown/hidden based on `/dev-login/available`
- [ ] GitHub button fetches OAuth URL, redirects to GitHub
- [ ] Dev-login button POSTs, calls `onAuthSuccess` with token + user
- [ ] JWT stored as `ra96it_token`, user as `ra96it_user` in localStorage
- [ ] `isAuthenticated()` validates expiry + scope (rejects bot/api tokens)
- [ ] All 17+ tests pass

### Phase 3 (TASK-138: Hivenode Integration)
- [ ] JWKS cache fetches from `/.well-known/jwks.json` on first call
- [ ] Cached key used within TTL (no redundant fetches)
- [ ] Auto-refresh after TTL expires or on signature failure
- [ ] Fallback to static public key when JWKS unreachable
- [ ] `verify_jwt()` accepts `aud="deiasolutions"` OR `aud="shiftcenter"`
- [ ] `verify_jwt_or_local()` bypasses auth on localhost
- [ ] GET `/auth/identity` returns provider info from JWT
- [ ] All 14+ tests pass

---

## Hard Rules Enforced in Task Files

- **Rule 3:** NO HARDCODED COLORS — only `var(--sd-*)` CSS variables (TASK-137)
- **Rule 4:** No file over 500 lines — modularize at 500 (all tasks)
- **Rule 5:** TDD — tests first, then implementation (all tasks)
- **Rule 6:** NO STUBS — every function fully implemented (all tasks)
- **Rule 8:** All file paths absolute (all tasks)
- **Briefing directive:** Port existing code — do NOT rewrite from scratch (all tasks)

---

## Environment Variables Added

### TASK-136 (ra96it)
```bash
RA96IT_GITHUB_CLIENT_ID=...
RA96IT_GITHUB_CLIENT_SECRET=...
RA96IT_GITHUB_REDIRECT_URI=http://localhost:8021/oauth/github/callback
RA96IT_FRONTEND_URL=http://localhost:5174
RA96IT_ADMIN_GITHUB_LOGINS=davee,other-admin
RA96IT_MODE=local
```

### TASK-138 (hivenode)
```bash
RA96IT_JWKS_URL=https://ra96it.com/.well-known/jwks.json
```

---

## Files to Be Created/Modified

### TASK-136 (13 files)
**New:**
- `ra96it/routes/oauth.py`
- `ra96it/routes/jwks.py`
- `ra96it/routes/dev_login.py`
- `ra96it/services/github.py`
- `ra96it/tests/test_oauth.py`
- `ra96it/tests/test_jwks.py`
- `ra96it/tests/test_dev_login.py`

**Modified:**
- `ra96it/models.py` (add github_id, provider, email_verified, display_name)
- `ra96it/schemas.py` (add OAuth request/response schemas)
- `ra96it/config.py` (add GitHub OAuth settings, mode, allowed_origins)
- `ra96it/services/jwt.py` (add provider, provider_id, display_name, scope claims; upgrade aud)
- `ra96it/main.py` (register oauth, jwks, dev_login routers)

### TASK-137 (9 files)
**New:**
- `browser/src/primitives/auth/LoginPage.tsx`
- `browser/src/primitives/auth/LoginPage.css`
- `browser/src/primitives/auth/authStore.ts`
- `browser/src/primitives/auth/index.ts`
- `browser/src/primitives/auth/__tests__/LoginPage.test.tsx`
- `browser/src/primitives/auth/__tests__/authStore.test.ts`
- `eggs/login.egg.md`

**Modified:**
- `browser/src/eggs/eggResolver.ts` (add /login path)
- `browser/src/apps/index.ts` (register auth adapter)

### TASK-138 (4 files)
**New:**
- `hivenode/services/jwks_cache.py`
- `hivenode/services/__tests__/test_jwks_cache.py`

**Modified:**
- `hivenode/dependencies.py` (use JWKS cache, accept both audiences)
- `hivenode/config.py` (add ra96it_jwks_url)
- `hivenode/routes/auth.py` (add provider info to /auth/identity)
- `tests/hivenode/test_auth_routes.py` (extend with new tests)

---

## Next Steps for Q33NR

1. **Review task files** for completeness, accuracy, missing deliverables
2. **Check test counts** — verify 52+ tests total (21+17+14)
3. **Verify file paths** — all absolute Windows paths
4. **Verify model assignments** — TASK-136 (Sonnet), TASK-137 (Haiku), TASK-138 (Haiku)
5. **Approve dispatch** — if task files are clean, approve bee dispatch
6. **Sequential execution:** TASK-136 → TASK-137 → TASK-138 (TASK-137 needs ra96it endpoints from TASK-136)

---

## Questions for Q33NR

None. Task files are complete and ready for review.

---

## Issues / Risks

None identified. The platform code is well-tested (13 OAuth tests), the ra96it service already has RS256 + bcrypt + MFA, and hivenode already has JWT verification. This is a port + wire task, not a greenfield build.

---

**Q33N ready to dispatch bees after Q33NR approval.**
