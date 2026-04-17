# Q33N Coordination Report: Fix E2E Server Startup Timeout

**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-fix-e2e-se
**Spec:** `.deia/hive/queue/2026-03-16-1103-SPEC-fix-R16-e2e-server-fixture.md`
**Model Assignment:** sonnet
**Priority:** P0.93

---

## Summary

E2E test suite is experiencing widespread failures due to the hivenode subprocess failing to start within the 10-second timeout. All 28 E2E tests fail with `httpx.ConnectTimeout` errors during fixture setup.

I have investigated the root cause and enhanced the existing task file with detailed analysis and investigation steps.

---

## Root Cause Analysis

**Primary Issue: VolumeRegistry initialization**

The E2E fixture (`e2e_server` in `test_e2e.py`) creates a minimal `volumes.yml` config file:

```yaml
volumes:
  home:
    type: local
    root: {storage_root}
```

However, `hivenode/main.py` line 38 calls `VolumeRegistry()` without a `config_path` argument:

```python
volume_registry = VolumeRegistry()  # Uses default config
```

This causes VolumeRegistry to call `get_default_config()` which tries to initialize cloud storage and may require environment variables (SHIFTCENTER_CLOUD_URL, SHIFTCENTER_AUTH_TOKEN) that are not set in the E2E test environment.

**Secondary Issues (to be verified by BEE):**
1. Other startup dependencies may also fail in test context:
   - `_find_repo_root()` - does it work from test subprocess?
   - Node announcement (local mode) - does it need network access?
   - JWKS cache initialization - does it try to fetch from network?
   - Sync engine startup - does it fail if config.yml doesn't exist?

2. The fixture already tries to capture subprocess stderr (lines 94-101), but it may not be working properly

---

## Task File Status

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-R16-fix-e2e-server-fixture.md`

**Status:** Enhanced with detailed analysis

I found that the task file already existed (created by an earlier process). I have updated it with:

1. **Detailed root cause analysis** - explaining the VolumeRegistry config issue
2. **Investigation steps** - specific actions to capture stderr and verify the issue
3. **Fix options** - three possible approaches to resolve the config path problem
4. **Verification requirements** - ensuring no regressions and all tests run

The task file is now ready for BEE dispatch.

---

## Proposed Solution Approaches

**Option A: Add HIVENODE_VOLUMES_CONFIG env var**
- Modify `hivenode/main.py` to check for `HIVENODE_VOLUMES_CONFIG` env var
- Pass it to `VolumeRegistry(config_path=...)`
- E2E fixture sets this env var pointing to its `volumes.yml`

**Option B: Auto-detect test context**
- Modify `storage/config.py` to check for `HIVENODE_STORAGE_ROOT` env var
- If set, generate a minimal test config instead of using default
- Less invasive to main.py

**Option C: Use standard config location**
- E2E fixture writes volumes.yml to `~/.shiftcenter/volumes.yml`
- VolumeRegistry already checks this location
- Less clean: pollutes user's home directory during tests

**Recommendation:** Option A is cleanest and most explicit.

---

## Files Involved

**Core files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (E2E fixture)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (hivenode app startup)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (VolumeRegistry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\config.py` (config loading)

**Supporting files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings)

---

## Acceptance Criteria

From spec:
- [ ] E2E test server starts successfully
- [ ] 28 E2E tests pass (or pre-existing failures documented)
- [ ] No regressions

Enhanced criteria in task file:
- [ ] Server starts within 10-second timeout
- [ ] Server responds to /health with 200 OK
- [ ] All 28 E2E tests run to completion (not ConnectTimeout)
- [ ] Pass/fail status documented for each test
- [ ] Any pre-existing failures documented with root cause
- [ ] No regressions: hivenode unit tests pass

---

## Next Steps

**Q33NR Decision Required:**

1. **Review the enhanced task file** - does it have sufficient detail for a sonnet BEE?
2. **Approve solution approach** - Option A (env var), B (auto-detect), or C (standard location)?
3. **Dispatch approval** - should I dispatch the BEE now, or do you want further refinement?

If approved, I will dispatch:
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-R16-fix-e2e-server-fixture.md \
  --model sonnet --role bee --inject-boot
```

---

## Estimated Scope

**Model:** sonnet (as specified)
**Complexity:** Medium - clear root cause, needs investigation to confirm and verify fix
**Lines changed:** ~10-20 lines across 2-3 files
**Test impact:** Should fix all 28 E2E test ConnectTimeout errors

---

**Q33N Status:** Awaiting Q33NR review and dispatch approval
