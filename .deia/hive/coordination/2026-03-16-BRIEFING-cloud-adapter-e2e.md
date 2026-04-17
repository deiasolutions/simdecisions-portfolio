# BRIEFING: Cloud Storage Adapter End-to-End Verification

**Date:** 2026-03-16
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** SPEC-w3-06-cloud-adapter-e2e.md
**Priority:** P1
**Model Assignment:** sonnet

---

## Objective

Verify the cloud:// storage adapter works end-to-end on the deployed Railway hivenode. Write integration tests that confirm read, write, list, delete operations against the Railway deployment, with JWT auth and offline error handling.

---

## Context

The cloud storage adapter was built in overnight session (TASK-099 through TASK-102). Files exist:

- `hivenode/storage/adapters/cloud.py` — CloudAdapter class, HTTP client to remote hivenode
- `hivenode/storage/registry.py` — VolumeRegistry with adapter instantiation
- `hivenode/routes/storage_routes.py` — Storage routes (read/write/list/stat/delete/volumes)
- `hivenode/config.py` — HivenodeConfig with mode detection

The dependency SPEC-3000 (vercel-railway-repoint) is complete. Railway hivenode is deployed.

---

## What Q33N Must Do

1. **Read the existing implementation files first:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (for JWT verification)

2. **Write integration tests** (not unit tests — these test the full HTTP stack):
   - Test POST /storage/write with volume=cloud:// → writes to Railway persistent volume
   - Test POST /storage/read with volume=cloud:// → reads file back
   - Test POST /storage/list with volume=cloud:// → lists directory
   - Test POST /storage/delete with volume=cloud:// → deletes file
   - Test JWT requirement: all routes reject requests without valid JWT when mode=cloud
   - Test offline behavior: if cloud unreachable, /storage/write returns {queued: true}, /storage/read raises VolumeOfflineError with 503 or 500

3. **Test file path:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter_e2e.py` (new file)

4. **Test approach:**
   - Use real HTTP calls (httpx.Client or TestClient from FastAPI)
   - If Railway deployment is live: test against live Railway URL with real JWT
   - If Railway is not accessible: run local hivenode in cloud mode with temp dir simulating Railway volume
   - Minimum 6 integration tests covering all acceptance criteria

5. **Edge cases to test:**
   - File not found (404)
   - Invalid JWT (403)
   - Cloud offline (503 or VolumeOfflineError)
   - List empty directory (returns [])
   - Delete non-existent file (404)

---

## Acceptance Criteria (from spec)

- [ ] POST /storage/write with volume=cloud:// writes to Railway persistent volume
- [ ] POST /storage/read with volume=cloud:// reads the file back
- [ ] POST /storage/list with volume=cloud:// lists the directory
- [ ] POST /storage/delete with volume=cloud:// deletes the file
- [ ] JWT required on all storage routes when HIVENODE_MODE=cloud
- [ ] Offline behavior: if cloud unreachable, return VOLUME_OFFLINE error (not crash)
- [ ] 6+ integration tests using real HTTP calls

---

## Smoke Test (from spec)

- [ ] From browser: save a chat → cloud hivenode writes file → refresh page → chat loads from cloud

This smoke test is manual. Include instructions in the response file on how to run it manually.

---

## Constraints

- All file paths absolute (Windows format)
- No file over 500 lines (modularize at 500)
- TDD: tests first, then implementation (but implementation already exists — just need tests)
- No stubs
- No hardcoded colors (not applicable to this task)
- Response file with all 8 sections

---

## Depends On

- SPEC-3000 (vercel-railway-repoint) — COMPLETE (verified in `_done/`)

---

## What to Return

Write task files for Q33NR review. Do NOT dispatch bees yet. Wait for Q33NR approval.

Task files should be bee-sized (one file per logical unit). For this spec, likely 1-2 tasks:

1. TASK-XXX: Write cloud adapter E2E integration tests
2. TASK-XXX+1: (Optional) Manual smoke test instructions or browser-side test if needed

Return to Q33NR with:
- List of task files created
- Summary of what each task delivers
- Estimated test count per task
- Any issues or clarifications needed

---

## Notes

- CloudAdapter raises `VolumeOfflineError` on network errors (httpx.ConnectError, TimeoutException, NetworkError)
- Storage routes use `verify_jwt_or_local()` dependency — local mode bypasses JWT, cloud mode requires it
- Registry resolves "cloud" adapter type by reading env vars SHIFTCENTER_CLOUD_URL and SHIFTCENTER_AUTH_TOKEN
- If Railway is not accessible, tests can run against local hivenode in cloud mode with temp directory

---

**End of briefing. Q33N: read the files, write task files, return for review.**
