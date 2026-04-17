# TASK-AUTH-D: Hivenode Auth Config Rebrand (ra96it → auth)

**Date:** 2026-03-24
**Model:** Haiku
**Priority:** P1
**Layer:** Backend (hivenode config + auth)

---

## Objective

Rebrand hivenode auth configuration from ra96it-specific naming to generic auth_* naming. Update JWT issuer validation to accept BOTH ra96it AND hodeia issuers for backwards compatibility during the auth provider transition period.

---

## Context

ShiftCenter is migrating from "ra96it" auth provider branding to "hodeia" branding. This task updates the hivenode backend to use generic auth_* config field names and dual-issuer JWT validation.

This is part of a larger auth rebrand (AUTH-A through AUTH-F). Other tasks handle frontend, authStore, and EGG files. This task is **BACKEND ONLY** — config fields and JWT validation.

**Current state:**
- Config fields: ra96it_public_key, ra96it_public_key_path, ra96it_jwks_url
- JWT issuer validation: hardcoded `issuer="ra96it"` in dependencies.py
- Default JWKS URL: `https://ra96it.com/.well-known/jwks.json`
- Method name: `get_ra96it_public_key()`

**Target state:**
- Config fields: auth_public_key, auth_public_key_path, auth_jwks_url
- JWT issuer validation: accepts `["ra96it", "hodeia"]` (dual-issuer list)
- Default JWKS URL: `https://hodeia.com/.well-known/jwks.json`
- Method name: `get_auth_public_key()`

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
   - Lines 46-49: config field declarations
   - Lines 154-160: get_ra96it_public_key() method
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`
   - Lines 214, 226: issuer="ra96it" in jwt.decode()
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\services\jwks_cache.py`
   - Line 26: docstring with ra96it URL example
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`
   - Lines 207-211: JWKS cache initialization using ra96it_ config fields
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py`
   - Lines 72, 99: ra96it_public_key fixture usage
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_routes.py`
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_identity.py`
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py`

---

## Deliverables

### 1. Config Field Renaming (config.py)
- [ ] Rename `ra96it_public_key` → `auth_public_key`
- [ ] Rename `ra96it_public_key_path` → `auth_public_key_path`
- [ ] Rename `ra96it_jwks_url` → `auth_jwks_url`
- [ ] Update default for `auth_jwks_url` to `https://hodeia.com/.well-known/jwks.json`
- [ ] Rename method `get_ra96it_public_key()` → `get_auth_public_key()`
- [ ] Update method docstring and error message to reference "auth" not "ra96it"
- [ ] Update env var references in error messages to `HIVENODE_AUTH_PUBLIC_KEY` and `HIVENODE_AUTH_PUBLIC_KEY_PATH`

### 2. Dual-Issuer JWT Validation (dependencies.py)
- [ ] Change `issuer="ra96it"` to `issuer=["ra96it", "hodeia"]` in BOTH jwt.decode() calls (lines 214 and 226)
- [ ] This enables backwards compatibility — JWTs from EITHER issuer validate during transition

### 3. Update JWKS Cache References (jwks_cache.py)
- [ ] Update docstring (line 26) to reference hodeia as primary example: `https://hodeia.com/.well-known/jwks.json`
- [ ] Add comment noting ra96it backwards compatibility

### 4. Update Main.py Initialization (main.py)
- [ ] Replace `settings.ra96it_jwks_url` → `settings.auth_jwks_url` (line 208)
- [ ] Replace `settings.get_ra96it_public_key()` → `settings.get_auth_public_key()` (line 209)
- [ ] Replace `settings.ra96it_public_key` → `settings.auth_public_key` (line 209)
- [ ] Replace `settings.ra96it_public_key_path` → `settings.auth_public_key_path` (line 209)

### 5. Update Tests (all test files)
- [ ] conftest.py: Replace `ra96it_public_key=TEST_PUBLIC_KEY` → `auth_public_key=TEST_PUBLIC_KEY` (lines 72, 99)
- [ ] Search test files for any remaining ra96it_ references and update to auth_*
- [ ] Add new test: verify dual-issuer acceptance (create test JWT with issuer="hodeia", verify it passes)
- [ ] Add new test: verify backwards compat (create test JWT with issuer="ra96it", verify it passes)
- [ ] Ensure all existing auth tests still pass

---

## Test Requirements

### Tests to Write FIRST (TDD)

#### Test File: `tests/hivenode/test_auth_dual_issuer.py` (NEW)
Create new test file with dual-issuer tests:

- [ ] `test_jwt_verification_with_ra96it_issuer()` — create JWT with issuer="ra96it", verify it decodes successfully
- [ ] `test_jwt_verification_with_hodeia_issuer()` — create JWT with issuer="hodeia", verify it decodes successfully
- [ ] `test_jwt_verification_rejects_wrong_issuer()` — create JWT with issuer="unknown", verify it raises InvalidIssuerError
- [ ] `test_config_fields_renamed()` — verify settings.auth_public_key, settings.auth_public_key_path, settings.auth_jwks_url exist
- [ ] `test_get_auth_public_key_method_exists()` — verify settings.get_auth_public_key() works
- [ ] `test_default_auth_jwks_url_is_hodeia()` — verify default URL points to hodeia.com

**Test count target:** 6+ new tests

#### Update Existing Tests
- [ ] conftest.py: update fixture field names
- [ ] test_auth_routes.py: verify no breakage
- [ ] test_auth_identity.py: verify no breakage
- [ ] test_rate_limiter.py: verify no breakage

### Edge Cases to Test
- [ ] JWT with issuer="ra96it" + audience="shiftcenter" → PASS
- [ ] JWT with issuer="hodeia" + audience="shiftcenter" → PASS
- [ ] JWT with issuer="ra96it" + audience="deiasolutions" → PASS
- [ ] JWT with issuer="hodeia" + audience="deiasolutions" → PASS
- [ ] JWT with issuer="other" → FAIL (InvalidIssuerError)
- [ ] Config with auth_public_key set → get_auth_public_key() returns it
- [ ] Config with auth_public_key_path set → get_auth_public_key() reads file
- [ ] Config with neither set → get_auth_public_key() raises ValueError

### All Tests Must Pass
Run after implementation:
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest tests/hivenode/test_auth_dual_issuer.py -v
python -m pytest tests/hivenode/test_auth_routes.py -v
python -m pytest tests/hivenode/test_auth_identity.py -v
python -m pytest tests/hivenode/test_rate_limiter.py -v
python -m pytest tests/hivenode/conftest.py -v
```

---

## Constraints

- **No file over 500 lines** — config.py is currently 165 lines (safe)
- **No stubs** — full implementation required
- **TDD** — write tests first, then implementation
- **Dual-issuer MUST work** — do NOT break existing ra96it JWTs
- **Backwards compatibility** — old env vars like HIVENODE_RA96IT_PUBLIC_KEY should ideally still work via pydantic Field aliases if feasible (optional stretch goal, not required)
- **No breaking changes** — existing ra96it JWT validation continues to work

---

## Acceptance Criteria

- [ ] Config fields renamed: ra96it_public_key → auth_public_key, ra96it_public_key_path → auth_public_key_path, ra96it_jwks_url → auth_jwks_url
- [ ] Method renamed: get_ra96it_public_key() → get_auth_public_key()
- [ ] Default auth_jwks_url = "https://hodeia.com/.well-known/jwks.json"
- [ ] JWT issuer validation accepts list: ["ra96it", "hodeia"]
- [ ] All references in main.py updated to auth_*
- [ ] All references in jwks_cache.py docstrings updated (hodeia primary, ra96it noted for compat)
- [ ] Tests updated: conftest.py uses auth_public_key
- [ ] New tests: test_auth_dual_issuer.py created with 6+ tests, all passing
- [ ] Existing tests: test_auth_routes.py, test_auth_identity.py, test_rate_limiter.py all still pass
- [ ] No hardcoded ra96it strings in config field names (docstrings/comments OK for backwards compat notes)
- [ ] Build verification: all hivenode tests pass

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-D-RESPONSE.md`

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

---

## Notes

- This is part of a larger auth rebrand initiative (AUTH-A through AUTH-F)
- Other tasks handle frontend (login page), authStore, EGG files, and deployment docs
- This task is BACKEND ONLY — config and JWT validation
- The dual-issuer approach is temporary during migration but should remain robust indefinitely
- After full migration, a future task may remove ra96it issuer support (not in scope here)
- PyJWT's jwt.decode() accepts `issuer` as either a string OR a list — passing a list means "accept any of these"
- Use `import jwt` (PyJWT library) for JWT operations
- Use same TEST_PRIVATE_KEY and TEST_PUBLIC_KEY from conftest.py for generating test JWTs

---

**End of Task File**
