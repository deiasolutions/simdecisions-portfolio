# BRIEFING: AUTH-D — Hivenode Auth Config Rebrand (ra96it → auth)

**Date:** 2026-03-24
**For:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Priority:** P1
**Model Assignment:** haiku

---

## Objective

Rebrand hivenode auth configuration from ra96it-specific naming (ra96it_public_key, ra96it_public_key_path, ra96it_jwks_url) to generic auth_* naming (auth_public_key, auth_public_key_path, auth_jwks_url). Update JWT issuer validation to accept BOTH ra96it AND hodeia issuers for backwards compatibility during the transition period.

---

## Context

ShiftCenter is rebranding its auth provider from "ra96it" to "hodeia". The hivenode backend currently has ra96it hardcoded in:

1. **Config field names** (hivenode/config.py lines 46-49)
2. **JWT issuer validation** (hivenode/dependencies.py lines 214, 226)
3. **JWKS cache docstrings** (hivenode/services/jwks_cache.py line 26)
4. **Main.py initialization** (hivenode/main.py lines 208-209)

The goal is to make config field names auth-provider-agnostic while maintaining dual-issuer JWT support.

---

## Files Identified

### Config and Services
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
  - Lines 46-49: ra96it_public_key, ra96it_public_key_path, ra96it_jwks_url fields
  - Lines 154-160: get_ra96it_public_key() method
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`
  - Lines 214, 226: issuer="ra96it" hardcoded in jwt.decode()
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\services\jwks_cache.py`
  - Line 26: docstring "https://ra96it.com/.well-known/jwks.json"
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`
  - Lines 207-211: references to ra96it_ config fields in JWKS cache init

### Tests (need updating)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_identity.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py`

---

## Requirements

### 1. Config Field Renaming
- Rename: `ra96it_public_key` → `auth_public_key`
- Rename: `ra96it_public_key_path` → `auth_public_key_path`
- Rename: `ra96it_jwks_url` → `auth_jwks_url`
- Rename method: `get_ra96it_public_key()` → `get_auth_public_key()`
- Update default JWKS URL to use hodeia: `https://hodeia.com/.well-known/jwks.json`

### 2. Dual-Issuer JWT Validation
In `hivenode/dependencies.py`, the `verify_jwt()` function must accept BOTH:
- `issuer="ra96it"` (backwards compat)
- `issuer="hodeia"` (new issuer)

Implementation approach: pass a list of issuers to `jwt.decode()`:
```python
issuer=["ra96it", "hodeia"]
```

This allows JWTs from EITHER issuer to validate during the transition period.

### 3. Update All References
- main.py: update JWKS cache initialization to use auth_* fields
- jwks_cache.py: update docstrings to reference hodeia as primary example
- Search entire hivenode/ directory for any remaining ra96it_ references

### 4. Test Updates
Update test files to:
- Use auth_* field names instead of ra96it_*
- Test dual-issuer acceptance (create test JWTs with both ra96it and hodeia issuers)
- Ensure backwards compatibility with existing ra96it JWTs

---

## Constraints

- **No file over 500 lines**
- **No stubs** — full implementation
- **TDD** — tests first, then implementation
- **Dual-issuer MUST work** — do NOT break existing ra96it JWTs
- **Config changes are non-breaking** — old env vars HIVENODE_RA96IT_PUBLIC_KEY should still work (if feasible via pydantic aliases)

---

## Acceptance Criteria

Your task files must ensure:

- [ ] Config fields renamed: ra96it_* → auth_* in config.py
- [ ] Method renamed: get_ra96it_public_key() → get_auth_public_key()
- [ ] Default auth_jwks_url points to hodeia.com (not ra96it.com)
- [ ] JWT issuer validation accepts BOTH ra96it AND hodeia
- [ ] All references in main.py updated
- [ ] All references in jwks_cache.py docstrings updated
- [ ] Tests updated to use auth_* field names
- [ ] Tests verify dual-issuer acceptance (ra96it and hodeia both work)
- [ ] All existing auth tests still pass
- [ ] No hardcoded ra96it strings in config field names (docstrings/comments OK if explaining backwards compat)

---

## Next Steps for Q33N

1. Read all files listed above
2. Write task files for a single bee (haiku model)
3. Return task files to me (Q33NR) for review
4. After my approval, dispatch the bee
5. Review bee response file
6. Report results to me

---

## Notes

- This is part of a larger auth rebrand initiative (AUTH-A through AUTH-F)
- Other tasks handle frontend (login page), authStore, EGG files, and deployment docs
- This task is BACKEND ONLY — config and JWT validation
- The dual-issuer approach is temporary during migration, but should remain robust (no time limit)
- After full migration, a future task may remove ra96it issuer support (not in scope here)

---

**Q33NR out.**
