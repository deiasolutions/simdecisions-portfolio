# TASK-193: Volume Sync Smoke Test Script

**Date:** 2026-03-16
**Model Assignment:** Haiku
**Priority:** P2
**Estimated Complexity:** S

---

## Objective

Create a manual smoke test script that Dave can run to verify sync works on his actual local hivenode + Railway cloud hivenode. This is a script for manual verification, not an automated test suite.

---

## Context

The volume sync system is fully implemented. TASK-192 provides automated E2E tests with temp directories. This task provides a smoke test script that Dave can run against his real local hivenode (localhost:8420) and his real cloud hivenode (Railway deployment).

**Purpose:** Verify that sync works in production between Dave's local machine and Railway cloud.

**What it does:**
1. Verify local hivenode is running (check `http://localhost:8420/health`)
2. Verify cloud hivenode is reachable (check Railway health endpoint)
3. Write a test file to home:// via `POST /storage/write`
4. Trigger sync via `POST /sync/trigger`
5. Read the file from cloud:// via `POST /storage/read`
6. Verify content matches
7. Delete test file from both volumes
8. Print success message

**This is NOT a pytest test file.** This is a standalone Python script that can be run via `python tests/smoke/smoke_sync.py`.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py` (sync routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (storage routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` (reference for how to call routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 6: Volume Sync requirements)

---

## Deliverables

### Primary Deliverable

- [ ] **NEW FILE:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\smoke_sync.py`
  - Standalone Python script (NOT a pytest test)
  - Runnable via `python tests/smoke/smoke_sync.py`
  - Prints clear success/failure messages
  - Cleans up test files (deletes test file from both volumes)
  - Uses `httpx` to call local and cloud hivenode HTTP routes
  - Uses environment variables for cloud hivenode URL (default: `https://api.shiftcenter.com`)
  - Under 200 lines

### Script Behavior

```bash
$ python tests/smoke/smoke_sync.py

[1/7] Checking local hivenode health...
✓ Local hivenode running at http://localhost:8420

[2/7] Checking cloud hivenode health...
✓ Cloud hivenode reachable at https://api.shiftcenter.com

[3/7] Writing test file to home://...
✓ Wrote test file to home://smoke_test/test_sync.md

[4/7] Triggering sync (home → cloud)...
✓ Sync completed: pushed=1, pulled=0, conflicts=0, skipped=0

[5/7] Reading file from cloud://...
✓ File exists on cloud://smoke_test/test_sync.md
✓ Content matches

[6/7] Cleaning up test files...
✓ Deleted from home://
✓ Deleted from cloud://

[7/7] All checks passed.

SUCCESS: Volume sync is working correctly between local and cloud.
```

If any step fails, print error message and exit with code 1:

```bash
[1/7] Checking local hivenode health...
✗ FAILED: Could not connect to http://localhost:8420
  Error: Connection refused
  Hint: Is your local hivenode running? Try: 8os up

ERROR: Smoke test failed at step 1/7.
```

---

## Test Requirements

### NOT a Pytest Test

This is a standalone Python script. Do NOT use pytest decorators, fixtures, or assertions. Use simple `if` checks and print statements.

### Implementation Notes

- Use `httpx.Client()` (sync client, not async)
- Use environment variable `CLOUD_HIVENODE_URL` (default: `https://api.shiftcenter.com`)
- Use environment variable `LOCAL_HIVENODE_URL` (default: `http://localhost:8420`)
- Write test file to `home://smoke_test/test_sync.md` (so it doesn't clutter user's files)
- Test file content: `"Smoke test at {timestamp}"`
- On cleanup, delete `home://smoke_test/test_sync.md` AND `cloud://smoke_test/test_sync.md`
- If cleanup fails, print warning but don't fail the script
- Print clear error messages with hints (e.g., "Is your local hivenode running? Try: 8os up")

### Error Handling

- If local hivenode unreachable → print error, exit code 1
- If cloud hivenode unreachable → print error, exit code 1
- If write fails → print error, exit code 1
- If sync fails → print error, exit code 1
- If read fails → print error, exit code 1
- If content mismatch → print error with both contents, exit code 1
- If cleanup fails → print warning, exit code 0 (success but warn)

---

## Constraints

1. **File must be under 200 lines.** This is a simple smoke test script.
2. **No pytest.** Use plain Python with httpx.
3. **All file paths must be absolute** in comments and error messages.
4. **Clean up test files** after each run.
5. **Print clear messages** for each step.
6. **Exit with code 0 on success, 1 on failure.**
7. **No hardcoded colors.** (Not applicable — this is a CLI script, can use ANSI codes for terminal colors if desired.)
8. **No stubs.** Fully implement all steps.

---

## Acceptance Criteria

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\smoke_sync.py` created
- [ ] Script is runnable via `python tests/smoke/smoke_sync.py`
- [ ] Script checks local hivenode health (GET /health)
- [ ] Script checks cloud hivenode health (GET /health)
- [ ] Script writes test file to home:// (POST /storage/write)
- [ ] Script triggers sync (POST /sync/trigger)
- [ ] Script reads test file from cloud:// (POST /storage/read)
- [ ] Script verifies content matches
- [ ] Script deletes test files from both volumes (POST /storage/delete)
- [ ] Script prints clear success message if all steps pass
- [ ] Script prints clear error message if any step fails
- [ ] Script exits with code 0 on success, 1 on failure
- [ ] Script under 200 lines

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-193-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — NOT applicable (this is not a test file, it's a smoke script)
5. **Build Verification** — Run the script against local hivenode (if available) or describe expected behavior
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Notes for BEE

- Use `httpx.Client()` for sync HTTP calls (not AsyncClient)
- Use `datetime.now(timezone.utc).isoformat()` for timestamp in test file content
- Use `os.environ.get("CLOUD_HIVENODE_URL", "https://api.shiftcenter.com")` for cloud URL
- Use `os.environ.get("LOCAL_HIVENODE_URL", "http://localhost:8420")` for local URL
- Print progress with clear step numbers: `[1/7]`, `[2/7]`, etc.
- Use checkmark `✓` for success, `✗` for failure
- If you want to use ANSI colors for terminal output, that's fine (optional)
- Clean up test files even if earlier steps failed (use try/finally or similar pattern)
