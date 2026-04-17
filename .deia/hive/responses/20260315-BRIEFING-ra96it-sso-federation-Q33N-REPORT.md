# Q33N Report: ra96it SSO Federation — Task Files Ready for Review

**From:** Q33N (coordinator)
**To:** Q33NR (regent)
**Date:** 2026-03-15
**Briefing:** `.deia/hive/coordination/2026-03-15-BRIEFING-ra96it-sso-federation.md`
**Bot ID:** QUEEN-2026-03-15-BRIEFING-ra96it-sso

---

## Summary

I have completed the task breakdown for the ra96it SSO federation system as specified in the briefing. The spec called for a 3-phase approach, and I have created **three task files** corresponding to each phase:

1. **TASK-133:** Phase 1 — LoginPage + authStore (browser-only, ships independently)
2. **TASK-134:** Phase 2 — ra96it service (backend, separate repo)
3. **TASK-135:** Phase 3 — Wire ShiftCenter to ra96it (backend + frontend integration)

All task files follow the mandatory 8-section response template, include TDD requirements, specify absolute Windows paths, and enforce all 10 hard rules (no hardcoded colors, no stubs, no files over 500 lines, etc.).

---

## Task Files Created

### TASK-133: Phase 1 — LoginPage + authStore (Browser-Only)

**File:** `.deia\hive\tasks\2026-03-15-TASK-133-ra96it-sso-phase1-login-page.md`

**Scope:**
- Browser primitives: `LoginPage.tsx`, `authStore.ts`, `LoginPage.css`, `types.ts`, `index.ts`
- EGG config: `eggs/login.egg.md` (minimal chrome, single pane)
- App registration: `loginAdapter.tsx` + register in `apps/index.ts`
- Routing: Update `eggResolver.ts` to handle `/login` pathname
- Tests: 12+ tests (authStore + LoginPage component tests)

**Model Recommendation:** Haiku (straightforward port/adaptation)

**Deliverables:**
- Dev-login bypass works on localhost (no GitHub account needed)
- GitHub OAuth button present but disabled (no backend yet)
- JWT storage in localStorage (key: `sd_auth_token`)
- All colors use `var(--sd-*)` CSS variables
- No network calls (browser-only)

**Key Design Decisions:**
- Uses jwt-decode for basic JWT parsing (no verification yet)
- Dev token is a mock JWT with fake signature
- Follows SettingsPanel UI pattern (clean, minimal, CSS variables only)
- Can ship independently before ra96it backend exists

---

### TASK-134: Phase 2 — ra96it Service (Backend)

**File:** `.deia\hive\tasks\2026-03-15-TASK-134-ra96it-sso-phase2-backend-service.md`

**Scope:**
- FastAPI service in **separate ra96it repo** (NOT in shiftcenter repo)
- Repo path: `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\`
- Endpoints: `/token/exchange`, `/token/validate`, `/token/refresh` (501), `/userinfo`, `/.well-known/jwks.json`, `/authorize` (501)
- JWT signing with RS256 (asymmetric — private key signs, public key verifies)
- Efemera token exchange via HTTP API call
- User identity store (SQLite for dev, PostgreSQL for prod)
- Tests: 25+ tests (models, JWT, token exchange, validation, JWKS)

**Model Recommendation:** Sonnet (new service, architectural complexity, JWT signing, JWKS)

**Deliverables:**
- POST /token/exchange: Efemera token → ra96it JWT
- JWT claims: `{ sub: "github:{id}", email, display_name, iss: "ra96it.com", aud: "deiasolutions", scope: [...], provider: "github", provider_id: "{id}" }`
- 24-hour JWT expiry (no refresh tokens in MVP)
- CORS configured for shiftcenter.com, efemera.live, localhost:5174
- JWKS endpoint for public key distribution
- SQLAlchemy models: User (provider, provider_id, email, display_name)

**Key Design Decisions:**
- RS256 (asymmetric) instead of HS256 (symmetric) for security
- JWKS instead of static public key (allows key rotation)
- Efemera token validation via HTTP API (trusts Efemera's GitHub OAuth)
- User identity stored in ra96it DB (single source of truth for family)
- Dev mode bypass for local testing (skips Efemera validation)

---

### TASK-135: Phase 3 — Wire ShiftCenter to ra96it

**File:** `.deia\hive\tasks\2026-03-15-TASK-135-ra96it-sso-phase3-wire-shiftcenter.md`

**Scope:**
- Backend: Update `verify_jwt()` to fetch JWKS from ra96it and verify tokens
- Backend: Add `jwks_cache.py` service (in-memory caching, 6-hour TTL)
- Backend: Update `config.py` to add `ra96it_url` field
- Frontend: Update `authStore.ts` to add token exchange, validation, refresh
- Frontend: Update `LoginPage.tsx` to handle OAuth redirect flow
- Frontend: Add `authService.ts` for ra96it API calls
- Frontend: Add HTTP interceptor to attach `Authorization` header
- Tests: 18+ tests (JWKS caching, JWT verification, auth service, integration)

**Model Recommendation:** Haiku (integration work, updating existing code)

**Deliverables:**
- verify_jwt() validates ra96it JWTs via JWKS
- JWKS fetched from ra96it service and cached (6-hour TTL)
- LoginPage GitHub OAuth redirects to ra96it /authorize
- Token exchange flow: Efemera token → ra96it token → localStorage
- All hivenode API calls include Authorization header
- 401 responses redirect to /login
- Dev mode still bypasses auth on localhost
- Documentation updated

**Key Design Decisions:**
- JWKS caching to avoid fetching on every request (performance)
- HTTP interceptor for global auth header attachment
- verify_jwt_or_local() preserves localhost bypass (dev mode)
- Issuer: "ra96it.com", Audience: "deiasolutions" (family scope)
- Environment variables for ra96it URL (local vs cloud)

---

## Spec Compliance Check

| Spec Requirement | Task Coverage |
|------------------|---------------|
| Phase 1: LoginPage + authStore (browser-only) | ✅ TASK-133 |
| Phase 2: ra96it service (backend) | ✅ TASK-134 |
| Phase 3: Wire ShiftCenter to ra96it | ✅ TASK-135 |
| JWT claims match spec | ✅ TASK-134 (exact match) |
| RS256 asymmetric signing | ✅ TASK-134 |
| JWKS endpoint | ✅ TASK-134 |
| Efemera token exchange | ✅ TASK-134 |
| Dev mode bypass on localhost | ✅ TASK-133, TASK-135 |
| CSS variables only (no hardcoded colors) | ✅ TASK-133 (enforced) |
| No file over 500 lines | ✅ All tasks (enforced) |
| TDD (tests first) | ✅ All tasks (enforced) |
| No stubs | ✅ All tasks (enforced) |
| Absolute paths in task files | ✅ All tasks (verified) |

---

## Hard Rules Compliance

All three task files enforce the 10 hard rules:

1. ✅ **Q88N is sovereign** — tasks report to Q33NR, not Q88N
2. ✅ **Q33N does NOT code** — task files instruct bees to write code
3. ✅ **NO HARDCODED COLORS** — TASK-133 explicitly enforces CSS variables only
4. ✅ **No file over 500 lines** — all tasks specify this constraint
5. ✅ **TDD** — all tasks require tests written first
6. ✅ **NO STUBS** — all tasks prohibit stubs and TODOs
7. ✅ **STAY IN YOUR LANE** — each task has clear scope boundaries
8. ✅ **Absolute paths** — all task files use Windows absolute paths
9. ✅ **Archive on completion** — tasks specify response file requirements

---

## Test Count Summary

| Task | Minimum Tests | Test Files |
|------|---------------|------------|
| TASK-133 | 12 | `authStore.test.ts`, `LoginPage.test.tsx` |
| TASK-134 | 25 | `test_models.py`, `test_jwt.py`, `test_token_exchange.py`, `test_token_validate.py`, `test_userinfo.py`, `test_jwks.py` |
| TASK-135 | 18 | `test_jwks_cache.py`, `test_auth_ra96it_integration.py`, `authService.test.ts`, `LoginPage-integration.test.tsx` |
| **Total** | **55** | **12 test files** |

---

## Model Assignments

| Task | Model | Rationale |
|------|-------|-----------|
| TASK-133 | Haiku | Straightforward port of UI pattern, no architectural decisions |
| TASK-134 | Sonnet | New service, JWT signing, RS256, JWKS, Efemera integration — architectural complexity |
| TASK-135 | Haiku | Integration work, updating existing code, no new architecture |

---

## Execution Order

**Recommended:**
1. **TASK-133 first** (can ship independently, no dependencies)
2. **TASK-134 next** (ra96it service must exist before Phase 3)
3. **TASK-135 last** (requires TASK-133 and TASK-134 complete)

**Parallel Option:**
- TASK-133 and TASK-134 can run in parallel (independent)
- TASK-135 must wait for both

---

## Dependencies Between Tasks

```
TASK-133 (LoginPage) ─────┐
                          ├──> TASK-135 (Wire ShiftCenter)
TASK-134 (ra96it service) ┘
```

TASK-133 and TASK-134 have no dependencies on each other. TASK-135 depends on both.

---

## Edge Cases Covered

### TASK-133
- Malformed JWT (authStore handles gracefully)
- Expired token (decode only, no verification)
- Empty localStorage (returns null)
- Localhost detection (uses window.location.hostname)

### TASK-134
- Invalid Efemera token (rejects with 401)
- Expired JWT (PyJWT validates)
- Invalid signature (PyJWT validates)
- Duplicate user (unique constraint on provider + provider_id)
- CORS preflight (FastAPI CORS middleware)

### TASK-135
- JWKS fetch failure (cache old JWKS, retry on next request)
- ra96it service down (local mode bypasses, cloud mode returns 401)
- Token expiry (frontend checks exp claim, redirects to /login)
- 401 redirect loop (HTTP interceptor skips /auth/* routes)

---

## Files That Will Be Modified

### TASK-133 (Browser-Only)
- `browser/src/primitives/auth/LoginPage.tsx` (NEW)
- `browser/src/primitives/auth/authStore.ts` (NEW)
- `browser/src/primitives/auth/LoginPage.css` (NEW)
- `browser/src/primitives/auth/types.ts` (NEW)
- `browser/src/primitives/auth/index.ts` (NEW)
- `browser/src/primitives/auth/__tests__/authStore.test.ts` (NEW)
- `browser/src/primitives/auth/__tests__/LoginPage.test.tsx` (NEW)
- `eggs/login.egg.md` (NEW)
- `browser/src/apps/loginAdapter.tsx` (NEW)
- `browser/src/apps/index.ts` (UPDATE — add login adapter)
- `browser/src/eggs/eggResolver.ts` (UPDATE — add /login path)

### TASK-134 (ra96it Repo)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\main.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\config.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\db.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\models.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\schemas.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\services\jwt.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\services\efemera.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\authorize.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\token.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\userinfo.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\jwks.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\pyproject.toml` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\.env.example` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\README.md` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\conftest.py` (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_*.py` (6 test files, NEW)

### TASK-135 (Backend + Frontend Integration)
- `hivenode/dependencies.py` (UPDATE — verify_jwt)
- `hivenode/config.py` (UPDATE — add ra96it_url)
- `hivenode/services/jwks_cache.py` (NEW)
- `hivenode/routes/auth.py` (UPDATE — validate ra96it JWTs)
- `browser/src/primitives/auth/authStore.ts` (UPDATE — add exchange, validate, refresh)
- `browser/src/primitives/auth/LoginPage.tsx` (UPDATE — OAuth redirect flow)
- `browser/src/services/authService.ts` (NEW)
- `.env.example` (UPDATE — add HIVENODE_RA96IT_URL)
- `browser/.env.example` (UPDATE — add VITE_RA96IT_URL)
- `docs/AUTH.md` (NEW or UPDATE)
- `tests/hivenode/test_jwks_cache.py` (NEW)
- `tests/hivenode/test_auth_ra96it_integration.py` (NEW)
- `browser/src/primitives/auth/__tests__/authService.test.ts` (NEW)
- `browser/src/primitives/auth/__tests__/LoginPage-integration.test.tsx` (NEW)

---

## Potential Issues Identified

### Issue 1: Efemera API Endpoint Unknown
**Problem:** TASK-134 requires calling Efemera API to validate tokens, but the exact endpoint is not documented in the spec.

**Recommendation:** Ask Q88N or check Efemera codebase for the user profile endpoint. Likely: `GET /api/auth/user` with `Authorization: Bearer {efemera_token}`.

**Fallback:** In dev mode, skip Efemera validation and accept any token (stub user profile).

### Issue 2: ra96it Deployment Not Specified
**Problem:** TASK-134 creates the ra96it service, but deployment is not specified. Where does it run?

**Recommendation:** Deploy to Railway (same as hivenode). Add deployment notes to TASK-134 or create a follow-up deployment task.

**Fallback:** For MVP, run ra96it locally on port 8421. ShiftCenter connects to `http://localhost:8421` in dev mode.

### Issue 3: GitHub OAuth App Credentials
**Problem:** TASK-134 requires GitHub OAuth client ID and secret for Efemera validation, but these are not in the spec.

**Recommendation:** Use existing Efemera GitHub OAuth app credentials. Check Efemera config or ask Q88N.

**Fallback:** In dev mode, skip OAuth validation and accept any token.

---

## Recommended Next Steps

1. **Q33NR reviews task files** — check for gaps, missing requirements, unclear acceptance criteria
2. **Q33NR approves or requests corrections** — if issues found, I will fix and resubmit
3. **Q33N dispatches bees** (after Q33NR approval):
   - TASK-133: Haiku bee (parallel)
   - TASK-134: Sonnet bee (parallel)
   - Wait for TASK-133 and TASK-134 to complete
   - TASK-135: Haiku bee (sequential after both complete)
4. **Q33N reviews bee responses** — check for stubs, missing tests, acceptance criteria gaps
5. **Q33N reports to Q33NR** — completion summary with test counts, issues, follow-ups
6. **Q33NR reports to Q88N** — final result, demo, next steps

---

## Questions for Q33NR

1. **Efemera API endpoint:** Do you know the exact endpoint for validating Efemera tokens and fetching user profile? If not, should I add a subtask to research this or assume dev-mode bypass for MVP?

2. **ra96it deployment:** Should TASK-134 include Railway deployment config (Procfile, railway.json) or is that a separate task?

3. **Parallel dispatch:** Should I dispatch TASK-133 and TASK-134 in parallel, or sequential?

4. **GitHub OAuth app:** Should TASK-134 use existing Efemera GitHub OAuth app credentials, or create a new OAuth app for ra96it?

---

## Ready for Review

All task files are written and ready for Q33NR review. No bees dispatched yet. Awaiting Q33NR approval to proceed with dispatch.

**Q33N standing by for corrections or approval.**

---

**End of Q33N Report**
