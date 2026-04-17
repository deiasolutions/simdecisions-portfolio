# TASK-208: Cloud Storage Adapter End-to-End Integration Tests

## Objective
Write comprehensive E2E integration tests for the cloud:// storage adapter that verify all operations (read, write, list, delete) work end-to-end with JWT auth, offline handling, and error scenarios.

## Context
The cloud storage adapter (`CloudAdapter`) was built in overnight session (TASK-099 through TASK-102). It provides an HTTP client that calls the cloud hivenode's `/storage/*` routes. The adapter handles offline scenarios by queueing writes and raising `VolumeOfflineError` for reads.

This task writes **integration tests** (not unit tests). These tests verify the full HTTP stack: client → storage routes → adapter → backend storage.

The cloud hivenode is deployed on Railway (SPEC-3000 complete). Tests can run against:
1. **Live Railway deployment** (preferred if accessible with real JWT)
2. **Local hivenode in cloud mode** (fallback for dev/CI environments)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` — CloudAdapter implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` — Storage routes (write, read, list, delete, stat, volumes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — HivenodeConfig with mode detection
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — verify_jwt_or_local() dependency
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` — E2E test fixture pattern (real server in subprocess)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_integration.py` — Existing cloud adapter unit tests (for reference)

## Deliverables
- [ ] New test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter_e2e.py`
- [ ] Fixture: `cloud_e2e_server()` — starts local hivenode in cloud mode with temp persistent volume
- [ ] Fixture: `cloud_client()` — httpx.AsyncClient with JWT auth headers
- [ ] Test: `test_cloud_write_creates_file_on_persistent_volume()` — POST /storage/write with volume=cloud:// writes to persistent volume
- [ ] Test: `test_cloud_read_returns_file_content()` — POST /storage/read with volume=cloud:// reads file back
- [ ] Test: `test_cloud_list_returns_directory_entries()` — POST /storage/list with volume=cloud:// lists directory
- [ ] Test: `test_cloud_delete_removes_file()` — POST /storage/delete with volume=cloud:// deletes file
- [ ] Test: `test_cloud_stat_returns_file_metadata()` — POST /storage/stat returns file metadata
- [ ] Test: `test_storage_routes_require_jwt_in_cloud_mode()` — all routes reject requests without JWT when mode=cloud (401/403)
- [ ] Test: `test_cloud_offline_write_returns_queued_true()` — if cloud unreachable, /storage/write returns {queued: true}
- [ ] Test: `test_cloud_offline_read_raises_503_or_500()` — if cloud unreachable, /storage/read returns 503 or 500 with VolumeOfflineError
- [ ] Test: `test_cloud_read_file_not_found_returns_404()` — reading non-existent file returns 404
- [ ] Test: `test_cloud_delete_file_not_found_returns_404()` — deleting non-existent file returns 404
- [ ] Test: `test_cloud_list_empty_directory_returns_empty_list()` — listing empty directory returns []
- [ ] Test: `test_cloud_invalid_jwt_returns_401_or_403()` — invalid JWT token returns 401 or 403

## Test Requirements
- [ ] **TDD not applicable** — implementation already exists, tests verify behavior
- [ ] **12+ integration tests** covering all acceptance criteria from SPEC-w3-06
- [ ] All tests use **real HTTP calls** via `httpx.AsyncClient` (not mocked transport)
- [ ] Tests run against **local hivenode in cloud mode** with temp persistent volume (for CI compatibility)
- [ ] Use `pytest.mark.asyncio` for async tests
- [ ] Use `pytest.mark.e2e` marker for E2E tests
- [ ] Fixture pattern matches `tests/hivenode/test_e2e.py` (subprocess server, health polling)
- [ ] Edge cases:
  - File not found (404)
  - Invalid JWT (401/403)
  - Cloud offline (503 or VolumeOfflineError)
  - Empty directory list
  - Delete non-existent file
  - Write with offline queueing
  - Read with offline error

## Test Approach

### Cloud E2E Server Fixture
```python
@pytest.fixture(scope="module")
def cloud_e2e_server(tmp_path_factory):
    """
    Start a real hivenode server in cloud mode for E2E tests.

    - HIVENODE_MODE=cloud
    - Temp persistent volume (simulates Railway volume)
    - Temp database
    - Random port
    """
    # Similar to e2e_server fixture in test_e2e.py
    # Set HIVENODE_MODE=cloud
    # Start uvicorn subprocess
    # Poll /health until ready
    # Yield (port, base_url, tmp_dir, persistent_volume_path)
    # Cleanup on teardown
```

### Cloud Client Fixture
```python
@pytest.fixture
async def cloud_client(cloud_e2e_server):
    """
    HTTP client with JWT auth for cloud E2E tests.

    Uses a test JWT token (or generates one if JWT signing is available).
    """
    port, base_url, tmp_dir, volume_path = cloud_e2e_server
    headers = {"Authorization": f"Bearer {test_jwt_token}"}
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30.0) as client:
        yield client
```

### JWT Token Strategy
Since `verify_jwt_or_local()` requires a valid JWT in cloud mode, the tests need a valid JWT token. Options:
1. **Mock JWT in fixture** — patch `verify_jwt_or_local()` to return stub claims
2. **Use test JWT signing** — generate a real JWT with test keys (if ra96it test keys available)
3. **Override dependency** — use FastAPI dependency override to bypass JWT check in tests

**Recommendation:** Use dependency override to bypass JWT for E2E tests. This is standard practice for testing protected routes.

```python
from hivenode.dependencies import verify_jwt_or_local

@pytest.fixture
def override_jwt(cloud_e2e_server):
    """Override JWT dependency for E2E tests."""
    from hivenode.main import app

    async def override_verify_jwt_or_local():
        return {
            "sub": "test-user-123",
            "email": "test@shiftcenter.com",
            "tier": "pro"
        }

    app.dependency_overrides[verify_jwt_or_local] = override_verify_jwt_or_local
    yield
    app.dependency_overrides.clear()
```

### Offline Scenario Testing
To test offline behavior:
1. Use `respx.mock` to intercept CloudAdapter HTTP calls and raise `httpx.ConnectError`
2. Or: stop the cloud server mid-test
3. Or: configure CloudAdapter with unreachable URL

**Recommendation:** Since these are E2E tests, test offline by:
- Starting server in cloud mode
- Making a request with an unreachable cloud_url in the volume config
- Verify the error response

## Constraints
- No file over 500 lines (test file should be ~350-400 lines)
- All file paths absolute (Windows format in task docs)
- No stubs — all tests fully implemented
- No hardcoded colors (not applicable to backend tests)
- Use existing patterns from `tests/hivenode/test_e2e.py` for fixture structure
- Use existing patterns from `tests/hivenode/storage/test_cloud_integration.py` for assertion style

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-208-RESPONSE.md`

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

## Acceptance Criteria (from SPEC-w3-06)
- [ ] POST /storage/write with volume=cloud:// writes to Railway persistent volume (or simulated persistent volume in local cloud mode)
- [ ] POST /storage/read with volume=cloud:// reads the file back
- [ ] POST /storage/list with volume=cloud:// lists the directory
- [ ] POST /storage/delete with volume=cloud:// deletes the file
- [ ] JWT required on all storage routes when HIVENODE_MODE=cloud (verified by test)
- [ ] Offline behavior: if cloud unreachable, write returns {queued: true}, read raises VolumeOfflineError with 503 or 500
- [ ] 12+ integration tests using real HTTP calls
- [ ] All tests pass
- [ ] Test file under 500 lines

## Notes
- The existing `test_cloud_integration.py` has unit tests with mocked HTTP responses (using `respx.mock`). This task writes **integration tests** that start a real server and make real HTTP calls.
- Cloud mode requires `HIVENODE_DATABASE_URL` to be set (per `config.py` validation). Use SQLite with aiosqlite for tests.
- Storage routes use `verify_jwt_or_local()` dependency — local mode bypasses JWT, cloud mode requires it. Use dependency override in tests.
- CloudAdapter raises `VolumeOfflineError` on `httpx.ConnectError`, `httpx.TimeoutException`, or `httpx.NetworkError`.
- Storage routes catch `VolumeOfflineError` and should return appropriate HTTP status (503 or 500).
- If Railway deployment is accessible and you have a real JWT token, you can add an optional test that runs against live Railway (skipped by default, enabled with env var).
