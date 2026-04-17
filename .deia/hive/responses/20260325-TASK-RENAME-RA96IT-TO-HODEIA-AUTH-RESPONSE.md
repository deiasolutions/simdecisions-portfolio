# TASK-RENAME-RA96IT-TO-HODEIA-AUTH: Rename ra96it module to hodeia_auth -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-25

## Files Modified

### Test directory (already renamed via git mv)
- `tests/hodeia_auth/` (entire directory, previously `tests/ra96it/`)

### Test files - import updates
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\conftest.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_dev_login.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_audit.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_login.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_mfa.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_oauth.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_jwt.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_jwks.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_token_refresh.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_token_revoke.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_password.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hodeia_auth\test_register.py`

### Config files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hodeia_auth\nixpacks.toml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\nixpacks.toml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml`

## What Was Done

- Verified test directory `tests/ra96it/` was already renamed to `tests/hodeia_auth/` via git mv (per git status)
- Verified internal imports in `hodeia_auth/` files were already updated (no `from ra96it.` found)
- Verified external imports in `hivenode/` and `_tools/` were already updated (no `from ra96it.` found)
- Updated all 13 test files in `tests/hodeia_auth/`:
  - Changed `from ra96it.` to `from hodeia_auth.` (absolute imports)
  - Changed `patch("ra96it.` to `patch("hodeia_auth.` (unittest.mock patches)
  - Updated docstrings referencing "ra96it" to "hodeia_auth"
- Updated `conftest.py` patch statements in fixture definitions
- Updated `hodeia_auth/nixpacks.toml`:
  - `pip install -r ra96it/requirements.txt` → `pip install -r hodeia_auth/requirements.txt`
  - `uvicorn ra96it.main:app` → `uvicorn hodeia_auth.main:app`
- Updated root `nixpacks.toml`:
  - `uvicorn ra96it.main:app` → `uvicorn hodeia_auth.main:app`
- Updated `pyproject.toml`:
  - `packages = ["ra96it", "ra96it.services", "ra96it.routes", ...]` → `packages = ["hodeia_auth", "hodeia_auth.services", "hodeia_auth.routes", ...]`
- Did NOT change:
  - Domain references to `ra96it.com` (real domain, per task spec)
  - `.deia/` coordination docs (task history, per task spec)
  - `hodeia_auth/config.py` (already had `jwt_issuer: str = "hodeia"`)

## Test Results

- Test command: `python -m pytest tests/hodeia_auth/ -q --tb=no`
- **85 tests passed, 0 failed**
- All import changes verified working
- JWT tests pass with updated issuer ("hodeia")
- OAuth tests pass with updated patch paths
- MFA, login, registration, token refresh/revoke tests all pass

## Build Verification

Tests passed:
```
........................................................................ [ 84%]
.............                                                            [100%]
85 passed in 24.72s
```

No build step required (Python module rename).

## Acceptance Criteria

- [x] Test directory renamed from `tests/ra96it/` to `tests/hodeia_auth/`
- [x] All imports in `tests/hodeia_auth/` updated from `ra96it` to `hodeia_auth`
- [x] All patch() calls updated from `ra96it.` to `hodeia_auth.`
- [x] `nixpacks.toml` files updated (both `hodeia_auth/` and root)
- [x] `pyproject.toml` packages list updated
- [x] Domain references to `ra96it.com` preserved (not changed)
- [x] `.deia/` coordination docs preserved (not changed)
- [x] All tests pass (85/85)
- [x] No hardcoded `ra96it` module references remain in source code

## Clock / Cost / Carbon

- **Clock:** ~12 minutes (sequential file updates, test runs)
- **Cost:** ~$0.05 USD (Sonnet model, moderate token usage)
- **Carbon:** ~2g CO2e (estimated based on compute time)

## Issues / Follow-ups

None. All changes complete and verified.

**Note:** The `hodeia_auth/` directory and internal module imports were already renamed prior to this task. This task completed the remaining references in:
1. Test files (13 files, import and patch statements)
2. Build config files (2 nixpacks.toml, 1 pyproject.toml)

Railway environment variable `NIXPACKS_START_CMD` will need to be updated separately on Railway platform to reference `hodeia_auth.main:app` instead of `ra96it.main:app`. This is a deployment config change, not a code change.
