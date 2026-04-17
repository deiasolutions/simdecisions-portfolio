# BRIEFING: Auth Rebrand — ra96it → hodeia.me

**Date:** 2026-03-24
**From:** Q33NR
**To:** Q33N
**Priority:** P1

## Objective

Rebrand the authentication system from ra96it to hodeia.me across the shiftcenter codebase. This is a branding/routing migration — NOT a rewrite. The ra96it backend service stays on the platform repo at api.ra96it.com. hodeia.me becomes the public-facing auth gateway.

## Context

- ra96it is a standalone FastAPI auth service in `ra96it/` (register, login, MFA, GitHub OAuth, JWKS, dev-login)
- It is deployed on Railway at `api.ra96it.com` from the platform repo
- hodeia.me is the new auth domain — DNS infrastructure is ready on Cloudflare but nameservers haven't been updated at registrars yet
- The codebase still references ra96it everywhere: env vars, localStorage keys, UI text, JWT issuer, JWKS URLs
- The frontend OAuth flow in App.tsx is already domain-agnostic (works for any EGG)

## What Needs to Happen

### Wave 1 — Frontend Branding (3 bee tasks, independent)

**TASK A: LoginPage rebrand**
- File: `browser/src/primitives/auth/LoginPage.tsx`
- Replace `VITE_RA96IT_API` with `VITE_AUTH_API` (generic, not tied to either brand)
- Replace all "ra96it" UI text with "hodeia" or neutral "Sign in" language
- Keep the same GitHub OAuth flow, just update the env var name
- Test file: `browser/src/primitives/auth/__tests__/` — update existing tests + add tests for the new env var name

**TASK B: authStore rebrand**
- File: `browser/src/primitives/auth/authStore.ts`
- Rename localStorage keys from `ra96it_token`/`ra96it_user` to `sd_auth_token`/`sd_auth_user` (use `sd_` prefix to match existing `sd_user_settings` convention)
- Add migration: on load, if old keys exist and new keys don't, copy values over and delete old keys
- Update all imports/references across the codebase
- Test the migration path (old keys → new keys, new keys already exist, no keys)

**TASK C: login.egg.md update**
- File: `eggs/login.egg.md`
- Update description text from "ra96it service" to "hodeia authentication"
- Update any localStorage key references in the EGG config to match new `sd_auth_*` keys
- No layout changes needed

### Wave 2 — Backend Config (2 bee tasks, independent)

**TASK D: hivenode auth config rebrand**
- File: `hivenode/config.py` — rename `ra96it_public_key`, `ra96it_public_key_path`, `ra96it_jwks_url` to `auth_public_key`, `auth_public_key_path`, `auth_jwks_url`
- File: `hivenode/dependencies.py` — update JWT issuer validation to accept BOTH `"ra96it"` and `"hodeia"` (dual-issuer for backwards compat during transition)
- File: `hivenode/services/jwks_cache.py` — update to use new config field names
- Update all references in hivenode/ that use the old config field names
- Tests: update existing JWT/auth tests, add test for dual-issuer acceptance

**TASK E: deployment docs update**
- File: `.deia/config/deployment-env.md` — update all env var names and URLs
- Document the migration: old env var → new env var mapping
- Document dual-issuer strategy (accept both ra96it and hodeia JWTs during transition)
- No code changes, docs only

### Wave 3 — eggResolver cleanup (1 bee task, depends on Wave 1)

**TASK F: eggResolver routing cleanup**
- File: `browser/src/eggs/eggResolver.ts`
- Keep both `hodeia.me` and `ra96it.com` → `login` mappings (backwards compat)
- Add comment marking ra96it.com entries as deprecated
- Update test file to verify both old and new hostnames resolve to login

## Constraints

- CSS: `var(--sd-*)` only (relevant for LoginPage if any style changes)
- No file over 500 lines
- TDD — tests first
- No stubs
- The ra96it/ directory itself is NOT modified — that's the platform repo's service
- localStorage key migration MUST be backwards-compatible (don't break existing sessions)
- JWT issuer MUST accept both "ra96it" and "hodeia" during transition

## Models

- Wave 1 tasks (A, B, C): **haiku** — straightforward find-and-replace with tests
- Wave 2 tasks (D, E): **haiku** for D, **haiku** for E (docs only)
- Wave 3 task (F): **haiku** — small scope

## Files to Read First

- `browser/src/primitives/auth/LoginPage.tsx`
- `browser/src/primitives/auth/authStore.ts`
- `browser/src/primitives/auth/__tests__/` (all files)
- `eggs/login.egg.md`
- `hivenode/config.py`
- `hivenode/dependencies.py`
- `hivenode/services/jwks_cache.py`
- `browser/src/eggs/eggResolver.ts`
- `.deia/config/deployment-env.md`

## Success Criteria

- Zero references to `ra96it` in frontend source code (except eggResolver backwards-compat entries marked deprecated)
- Zero references to `ra96it` in hivenode config field names
- JWT validation accepts both `ra96it` and `hodeia` issuers
- localStorage migration works: existing ra96it_token users seamlessly get sd_auth_token
- All existing auth tests pass + new tests for migration/dual-issuer
- Deployment docs updated with new env var names

## What Q33N Should Do

1. Read the files listed above
2. Write 6 task files (TASK-A through TASK-F) to `.deia/hive/tasks/`
3. Return to Q33NR for review before dispatching
4. After approval, dispatch Wave 1 (A, B, C) in parallel, then Wave 2 (D, E) in parallel, then Wave 3 (F)
