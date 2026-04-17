# TASK-102: Cloud Storage Adapter Integration Tests

## Objective
Write integration tests that verify CloudAdapter + VolumeRegistry + SyncQueue work together end-to-end.

## Context
TASK-099 converted CloudAdapter to sync, TASK-100 fixed registry instantiation, TASK-101 updated config schema. This task verifies the full stack works together.

## Dependencies
- **TASK-099, TASK-100, TASK-101 must all be complete**

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` (from TASK-099)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (from TASK-100)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py` (existing tests)

## Deliverables
- [ ] Create `tests/hivenode/storage/test_cloud_integration.py` — 8+ tests:
  - Registry creates CloudAdapter from config with correct params
  - CloudAdapter.read() returns bytes (not coroutine) when server responds 200
  - CloudAdapter.write() sends PUT request with correct body
  - CloudAdapter raises VolumeOfflineError when server unreachable
  - SyncQueue captures writes during offline
  - SyncQueue.flush() retries writes when server comes back
  - CloudAdapter.list() returns file list from server response
  - CloudAdapter.stat() returns file metadata
- [ ] All tests use `respx` to mock HTTP endpoints (no real network calls)
- [ ] All tests use `tmp_path` for queue directory

## Constraints
- No file over 500 lines
- Use `respx` for HTTP mocking
- Use `tmp_path` for filesystem operations
- Each test must be independent

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-102-RESPONSE.md`

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

## Model Assignment
haiku
