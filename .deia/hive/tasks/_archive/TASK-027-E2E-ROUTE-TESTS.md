# TASK-027: E2E Route Verification Test Suite

**Assigned to:** BEE (Sonnet)
**From:** Q33N
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 3.1)
**Part of:** SPEC-HIVENODE-E2E-001 Wave 1

---

## Objective

Create an end-to-end integration test suite for all 16 existing hivenode routes. This is NOT unit tests with mocks — it's integration tests that start a REAL hivenode server process, make REAL HTTP calls via `httpx.AsyncClient`, write real data to disk, and verify the responses.

The purpose is to verify that all routes work end-to-end with real HTTP, real SQLite, real file I/O, and real process lifecycle.

---

## Requirements

### Test Infrastructure

1. **Server fixture**: Start a real hivenode instance on a random available port
   - Use `uvicorn.Server` in a background thread OR `subprocess` to launch the server
   - Server must start before tests run and shut down cleanly after tests complete
   - Use a random available port (not hardcoded 8420) to avoid conflicts
   - Poll `/health` endpoint until server is ready (max 5 seconds timeout)
   - Use temp directories for all SQLite DBs and volume storage

2. **HTTP client**: Use `httpx.AsyncClient` for all requests
   - Base URL: `http://localhost:<random_port>`
   - Each test is an async function (pytest-asyncio)
   - All tests use real HTTP (no mocks)

3. **Isolation**: Each test must be independent
   - Tests can share the same server instance (fixture scope: module or session)
   - Tests should not interfere with each other (unique file paths, unique event data)
   - Use temp directory for all storage and DBs (pytest `tmp_path` fixture)

### The 16 Routes to Test

From spec Section 3.1:

1. **`GET /health`** → Returns `{"status": "ok", "mode": "local", "version": "0.1.0", "uptime_s": <float>}`
2. **`GET /status`** → Returns `node_id`, `mode`, `uptime`, `volumes`, `event_count`
3. **`POST /auth/verify`** → Rejects invalid JWT with 401. In local mode, bypasses auth.
4. **`GET /auth/whoami`** → Returns user info from token (or local user in local mode)
5. **`GET /ledger/events`** → Returns list of events after writing 3 test events
6. **`GET /ledger/events/{id}`** → Returns specific event by ID
7. **`POST /ledger/query`** → Filters events by `event_type`, `actor`, time range
8. **`GET /ledger/cost`** → Returns cost aggregation after writing events with cost data
9. **`POST /storage/read`** → Reads a file written to `home://`
10. **`POST /storage/write`** → Writes file, verifies on disk
11. **`POST /storage/list`** → Lists directory contents
12. **`POST /storage/stat`** → Returns file metadata (size, modified, content_hash)
13. **`POST /storage/delete`** → Deletes file, verifies gone
14. **`POST /node/announce`** → Registers node, returns ack (cloud mode only — skip in local or mock cloud mode)
15. **`GET /node/discover`** → Returns known nodes (cloud mode only — skip in local or mock cloud mode)
16. **`POST /node/heartbeat`** → Updates last_seen (cloud mode only — skip in local or mock cloud mode)

**Note:** Routes 14–16 are cloud mode only. For this wave, either:
- Skip these tests in local mode (use `pytest.mark.skipif`)
- OR start the server in cloud mode for a separate test module

### Critical Pattern Difference

The existing hivenode tests (in `tests/hivenode/test_*.py`) use `TestClient` with mock transport to avoid SQLite thread-safety issues. The E2E suite is DIFFERENT:

- E2E tests start a REAL server process (separate from test process)
- E2E tests make REAL HTTP calls over localhost
- This avoids SQLite threading issues because the server runs in its own process/thread
- Tests must wait for server to be ready (poll `/health`)

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 3.1)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (app creation, lifespan, route mounting)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py` (health route)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` (auth routes)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\ledger_routes.py` (ledger routes)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (storage routes)
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node.py` (node routes)
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings, mode, ports)
9. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (dependency injection — verify_jwt_or_local)
10. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` (request/response models)
11. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py` (existing test fixtures)

---

## Files to Create

### 1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py`

Full E2E test suite for all 16 routes.

**Structure:**

```python
import pytest
import httpx
import asyncio
import subprocess
import time
import socket
from pathlib import Path
from contextlib import asynccontextmanager
import base64

def find_free_port() -> int:
    """Find a random available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

@pytest.fixture(scope="module")
def e2e_server(tmp_path_factory):
    """
    Start a real hivenode server for E2E tests.

    Runs in a subprocess on a random port.
    Yields (port, base_url, tmp_dir).
    """
    tmp_dir = tmp_path_factory.mktemp("e2e")
    port = find_free_port()

    # Set environment variables for temp paths
    env = {
        "HIVENODE_MODE": "local",
        "HIVENODE_PORT": str(port),
        "HIVENODE_STORAGE_ROOT": str(tmp_dir / "storage"),
        "HIVENODE_LEDGER_DB_PATH": str(tmp_dir / "ledger.db"),
        "HIVENODE_NODE_DB_PATH": str(tmp_dir / "nodes.db"),
        "HIVENODE_DATABASE_URL": f"sqlite+aiosqlite:///[REDACTED].db'}",
    }

    # Start server
    process = subprocess.Popen(
        ["uvicorn", "hivenode.main:app", "--host", "127.0.0.1", "--port", str(port)],
        env={**os.environ, **env},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to be ready
    base_url = f"http://127.0.0.1:{port}"
    max_wait = 5.0
    start = time.time()

    while time.time() - start < max_wait:
        try:
            response = httpx.get(f"{base_url}/health", timeout=1.0)
            if response.status_code == 200:
                break
        except (httpx.ConnectError, httpx.ReadTimeout):
            time.sleep(0.1)
    else:
        process.kill()
        raise RuntimeError("Server failed to start within 5 seconds")

    yield port, base_url, tmp_dir

    # Cleanup
    process.terminate()
    process.wait(timeout=5)

@pytest.fixture
async def client(e2e_server):
    """HTTP client for E2E tests."""
    port, base_url, tmp_dir = e2e_server
    async with httpx.AsyncClient(base_url=base_url, timeout=10.0) as client:
        yield client

# --- Route Tests ---

@pytest.mark.asyncio
async def test_health(client):
    """Test GET /health returns ok status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] == "local"
    assert "uptime_s" in data

@pytest.mark.asyncio
async def test_status(client):
    """Test GET /status returns node info."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "node_id" in data
    assert data["mode"] == "local"
    assert "volumes" in data
    assert "event_count" in data

@pytest.mark.asyncio
async def test_auth_verify_local_mode(client):
    """Test POST /auth/verify bypasses in local mode."""
    # In local mode, auth is bypassed
    response = await client.post("/auth/verify")
    # Local mode should accept or return appropriate response
    assert response.status_code in [200, 401]  # Depends on implementation

@pytest.mark.asyncio
async def test_auth_whoami(client):
    """Test GET /auth/whoami returns local user in local mode."""
    response = await client.get("/auth/whoami")
    assert response.status_code == 200
    data = response.json()
    assert data["sub"] == "local-user"
    assert data["mode"] == "local"

@pytest.mark.asyncio
async def test_ledger_events_empty(client):
    """Test GET /ledger/events returns empty list initially."""
    response = await client.get("/ledger/events")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data

# ... write tests for all 16 routes

@pytest.mark.asyncio
async def test_storage_write_and_read(client, e2e_server):
    """Test POST /storage/write and POST /storage/read."""
    port, base_url, tmp_dir = e2e_server

    # Write a file
    content = b"Hello, E2E test!"
    write_response = await client.post("/storage/write", json={
        "uri": "home://test_e2e.txt",
        "content_base64": base64.b64encode(content).decode(),
    })
    assert write_response.status_code == 200

    # Read it back
    read_response = await client.post("/storage/read", json={
        "uri": "home://test_e2e.txt"
    })
    assert read_response.status_code == 200
    data = read_response.json()
    retrieved = base64.b64decode(data["content_base64"])
    assert retrieved == content

# ... more storage tests (list, stat, delete)

@pytest.mark.asyncio
async def test_ledger_query(client):
    """Test POST /ledger/query filters events."""
    # Write some test events first via direct ledger writer or via another route
    # Then query with filters
    pass

@pytest.mark.asyncio
async def test_ledger_cost(client):
    """Test GET /ledger/cost returns aggregation."""
    # Write events with cost data
    # Query cost endpoint
    pass

# Node routes (cloud mode only - skip or separate fixture)
@pytest.mark.skip(reason="Node routes require cloud mode")
@pytest.mark.asyncio
async def test_node_announce(client):
    """Test POST /node/announce."""
    pass

@pytest.mark.skip(reason="Node routes require cloud mode")
@pytest.mark.asyncio
async def test_node_discover(client):
    """Test GET /node/discover."""
    pass

@pytest.mark.skip(reason="Node routes require cloud mode")
@pytest.mark.asyncio
async def test_node_heartbeat(client):
    """Test POST /node/heartbeat."""
    pass
```

**Key implementation notes:**
- Use `subprocess.Popen` to start server in a separate process
- Use `tmp_path_factory` (module-scoped) for temp directory
- Environment variables override hivenode config for temp paths
- Poll `/health` until server ready (max 5 seconds)
- Use `asyncio` and `pytest.mark.asyncio` for all async tests
- Each storage test uses unique file paths to avoid collisions
- Node route tests are skipped in local mode (or use a separate cloud mode fixture)

---

## Test Requirements

**Target:** 16+ tests (one per route minimum, some routes may have multiple test cases)

**Test breakdown:**
1. `test_health` — GET /health
2. `test_status` — GET /status
3. `test_auth_verify_local_mode` — POST /auth/verify
4. `test_auth_whoami` — GET /auth/whoami
5. `test_ledger_events_empty` — GET /ledger/events (empty)
6. `test_ledger_events_with_data` — GET /ledger/events (after writing events)
7. `test_ledger_event_by_id` — GET /ledger/events/{id}
8. `test_ledger_query` — POST /ledger/query
9. `test_ledger_cost` — GET /ledger/cost
10. `test_storage_write_and_read` — POST /storage/write + POST /storage/read
11. `test_storage_list` — POST /storage/list
12. `test_storage_stat` — POST /storage/stat
13. `test_storage_delete` — POST /storage/delete
14. `test_node_announce` — POST /node/announce (skipped in local mode)
15. `test_node_discover` — GET /node/discover (skipped in local mode)
16. `test_node_heartbeat` — POST /node/heartbeat (skipped in local mode)

**Additional tests (nice to have):**
- `test_storage_write_creates_directories` — Verify parent directories created
- `test_storage_read_nonexistent` — Verify 404 for missing file
- `test_ledger_events_pagination` — Test limit/offset
- `test_storage_list_empty_directory` — Verify empty list for empty dir

---

## Implementation Order (TDD)

1. **Write server fixture first** — `e2e_server` fixture that starts/stops server
2. **Write one simple test** — `test_health` to verify server fixture works
3. **Run test** — Verify server starts, test passes
4. **Write remaining tests** — All 16 route tests
5. **Run all tests** — Verify all pass

---

## Constraints

- No file over 500 lines (test file should be ~400-500 lines with all tests)
- TDD approach: write tests incrementally, verify each works
- No stubs — all tests fully implemented
- All tests must use real HTTP (no mocks)
- Use temp directories for all storage (no hardcoded paths)
- Tests must be independent (order doesn't matter)

---

## Expected Test Count

**Target:** 16–20 tests in `tests/hivenode/test_e2e.py`

---

## Definition of Done

- [ ] `tests/hivenode/test_e2e.py` created with all route tests
- [ ] Server fixture working (starts server, polls health, shuts down)
- [ ] All 16 routes tested with real HTTP calls
- [ ] Storage tests verify files on disk
- [ ] Ledger tests verify events in SQLite
- [ ] Node tests skipped in local mode (or cloud mode fixture created)
- [ ] All tests passing (16+ tests green)
- [ ] No hardcoded ports (use random available port)
- [ ] No hardcoded paths (use tmp_path)
- [ ] No stubs, no TODOs, no skipped tests (except node routes in local mode)

---

**Q33N signature:** TASK-027-READY-FOR-DISPATCH
