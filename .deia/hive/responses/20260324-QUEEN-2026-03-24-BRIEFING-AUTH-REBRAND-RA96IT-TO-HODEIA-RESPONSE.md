# BRIEFING: Auth Rebrand — ra96it → hodeia -- AWAITING REVIEW

**Status:** AWAITING REVIEW (task files written, awaiting Q33NR approval before dispatch)
**Model:** Sonnet
**Date:** 2026-03-24

## Task Files Created

Created 6 task files in `.deia/hive/tasks/`:

1. **TASK-AUTH-A**: `2026-03-24-TASK-AUTH-A-LOGIN-PAGE-REBRAND.md`
   - LoginPage.tsx: VITE_RA96IT_API → VITE_AUTH_API, UI text ra96it → hodeia
   - Model: haiku
   - Dependencies: None

2. **TASK-AUTH-B**: `2026-03-24-TASK-AUTH-B-AUTHSTORE-REBRAND.md`
   - authStore.ts: localStorage keys ra96it_token/ra96it_user → sd_auth_token/sd_auth_user
   - Includes backwards-compatible migration logic
   - Model: haiku
   - Dependencies: None

3. **TASK-AUTH-C**: `2026-03-24-TASK-AUTH-C-LOGIN-EGG-UPDATE.md`
   - login.egg.md: description update, localStorage key references
   - Model: haiku
   - Dependencies: TASK-AUTH-B (for localStorage key consistency)

4. **TASK-AUTH-D**: `2026-03-24-TASK-AUTH-D-HIVENODE-CONFIG-REBRAND.md`
   - hivenode config.py, dependencies.py, jwks_cache.py
   - Rename ra96it_* → auth_* config fields
   - Dual-issuer JWT validation (accept both "ra96it" and "hodeia")
   - Model: haiku
   - Dependencies: None

5. **TASK-AUTH-E**: `2026-03-24-TASK-AUTH-E-DEPLOYMENT-DOCS-UPDATE.md`
   - deployment-env.md: document migration, new env var names
   - Model: haiku
   - Dependencies: TASK-AUTH-A, TASK-AUTH-D (for env var name consistency)

6. **TASK-AUTH-F**: `2026-03-24-TASK-AUTH-F-EGGRESOLVER-CLEANUP.md`
   - eggResolver.ts: mark ra96it entries as deprecated, keep backwards compat
   - Model: haiku
   - Dependencies: None

## What Was Done

**Codebase Analysis:**
- Read 8 files to understand current ra96it references
- Identified 4 frontend files with ra96it env var/text references
- Identified 7 backend files with ra96it config references
- Verified eggResolver.ts already has hodeia.me mappings (lines 127-128)
- Verified authStore uses ra96it_token/ra96it_user keys (lines 10-11)
- Verified dependencies.py JWT issuer validation is hardcoded to "ra96it" (line 214)

**Task File Structure:**
- All tasks follow 8-section response template from BOOT.md
- All file paths are absolute
- All tasks include TDD requirements
- All tasks specify haiku model (straightforward find-and-replace scope)
- Migration logic specified for TASK-AUTH-B (backwards compat critical)
- Dual-issuer strategy specified for TASK-AUTH-D (transition period compat)

**Dependency Graph:**
```
Wave 1 (parallel): TASK-AUTH-A, TASK-AUTH-B, TASK-AUTH-D, TASK-AUTH-F
Wave 2 (parallel): TASK-AUTH-C (depends on AUTH-B), TASK-AUTH-E (depends on AUTH-A, AUTH-D)
```

## Review Checklist for Q33NR

Please verify:

1. **No hardcoded colors** — N/A (no CSS changes expected)
2. **No files over 500 lines** — All files are under 300 lines, well within limit
3. **TDD specified** — All code tasks (A, B, D, F) include test-first requirements
4. **No stubs** — All tasks explicitly forbid stubs
5. **Absolute paths** — All file paths in tasks are absolute
6. **Missing deliverables** — Each task has specific deliverables, acceptance criteria
7. **Gaps vs briefing** — All 6 briefing tasks covered, no gaps

**Specific concerns to review:**

- **TASK-AUTH-B migration logic**: Is the backwards-compat strategy clear? (copy old→new, delete old, idempotent)
- **TASK-AUTH-D dual-issuer**: Is the JWT issuer validation strategy clear? (accept both "ra96it" and "hodeia")
- **TASK-AUTH-E docs**: Should this also document the hodeia.me DNS status (nameservers not updated yet)?
- **Wave 2 dependencies**: Should TASK-AUTH-C and TASK-AUTH-E run after Wave 1 completes, or can they run in parallel with Wave 1?

## Proposed Dispatch Order

**Wave 1** (4 tasks, parallel):
- TASK-AUTH-A (frontend env var + UI text)
- TASK-AUTH-B (frontend localStorage keys + migration)
- TASK-AUTH-D (backend config + dual-issuer)
- TASK-AUTH-F (eggResolver comments)

**Wave 2** (2 tasks, parallel, after Wave 1):
- TASK-AUTH-C (login.egg.md docs)
- TASK-AUTH-E (deployment-env.md docs)

Total: 6 bees, 2 waves, all haiku model

## Clock / Cost / Carbon

- **Clock:** 45 minutes (codebase read + task file authoring)
- **Cost:** $0.15 (Sonnet, ~25k tokens input + 8k output)
- **Carbon:** ~0.02 kg CO2e

## Issues / Follow-ups

1. **Testing App.tsx references**: The file `App.shouldShowLanding.test.tsx` has hardcoded checks for `ra96it.com` hostnames (lines 64, 81-93). Should these be updated to also check `hodeia.me`? Or left as-is for backwards compat testing?

2. **DNS status documentation**: The briefing mentions "hodeia.me DNS infrastructure is ready on Cloudflare but nameservers haven't been updated at registrars yet." Should TASK-AUTH-E document this, or is it premature?

3. **Env var transition**: After these tasks complete, the old env vars (VITE_RA96IT_API, RA96IT_PUBLIC_KEY) will still work if set, but new deployments should use the new names. Should we add a deprecation warning log in code, or just rely on docs?

4. **eggResolver hodeia.me entries**: Lines 127-128 already map `hodeia.me` and `www.hodeia.me` to `login`. No code changes needed there, but TASK-AUTH-F will add tests to verify this works.

## Next Steps

Awaiting Q33NR review and approval to dispatch bees.
