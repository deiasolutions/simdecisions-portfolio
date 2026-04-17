# SPEC: ra96it SSO Federation — Efemera Identity + Family JWT

## Priority
P0.015

## Objective
Build an SSO federation layer where ra96it.com acts as the token issuer for the deiasolutions website family (shiftcenter, efemera, deiasolutions.org). Efemera's existing GitHub OAuth is the identity provider underneath. Users authenticate once via Efemera's GitHub flow, ra96it validates their identity and issues family-wide JWTs, and all deiasolutions apps accept those JWTs.

## Architecture

```
User hits code.shiftcenter.com/login
  → ShiftCenter checks: do I have a ra96it JWT?
    → YES: validated, proceed
    → NO: redirect to ra96it.com/authorize?app=shiftcenter&redirect=<url>
      → ra96it checks: is this user authenticated via Efemera?
        → YES: issue JWT for deiasolutions family, redirect back with token
        → NO: redirect to Efemera GitHub OAuth
          → on success: Efemera returns access_token + user profile
          → ra96it stores identity, issues family JWT, redirects back to app
```

### Token Flow
1. **Efemera** owns the GitHub OAuth integration (already built: `platform/efemera/frontend/src/pages/AuthPage.tsx`)
2. **ra96it** is the federation layer — it trusts Efemera tokens and issues its own JWTs scoped to the deiasolutions family
3. **ShiftCenter** (and all other apps) only need to validate ra96it JWTs — they never talk to GitHub or Efemera directly
4. **Family scope:** `shiftcenter.com`, `efemera.live`, `deiasolutions.org`, `ra96it.com`

### JWT Claims (ra96it-issued)
```json
{
  "sub": "github:12345",
  "email": "user@example.com",
  "display_name": "Dave",
  "iss": "ra96it.com",
  "aud": "deiasolutions",
  "iat": 1710000000,
  "exp": 1710086400,
  "scope": ["shiftcenter", "efemera", "deiasolutions"],
  "provider": "github",
  "provider_id": "12345"
}
```

## Context

### Existing auth in shiftcenter
- `hivenode/routes/__init__.py` has `verify_jwt_or_local()` — local bypasses auth, cloud requires JWT
- `verify_jwt()` always requires JWT (used by node routes)
- ra96it repo exists at `C:\Users\davee\OneDrive\Documents\GitHub\ra96it` — docs only, no code yet
- Efemera AuthPage: simple GitHub OAuth + dev-login bypass (137 lines)
- Efemera backend endpoints: `/api/auth/github/login`, `/api/auth/dev-login`, `/api/auth/dev-login/available`

### Key files
- Efemera auth page: `platform/efemera/frontend/src/pages/AuthPage.tsx`
- ShiftCenter JWT verification: `hivenode/routes/__init__.py` (`verify_jwt_or_local`, `verify_jwt`)
- ShiftCenter auth service dir: `ra96it/` (repo root, separate from shiftcenter)
- EGG resolver: `browser/src/eggs/eggResolver.ts`
- ShiftCenter settings store: `browser/src/primitives/settings/settingsStore.ts` (uses `sd_user_settings` in localStorage)

## Deliverables

### Phase 1: Login page in ShiftCenter (browser-only)
- [ ] Create `browser/src/primitives/auth/LoginPage.tsx` — port Efemera AuthPage, adapt to SC theme (CSS variables)
- [ ] Create `browser/src/primitives/auth/authStore.ts` — JWT storage (localStorage), token refresh check, isAuthenticated()
- [ ] Create `browser/src/primitives/auth/index.ts` — barrel export
- [ ] Create `eggs/login.egg.md` — minimal chrome login EGG
- [ ] Add `/login` path resolution in `eggResolver.ts`
- [ ] Register `login` adapter in `apps/index.ts`
- [ ] Add login status indicator to shell (logged in / not logged in)

### Phase 2: ra96it federation service (backend)
- [ ] Build ra96it FastAPI service with endpoints:
  - `GET /authorize` — redirect to Efemera OAuth if not authenticated, issue family JWT if authenticated
  - `POST /token/validate` — validate a ra96it JWT, return claims
  - `POST /token/refresh` — refresh a ra96it JWT
  - `GET /userinfo` — return user profile from JWT claims
  - `GET /.well-known/jwks.json` — public key for JWT verification
- [ ] JWT signing with RS256 (asymmetric — ra96it signs, apps verify with public key)
- [ ] User identity store (SQLite for dev, PostgreSQL for prod)
- [ ] Efemera token exchange endpoint — accepts Efemera access_token, returns ra96it family JWT

### Phase 3: Wire ShiftCenter to ra96it
- [ ] Update `verify_jwt()` and `verify_jwt_or_local()` to validate ra96it JWTs (fetch JWKS from ra96it)
- [ ] Add auth middleware that redirects unauthenticated users to `/login`
- [ ] Protected routes return 401 → frontend redirects to login
- [ ] Token stored in localStorage, attached as `Authorization: Bearer <token>` header
- [ ] Dev mode: `verify_jwt_or_local()` still bypasses auth on localhost

## Acceptance Criteria
- [ ] `localhost:5174/login` renders a GitHub OAuth login page styled with SC theme
- [ ] Dev-login bypass works on localhost (no GitHub account needed for dev)
- [ ] Login flow: click GitHub → OAuth → ra96it issues JWT → redirect back to app → authenticated
- [ ] JWT stored in localStorage, survives page refresh
- [ ] `verify_jwt()` accepts ra96it-issued JWTs
- [ ] `verify_jwt_or_local()` still bypasses auth on localhost
- [ ] All colors use `var(--sd-*)` CSS variables
- [ ] No file over 500 lines
- [ ] No hardcoded secrets in source (use env vars)

## Constraints
1. **No new OAuth providers yet.** GitHub only (via Efemera) for now. Google/email can come later.
2. **No HIPAA/2FA.** Simple auth tier only. FamilyBondBot-style tiering is future work.
3. **ra96it is a separate service.** It does NOT live inside shiftcenter or hivenode. It gets its own repo/deployment.
4. **Dev mode must still work without ra96it running.** `verify_jwt_or_local()` bypasses on localhost.
5. **Phase 1 can ship independently.** The login page + auth store work with mock/dev auth before ra96it backend exists.

## Source
Q88N-direct, 2026-03-14
