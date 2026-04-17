# BRIEFING: ra96it SSO Federation — Port from Platform

**From:** Q33NR (regent)
**To:** Q33N (coordinator)
**Date:** 2026-03-15
**Priority:** P0
**Model Assignment:** Sonnet (architectural complexity)
**Supersedes:** TASK-133, TASK-134, TASK-135 (scrap those — fresh task files from this briefing)

---

## Objective

Port the existing Efemera auth system from the platform repo into ShiftCenter, with ra96it as the identity provider for cross-app SSO. Users sign in through efemera.live, which communicates to ra96it.com, which issues JWTs accepted by ShiftCenter and other deiasolutions apps.

**DIRECTIVE: Port existing code. Do NOT rewrite from scratch.** The platform repo has a working GitHub OAuth flow, frontend AuthPage, and 13+ OAuth tests. The ra96it service already has RS256 JWT, MFA, refresh tokens, and bcrypt. Combine them.

---

## What Already Exists

### Platform Repo — Full Auth System (SOURCE for port)

All paths under `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\`:

| File | Lines | What It Does |
|------|-------|-------------|
| `src/efemera/auth/routes.py` | 644 | GitHub OAuth (login, callback, exchange), email/password register + verify, dev-login bypass, bot-login, terminal tokens, API tokens |
| `src/efemera/auth/models.py` | 81 | User model: UUID pk, email, password_hash, github_id, provider (email/github/bot/local), email_verified, role |
| `src/efemera/auth/jwt_utils.py` | 47 | HS256 JWT: chat (24h), terminal (7d) scopes. Claims: sub, email, scope, display_name, role, github_id, is_admin |
| `src/efemera/auth/password_utils.py` | 15 | SHA-256 password hashing |
| `src/efemera/auth/roles.py` | 51 | UserRole enum (member/admin/owner), ChannelPermission enum, ROLE_PERMISSIONS dict |
| `src/efemera/auth/email_sender.py` | 61 | Resend API for 6-digit verification emails |
| `src/efemera/dependencies.py` | 143 | get_current_user() — JWT verification, local user fallback, scope validation |
| `frontend/src/pages/AuthPage.tsx` | 138 | GitHub OAuth button + dev-login button + consent section |
| `frontend/src/lib/auth.ts` | 57 | Token store: getToken/setToken/clearToken, getUser/setUser, getAuthHeaders, isAuthenticated (checks exp + scope) |
| `tests/test_github_oauth.py` | 404 | 13 OAuth tests: login URL, callback, exchange, admin elevation, state validation |
| `tests/test_auth_scopes.py` | 291 | Scope validation tests: chat, terminal, api, bot tokens |

**Key platform auth flows to port:**
1. **GitHub OAuth**: GET `/api/auth/github/login` (returns GitHub auth URL with state), GET `/api/auth/github/callback` (exchanges code for JWT, redirects with token), POST `/api/auth/github/exchange` (SPA code exchange)
2. **Dev-login bypass**: GET `/api/auth/dev-login/available`, POST `/api/auth/dev-login` (available when `is_local_mode and not GITHUB_CLIENT_ID`)
3. **Email/password + 6-digit verification**: POST `/api/auth/register`, POST `/api/auth/verify`, POST `/api/auth/resend-code`, POST `/api/auth/login`
4. **Admin assignment**: `ADMIN_GITHUB_LOGINS` env var (comma-separated GitHub handles)
5. **Allowed origins**: simdecisions.com, shiftcenter.com, efemera.live, localhost variants
6. **State encoding**: base64(JSON(origin, nonce))

### ra96it Service — Already Built (TARGET to extend)

All paths under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\`:

| File | Lines | What It Has |
|------|-------|------------|
| `main.py` | 48 | FastAPI app with lifespan |
| `config.py` | 61 | Settings: RS256 keys (PEM), JWT params (15min access, 30d refresh), Twilio config |
| `models.py` | 123 | User (UUID, email, password_hash/bcrypt, tier, mfa_method), RefreshToken (single-use rotation), LoginSession (MFA state) |
| `schemas.py` | 93 | Pydantic models for register, login, mfa, token refresh/revoke |
| `routes/register.py` | 82 | POST /register |
| `routes/login.py` | 100 | POST /login (triggers MFA) |
| `routes/mfa.py` | 108 | POST /mfa/verify (issues tokens) |
| `routes/token.py` | 123 | POST /token/refresh (single-use rotation), POST /token/revoke |
| `services/jwt.py` | 80 | RS256 create/decode: claims sub, email, tier, iss=ra96it, aud=shiftcenter |
| `services/token.py` | 218 | Refresh token rotation, replay attack detection (revokes ALL on replay) |
| `services/password.py` | 34 | bcrypt via passlib |
| `services/mfa.py` | 88 | Twilio Verify (SMS/email) |
| `services/audit.py` | 131 | Event ledger emission (9 event types) |
| `tests/` | 10 files | JWT, password, models, login, mfa, register, token refresh/revoke, audit |

**What ra96it ALREADY has:** RS256 JWT, refresh token rotation with replay detection, bcrypt, MFA, audit logging, comprehensive tests.

**What ra96it is MISSING:** GitHub OAuth, JWKS endpoint, Efemera token exchange, dev-login bypass.

### Hivenode — JWT Verification (TARGET to wire)

| File | What It Has |
|------|------------|
| `hivenode/dependencies.py:161-263` | `verify_jwt()` (RS256, iss=ra96it, aud=shiftcenter), `verify_jwt_or_local()` (local bypass) |
| `hivenode/routes/auth.py` | GET /auth/verify, /auth/whoami, /auth/identity |
| `hivenode/config.py` | `ra96it_public_key`, `ra96it_public_key_path`, `mode` (local/remote/cloud) |

**What hivenode is MISSING:** JWKS caching (currently uses static public key), family-wide audience validation.

### Browser — Minimal Auth (TARGET to build out)

| File | What It Has |
|------|------------|
| `browser/src/apps/sim/lib/auth.ts` | Token store (efemera_token in localStorage), scope validation |
| `browser/src/services/identity/` | identityService, useIdentity hook, fallback chain |

**What browser is MISSING:** Login page, shared authStore (not sim-specific), login EGG.

---

## Decisions

- **Keep RS256** — more secure than HS256, already in ra96it, supports JWKS for cross-app verification
- **Port GitHub OAuth from platform into ra96it** — extend ra96it's existing routes, don't duplicate
- **Port AuthPage.tsx from platform into browser** — new `browser/src/primitives/auth/` primitive
- **Port auth.ts into shared authStore** — not buried in sim app
- **Keep dev-login bypass** from platform pattern
- **Add JWKS endpoint** to ra96it (new, enables offline JWT verification by any app)
- **Add Efemera token exchange** to ra96it (new, bridges efemera tokens to family JWTs)
- **Upgrade audience claim** from `"shiftcenter"` to `"deiasolutions"` (family-wide)

---

## Phase Structure

### Phase 1: Port GitHub OAuth into ra96it + JWKS (Backend)

**Port from:** `platform/efemera/src/efemera/auth/routes.py` (GitHub OAuth sections)
**Port into:** `ra96it/routes/` (new files alongside existing routes)

**Deliverables:**
- [ ] `ra96it/routes/oauth.py` — Port GitHub OAuth endpoints: GET /oauth/github/login, GET /oauth/github/callback, POST /oauth/github/exchange
- [ ] `ra96it/routes/jwks.py` — GET /.well-known/jwks.json (serves RS256 public key in JWK format)
- [ ] `ra96it/routes/dev_login.py` — Port dev-login bypass: GET /dev-login/available, POST /dev-login
- [ ] `ra96it/services/github.py` — GitHub API client (exchange code for access token, fetch user profile)
- [ ] Update `ra96it/models.py` — Add github_id, provider, display_name fields to User model
- [ ] Update `ra96it/schemas.py` — Add OAuth request/response schemas
- [ ] Update `ra96it/config.py` — Add GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_REDIRECT_URI, FRONTEND_URL, ADMIN_GITHUB_LOGINS
- [ ] Update `ra96it/services/jwt.py` — Add provider, provider_id, display_name, scope claims; update aud to "deiasolutions"
- [ ] Update `ra96it/main.py` — Register new routes
- [ ] Tests: Port from `platform/efemera/tests/test_github_oauth.py` (13 tests) + new JWKS tests + dev-login tests

**Key porting decisions:**
- Platform uses HS256 → upgrade to RS256 (ra96it already uses RS256)
- Platform state encoding (base64 JSON with origin+nonce) → keep same pattern
- Platform allowed origins list → update to deiasolutions family domains
- Platform admin elevation via ADMIN_GITHUB_LOGINS → keep pattern
- Keep MFA as optional for OAuth users (GitHub already verified email)

### Phase 2: Port AuthPage + authStore into Browser (Frontend)

**Port from:** `platform/efemera/frontend/src/pages/AuthPage.tsx` + `frontend/src/lib/auth.ts`
**Port into:** `browser/src/primitives/auth/`

**Deliverables:**
- [ ] `browser/src/primitives/auth/LoginPage.tsx` — Port AuthPage.tsx: GitHub OAuth button, dev-login button (if available), consent section. Use `var(--sd-*)` CSS variables only. No hex colors.
- [ ] `browser/src/primitives/auth/LoginPage.css` — Styles using `var(--sd-*)` only
- [ ] `browser/src/primitives/auth/authStore.ts` — Shared token store: getToken/setToken/clearToken, getUser/setUser, getAuthHeaders, isAuthenticated (exp + scope check). Port from `sim/lib/auth.ts` but make it shared (not sim-specific). Storage key: `ra96it_token` (not `efemera_token`).
- [ ] `browser/src/primitives/auth/index.ts` — Barrel export
- [ ] `eggs/login.egg.md` — Minimal login EGG (single pane, no chrome, LoginPage component)
- [ ] Update `browser/src/eggs/eggResolver.ts` — Add `/login` path resolution to login EGG
- [ ] Update `browser/src/apps/index.ts` — Register login adapter
- [ ] Tests: Vitest component tests for LoginPage (renders, buttons, dev-login check), unit tests for authStore (token CRUD, expiry check, scope validation)

**Key porting decisions:**
- Platform uses `efemera_token` localStorage key → use `ra96it_token`
- Platform AuthPage checks `/api/auth/dev-login/available` → check ra96it `/dev-login/available`
- Platform AuthPage has GitHub button → keep, point to ra96it `/oauth/github/login`
- All colors must use `var(--sd-*)` CSS variables (Rule 3)
- No file over 500 lines (Rule 4)

### Phase 3: Wire ShiftCenter to ra96it JWTs via JWKS (Integration)

**Modify:** `hivenode/dependencies.py`, `hivenode/config.py`

**Deliverables:**
- [ ] `hivenode/services/jwks_cache.py` — JWKS cache: fetch ra96it's /.well-known/jwks.json, cache public key, auto-refresh on expiry or signature failure
- [ ] Update `hivenode/dependencies.py` — `verify_jwt()` uses JWKS cache instead of static public key; accept aud="deiasolutions" (family-wide)
- [ ] Update `hivenode/config.py` — Add `ra96it_jwks_url` setting (default: `https://ra96it.com/.well-known/jwks.json`), keep `ra96it_public_key` as fallback
- [ ] Update `hivenode/routes/auth.py` — /auth/identity returns provider info from JWT claims
- [ ] Tests: Pytest for JWKS cache (fetch, cache, refresh, fallback to static key), updated verify_jwt tests with new audience

**Key porting decisions:**
- Keep `verify_jwt_or_local()` bypass on localhost (Rule: dev mode works without ra96it)
- JWKS cache should have TTL (e.g., 1 hour) and force-refresh on signature verification failure
- Static public key (`ra96it_public_key`) remains as fallback when JWKS endpoint unreachable
- Accept both `aud="shiftcenter"` (legacy) and `aud="deiasolutions"` (new) during transition

---

## Environment Variables (New)

### ra96it service (Phase 1)
```
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GITHUB_REDIRECT_URI=https://ra96it.com/oauth/github/callback
FRONTEND_URL=https://efemera.live
ADMIN_GITHUB_LOGINS=davee,other-admin
```

### hivenode (Phase 3)
```
RA96IT_JWKS_URL=https://ra96it.com/.well-known/jwks.json
```

---

## Hard Rules to Enforce

- **Rule 3:** NO HARDCODED COLORS. Only `var(--sd-*)` CSS variables.
- **Rule 4:** No file over 500 lines. Modularize at 500. Hard limit: 1,000.
- **Rule 5:** TDD. Tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 8:** All file paths must be absolute in task files.
- **DIRECTIVE:** Port existing code from platform. Do NOT rewrite what already works.

---

## Acceptance Criteria

- [ ] ra96it serves GET /.well-known/jwks.json with valid JWK
- [ ] ra96it GitHub OAuth flow: login → callback → JWT issued (RS256)
- [ ] ra96it dev-login bypass works on localhost
- [ ] `localhost:5174/login` renders GitHub OAuth login page styled with `var(--sd-*)` variables
- [ ] Dev-login bypass works on localhost (no GitHub account needed for dev)
- [ ] JWT stored in localStorage as `ra96it_token`, survives page refresh
- [ ] hivenode `verify_jwt()` accepts ra96it-issued JWTs via JWKS cache
- [ ] hivenode `verify_jwt_or_local()` still bypasses auth on localhost
- [ ] All 13+ OAuth tests ported and passing
- [ ] No hardcoded secrets in source
- [ ] No file over 500 lines

---

## Your Job, Q33N

1. **Read the platform auth code** — all files listed above. Understand the OAuth flow, state encoding, admin elevation, and dev-login patterns.
2. **Read the ra96it service** — understand what already exists so you don't duplicate.
3. **Write task files** for 3 phases. One TASK file per phase. Include absolute Windows paths, test counts, acceptance criteria.
4. **Return to Q33NR for review.** Do NOT dispatch bees yet.
5. **Phase 1 model:** Sonnet (OAuth + JWKS complexity). **Phase 2 model:** Haiku (port UI). **Phase 3 model:** Haiku (wire existing code).

---

## End of Briefing

Q33N: Read the codebase, write task files, return for review. Do NOT dispatch until Q33NR approves.
