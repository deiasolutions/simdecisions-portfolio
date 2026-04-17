# TASK-R16: Fix E2E test server startup timeout

## Objective
Debug and fix why the E2E test fixture fails to start the hivenode subprocess, causing 28 `httpx.ConnectTimeout` errors.

## Context
R13 verification found 28 errors in `tests/hivenode/test_e2e.py`. All fail at setup with `httpx.ConnectTimeout`. The test fixture starts a hivenode subprocess and polls `/health` — but the server never responds.

**Root Cause Analysis (Q33N Investigation):**

The E2E fixture creates a minimal `volumes.yml` config at `tmp_dir / "volumes.yml"` (line 48-54), but `hivenode/main.py` line 38 calls `VolumeRegistry()` without any config_path argument. This causes VolumeRegistry to use `get_default_config()` which tries to initialize cloud storage and may require environment variables (SHIFTCENTER_CLOUD_URL, SHIFTCENTER_AUTH_TOKEN) that are not set in the test environment.

**Additional Issues to Check:**
1. Does VolumeRegistry initialization fail or just use wrong paths?
2. Do other startup dependencies (_find_repo_root, JWKS cache, node announcement) fail in test context?
3. Are environment variables properly passed to the subprocess?
4. Does the fixture properly capture and display subprocess stderr on failure?

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (fixture logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py` (shared fixtures)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (app entry point)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R13-RESPONSE.md`

## Deliverables

**Investigation Phase:**
- [ ] Run one E2E test with verbose output to capture subprocess stderr: `python -m pytest tests/hivenode/test_e2e.py::test_health_returns_ok_status -v -s`
- [ ] Check if subprocess stderr shows import errors or startup failures
- [ ] Verify VolumeRegistry is the root cause by checking if it tries to access undefined env vars

**Fix Phase:**
- [ ] Fix VolumeRegistry initialization (likely needs to accept a config path via env var)
- [ ] Options to consider:
  - Add `HIVENODE_VOLUMES_CONFIG` env var that main.py reads and passes to VolumeRegistry
  - OR modify storage/config.py to check for env var before using default config
  - OR make VolumeRegistry check for `HIVENODE_STORAGE_ROOT` and generate test config
- [ ] Fix any other startup blockers discovered (e.g., _find_repo_root, JWKS cache, node announcement)
- [ ] Run full E2E suite: `python -m pytest tests/hivenode/test_e2e.py -v`
- [ ] Document which tests pass vs fail with clear explanations

**Verification Phase:**
- [ ] Verify hivenode unit tests still pass (no regressions): `cd hivenode && python -m pytest tests/ -v`
- [ ] Verify server starts within 10-second timeout
- [ ] All 28 E2E tests run to completion (no ConnectTimeout)

## Constraints
- Fix only the startup issue — do NOT refactor E2E test logic
- If the server crashes on import, fix the import (likely from a rebuild task side effect)

## Acceptance Criteria
- [ ] E2E test server starts successfully
- [ ] 28 E2E tests pass (or pre-existing failures documented)
- [ ] No regressions

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R16-RESPONSE.md`
All 8 sections required.
