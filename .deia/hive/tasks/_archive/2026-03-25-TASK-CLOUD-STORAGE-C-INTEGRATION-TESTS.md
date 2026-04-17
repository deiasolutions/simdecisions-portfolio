# TASK-CLOUD-STORAGE-C: Cloud Storage Integration Tests

## Objective

Create integration tests for full cloud storage workflow: multi-file operations, quota tracking across write/delete, concurrent user isolation, and CloudAdapter → server round-trip.

---

## Context

TASK-A and TASK-B created the store and routes. This task verifies the full stack works end-to-end:

1. Write multiple files → quota accumulates
2. Delete files → quota decrements
3. Multiple users → namespace isolation (no cross-user access)
4. CloudAdapter HTTP client → cloud routes → store → response
5. Error handling: 404 on nonexistent files, 400 on invalid paths

These are integration tests, not unit tests. They test the full HTTP request → route → store → database flow.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\cloud_store.py` — PostgreSQL store (TASK-A)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\cloud_storage_routes.py` — FastAPI routes (TASK-B)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` — CloudAdapter HTTP client
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py` — test fixtures (TestClient, JWT mocks)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` — E2E test pattern reference

---

## Deliverables

- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_storage_integration.py`
- [ ] Integration tests for full workflow scenarios
- [ ] Tests pass: minimum 8 tests
- [ ] No stubs

---

## Test Requirements

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_storage_integration.py`

Minimum 8 tests covering:

### Multi-File Workflows (3 tests)
1. **Write multiple files → list → verify all appear**
   - Write 3 files to `cloud://userA/docs/`
   - List `cloud://userA/docs/`
   - Verify 3 files returned

2. **Write → stat → read → delete → stat (404)**
   - Write `cloud://userA/test.txt`
   - Stat → verify size
   - Read → verify content
   - Delete → verify 200 OK
   - Stat again → verify 404

3. **Quota tracking across write/delete**
   - GET /quota → verify `bytes_used=0`
   - Write 5 MB file → GET /quota → verify `bytes_used=5242880`
   - Write 3 MB file → GET /quota → verify `bytes_used=8388608`
   - Delete 5 MB file → GET /quota → verify `bytes_used=3145728`
   - Delete 3 MB file → GET /quota → verify `bytes_used=0`

### Concurrent User Isolation (2 tests)
4. **Two users write same path → both succeed, isolated**
   - User A writes `cloud://userA/data.txt`
   - User B writes `cloud://userB/data.txt`
   - User A reads `cloud://userA/data.txt` → success
   - User B reads `cloud://userB/data.txt` → success
   - User A reads `cloud://userB/data.txt` → 403
   - User B reads `cloud://userA/data.txt` → 403

5. **User A lists directory → doesn't see User B's files**
   - User A writes `cloud://userA/file1.txt`, `cloud://userA/file2.txt`
   - User B writes `cloud://userB/file3.txt`, `cloud://userB/file4.txt`
   - User A lists `cloud://userA/` → sees only `file1.txt`, `file2.txt`
   - User B lists `cloud://userB/` → sees only `file3.txt`, `file4.txt`

### Error Handling (3 tests)
6. **Read nonexistent file → 404**
   - GET /storage/read?uri=cloud://userA/nonexistent.txt → 404

7. **Delete nonexistent file → 404**
   - DELETE /storage/delete?uri=cloud://userA/nonexistent.txt → 404

8. **Write exceeding quota → 400 with structured error**
   - Write 8 MB file → success
   - Write 5 MB file → 400 with `{"error": "quota_exceeded", "bytes_used": 8388608, "quota_bytes": 10485760}`
   - Verify first file still exists (write was rejected, not partially written)

---

## Implementation Notes

### Test Fixtures

Use `TestClient` from `fastapi.testclient` for HTTP requests. Mock JWT via `conftest.py` pattern.

Example test structure:

```python
import pytest
from fastapi.testclient import TestClient
from hivenode.main import app
from hivenode.storage import cloud_store
from engine.database import Base, engine
import base64

@pytest.fixture(scope="function")
def client():
    """Create test client with fresh database."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)

    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_a_jwt():
    """Mock JWT for user A."""
    return "mock-jwt-userA"  # Mock JWT in conftest.py


@pytest.fixture
def user_b_jwt():
    """Mock JWT for user B."""
    return "mock-jwt-userB"


def test_write_multiple_files_then_list(client, user_a_jwt):
    """Write 3 files, list directory, verify all appear."""
    files = ["file1.txt", "file2.txt", "file3.txt"]

    for filename in files:
        response = client.post(
            "/storage/write",
            json={
                "uri": f"cloud://userA/docs/{filename}",
                "content_base64": base64.b64encode(b"test content").decode()
            },
            headers={"Authorization": f"Bearer {user_a_jwt}"}
        )
        assert response.status_code == 200

    # List directory
    response = client.get(
        "/storage/list",
        params={"uri": "cloud://userA/docs/"},
        headers={"Authorization": f"Bearer {user_a_jwt}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) == 3
    assert set(data["entries"]) == set(files)
```

### JWT Mocking

Update `tests/hivenode/conftest.py` to mock `verify_jwt()` for integration tests:

```python
@pytest.fixture(autouse=True)
def mock_jwt_verification(monkeypatch):
    """Mock JWT verification for all tests."""
    async def mock_verify_jwt(authorization: str = None):
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        # Extract user ID from mock JWT
        token = authorization.split()[-1]
        if token.startswith("mock-jwt-"):
            user_id = token.split("-")[-1]
            return {"sub": user_id}

        raise HTTPException(status_code=401, detail="Invalid token")

    monkeypatch.setattr("hivenode.dependencies.verify_jwt", mock_verify_jwt)
```

---

## Constraints

- **TDD:** Write tests first (but TASK-A and TASK-B are already complete, so tests can run immediately)
- **File size limit:** 500 lines
- **Python 3.13**
- **No stubs:** All tests fully implemented
- **Use TestClient:** HTTP client for FastAPI testing
- **Mock JWT:** Use fixtures for user authentication

---

## Acceptance Criteria

- [ ] `test_cloud_storage_integration.py` created with 8+ tests
- [ ] Multi-file workflow tests (write, list, read, delete, stat)
- [ ] Quota tracking across operations (write increments, delete decrements)
- [ ] Concurrent user isolation (no cross-user access)
- [ ] Error handling (404, 403, 400)
- [ ] All 8+ tests pass
- [ ] No file exceeds 500 lines
- [ ] No stubs

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-CLOUD-STORAGE-C-RESPONSE.md`

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

## Dependencies

- **TASK-CLOUD-STORAGE-A** (store) must complete first
- **TASK-CLOUD-STORAGE-B** (routes) must complete first

---

## Test Command

```bash
cd hivenode && python -m pytest tests/hivenode/test_cloud_storage_integration.py -v
```
