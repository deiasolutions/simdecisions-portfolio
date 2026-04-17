# BRIEFING: ra96it SSO Federation — Q33N

**From:** Q88NR (regent)
**To:** Q33N (coordinator)
**Date:** 2026-03-15
**Spec:** `.deia/hive/queue/2026-03-14-2200-SPEC-ra96it-sso-federation.md`
**Priority:** P0.015
**Model Assignment:** Sonnet (architectural complexity)

---

## Objective

Build an SSO federation layer where ra96it.com acts as the token issuer for the deiasolutions website family (shiftcenter, efemera, deiasolutions.org). Efemera's existing GitHub OAuth is the identity provider underneath. Users authenticate once via Efemera's GitHub flow, ra96it validates their identity and issues family-wide JWTs, and all deiasolutions apps accept those JWTs.

---

## Context from Spec

### Architecture Overview

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
1. **Efemera** owns the GitHub OAuth integration (already built)
2. **ra96it** is the federation layer — trusts Efemera tokens and issues its own JWTs scoped to the deiasolutions family
3. **ShiftCenter** (and all other apps) only validate ra96it JWTs — they never talk to GitHub or Efemera directly
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

---

## Existing Code to Read

### ShiftCenter Auth
- **JWT verification:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
  - `verify_jwt_or_local()` — local bypasses auth, cloud requires JWT
  - `verify_jwt()` — always requires JWT (used by node routes)
- **Settings store:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts` (uses `sd_user_settings` in localStorage)

### Efemera Auth (Reference)
- **Auth page:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\platform\efemera\frontend\src\pages\AuthPage.tsx` (137 lines — GitHub OAuth + dev-login bypass)
- **Backend endpoints:**
  - `/api/auth/github/login`
  - `/api/auth/dev-login`
  - `/api/auth/dev-login/available`

### ra96it Repo
- **Location:** `C:\Users\davee\OneDrive\Documents\GitHub\ra96it` (docs only, no code yet)

### Browser Infrastructure
- **EGG resolver:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`
- **Apps index:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`

---

## Deliverables (from Spec)

### Phase 1: Login page in ShiftCenter (browser-only)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — port Efemera AuthPage, adapt to SC theme (CSS variables)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — JWT storage (localStorage), token refresh check, isAuthenticated()
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\index.ts` — barrel export
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\login.egg.md` — minimal chrome login EGG
- [ ] `/login` path resolution in `eggResolver.ts`
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

---

## Acceptance Criteria (from Spec)

- [ ] `localhost:5174/login` renders a GitHub OAuth login page styled with SC theme
- [ ] Dev-login bypass works on localhost (no GitHub account needed for dev)
- [ ] Login flow: click GitHub → OAuth → ra96it issues JWT → redirect back to app → authenticated
- [ ] JWT stored in localStorage, survives page refresh
- [ ] `verify_jwt()` accepts ra96it-issued JWTs
- [ ] `verify_jwt_or_local()` still bypasses auth on localhost
- [ ] All colors use `var(--sd-*)` CSS variables
- [ ] No file over 500 lines
- [ ] No hardcoded secrets in source (use env vars)

---

## Constraints (from Spec)

1. **No new OAuth providers yet.** GitHub only (via Efemera) for now. Google/email can come later.
2. **No HIPAA/2FA.** Simple auth tier only. FamilyBondBot-style tiering is future work.
3. **ra96it is a separate service.** It does NOT live inside shiftcenter or hivenode. It gets its own repo/deployment.
4. **Dev mode must still work without ra96it running.** `verify_jwt_or_local()` bypasses on localhost.
5. **Phase 1 can ship independently.** The login page + auth store work with mock/dev auth before ra96it backend exists.

---

## Hard Rules to Enforce

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`).
- **Rule 4:** No file over 500 lines. Modularize at 500. Hard limit: 1,000.
- **Rule 5:** TDD. Tests first, then implementation. No exceptions except pure CSS and docs.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 8:** All file paths must be absolute in task files.

---

## Recommended Task Breakdown

Given the complexity and the 3-phase structure in the spec, I recommend:

1. **TASK-XXX:** Phase 1 — LoginPage + authStore + EGG + routing (browser-only, can ship independently)
   - **Model:** Haiku (straightforward port of Efemera AuthPage)
   - **Tests:** Vitest component tests for LoginPage, unit tests for authStore

2. **TASK-YYY:** Phase 2 — ra96it service (backend, separate repo)
   - **Model:** Sonnet (new service, JWT signing, RS256, JWKS, identity store)
   - **Tests:** Pytest for all endpoints, JWT signing/verification, token refresh, JWKS

3. **TASK-ZZZ:** Phase 3 — Wire ShiftCenter to ra96it (backend + frontend integration)
   - **Model:** Haiku (update existing JWT verification, add middleware)
   - **Tests:** Pytest for updated verify_jwt functions, integration tests for auth flow

---

## Your Job, Q33N

1. **Read the existing code paths** listed above (AuthPage, verify_jwt*, authStore, eggResolver, apps/index.ts).
2. **Write task files** for the 3 phases (or more if you see a better breakdown).
3. **Return to Q88NR for review.** Do NOT dispatch bees yet.
4. **Include absolute Windows paths** in all task files (`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\...`).
5. **Specify test counts** and edge cases explicitly in each task.
6. **Check for CSS variables** — any UI work must use `var(--sd-*)` only.

---

## Additional Notes

- The spec says "Phase 1 can ship independently" — this means TASK-XXX (LoginPage + authStore) should work with dev-login bypass even before ra96it backend exists.
- The spec says "ra96it is a separate service" — TASK-YYY should target the `C:\Users\davee\OneDrive\Documents\GitHub\ra96it` repo, NOT the shiftcenter repo.
- The spec says "Dev mode must still work without ra96it running" — TASK-ZZZ must preserve `verify_jwt_or_local()` bypass on localhost.

---

## End of Briefing

Q33N, you now have everything you need to write task files. Read the codebase, write the tasks, return to Q88NR for review. Do NOT dispatch bees until Q88NR approves.
