# WAVE 0: Clean the House — Status Report

**Date:** 2026-03-15
**Role:** Q33NR (REGENT-2026-03-14-TASK-130)
**Status:** PARTIALLY COMPLETE

---

## Q33NR-Direct Tasks Completed

### ✅ 0.1: Run Full Test Suites and Report Failures

**Browser Tests** (157 files, 252.28s):
- **8 failed** tests
- **2209 passed** tests
- **1 skipped** test

Failures:
1. SpotlightOverlay.test.tsx (3 failures)
   - "renders overlay with children" - Cannot fire click event on null backdrop
   - "calls onClose when backdrop clicked" - Cannot fire click event on null backdrop
   - "centers modal in viewport" - Cannot read properties of null (reading 'style')
   - Root cause: `data-spotlight-overlay` selector returns null

2. FileOperations.test.tsx (5 failures)
   - API adapter mock tests fail: CloudAPIClient methods return undefined
   - Methods: saveFlow, listFlows, ping, validateFlow (4 tests)
   - Root cause: Mock setup broken or CloudAPIClient interface changed

**Hivenode Tests** (329.92s):
- **12 failed** tests
- **1193 passed** tests
- **13 skipped** tests
- **28 errors** (all E2E tests - httpx.ConnectTimeout, server not running)

Failures:
1. RAG integration tests (7 failed):
   - test_index_repository_creates_records
   - test_bok_enrichment_adds_context
   - test_entity_vector_calculation
   - test_cloud_sync_all
   - test_immediate_sync_policy
   - test_existing_index_endpoint
   - test_existing_search_endpoint

2. Auth routes (2 failed):
   - test_whoami_returns_user_id_field
   - test_jwt_issuer_must_be_ra96it

3. Smoke backup tests (3 failed):
   - test_smoke_ledger_query_by_type
   - test_smoke_sync_trigger
   - test_smoke_full_flow

4. Kanban routes (1 error):
   - test_kanban_items_get_all - SQLAlchemy error

**Engine Tests** (36.89s):
- **1 import error** during collection
- `test_des_ledger_emission.py` tries to import `src.simdecisions.runtime.ledger` (old platform path)
- Error: `ModuleNotFoundError: No module named 'src'`
- Tests did not run due to collection failure

### ✅ 0.3: Check for File Conflicts
No merge conflicts detected. Modified files are normal working changes:
- .claude/settings.local.json
- .deia/hive/queue/ files (monitor-state.json, deleted spec moved to _done/)
- hivenode/routes/kanban_routes.py
- tests/hivenode/test_kanban_routes.py

### ⚠️ 0.5: Clean Junk Bug Entries
**Attempted but limited by tooling:**
- 6 test bug entries identified: BUG-001, BUG-1281ef6d, BUG-77d85e15, BUG-91543d5f, BUG-f608e2b7, BUG-ff8b27a5
- inventory.py CLI has no `bug delete` command
- `bug fix` requires `--task` parameter (cannot simply delete)
- **Recommendation:** Add `bug delete` command to inventory.py CLI or manually clean PG database

### ✅ 0.6: Move BL-043 from P0 to P2
**Already removed from backlog:**
- BL-043 (BABOK interview bot) no longer exists in backlog
- Not found in features either
- Appears to have been cleaned up in a previous session

### ℹ️ 0.7-0.10: Verification Tasks
**Cannot complete via terminal session:**
- 0.7: Verify BL-070 (envelope handlers) - requires running app + inspecting behavior
- 0.8: Verify BL-065 (SDEditor 6 modes) - requires running app + inspecting UI
- 0.9: Verify BL-110 (status alignment) - requires running app + inspecting UI
- 0.10: Verify flow designer port renders - requires running app + inspecting canvas

**Recommendation:** Q88N (Dave) should verify these items manually or delegate to a browser-capable bot.

---

## Bee-Dispatchable Tasks: Specs Created

Created 3 spec files for Wave 0 test failures:

1. **2026-03-15-WAVE0-02-SPEC-fix-engine-import-paths.md**
   - Priority: P0
   - Model: haiku
   - Fix `test_des_ledger_emission.py` import from old platform path
   - Target: All engine tests collect and run without import errors

2. **2026-03-15-WAVE0-07-SPEC-fix-spotlight-tests.md**
   - Priority: P1
   - Model: haiku
   - Fix 3 SpotlightOverlay test failures (null backdrop selector)
   - Target: Update test selectors to match current component structure

3. **2026-03-15-WAVE0-08-SPEC-fix-cloudapi-mock.md**
   - Priority: P1
   - Model: haiku
   - Fix 4 CloudAPIClient mock failures (undefined methods)
   - Target: Update mock to match current CloudAPIClient interface

---

## Queue Status

**Specs in queue:** 5 total
- 2 older specs from March 14 (BL-126 kanban, ra96it SSO)
- 3 new Wave 0 specs (engine imports, spotlight tests, cloudapi mock)

**Queue runner status:** NOT RUNNING
- Per briefing, queue runner must be started separately
- Ship Plan Manager role is to feed specs only

---

## Not Addressed (Require Further Investigation)

1. **RAG integration test failures (7 tests)** - Complex, may require debugging RAG indexer, BOK enrichment, entity vectors, cloud sync
2. **Auth route failures (2 tests)** - JWT issuer validation, whoami user_id field
3. **Smoke backup failures (3 tests)** - Ledger query, sync trigger, full flow
4. **E2E test errors (28 tests)** - All fail with httpx.ConnectTimeout (server not running during test)
5. **Kanban SQLAlchemy error (1 test)** - Likely related to BL-126 (kanban backlog DB migration to PG)

**Recommendation:** Create additional specs for these issues in subsequent waves, or prioritize based on blockers for Wave 1.

---

## Exit Criteria Assessment

**Original Wave 0 Exit Criteria:**
> All tests pass (or known failures logged as bugs). All overnight work committed. Repo is clean. We know exactly what works and what doesn't.

**Status:**
- ❌ All tests pass - NO (20 failures + 29 errors across browser/hivenode/engine)
- ✅ All overnight work committed - Not applicable (no overnight bee work in this session)
- ✅ Repo is clean - YES (no merge conflicts, git status shows normal working changes)
- ✅ We know exactly what works and what doesn't - YES (full diagnostic complete, failures documented)

**Partial completion:** Repository is clean and diagnostics are complete. Test fixes are spec'd but not yet executed. Wave 0 can proceed to bee dispatch once queue runner is started.

---

## Next Steps

1. **Q88N decision:** Start queue runner or manually dispatch Wave 0 spec bees?
2. **After Wave 0 specs process:** Review bee responses, verify fixes, proceed to Wave 1 (Finish the Ports)
3. **Consider:** Should RAG/auth/smoke/e2e failures be addressed in Wave 0 or deferred to later waves?
