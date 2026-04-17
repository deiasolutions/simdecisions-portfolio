# TASK-242-B: Create Backend API Smoke Tests for Production

## Objective
Create `tests/smoke/test_production_api.py` with 3 smoke tests to verify production API health and protected endpoint rejection against live deployed URL.

## Context

Wave 5 Ship (WAVE-5-SHIP.md) requires comprehensive smoke tests against production. Playwright tests cover frontend; backend tests must verify:
1. Health endpoint returns 200
2. Protected endpoints reject unauthenticated requests (401/403)

**Existing E2E test patterns from `tests/hivenode/test_e2e.py`:**
- Use `httpx.AsyncClient` for HTTP calls
- Tests are async (`@pytest.mark.asyncio`)
- Production URL configurable via env var
- Graceful failure if production unreachable (use pytest.skip)
- Fast execution (no retries, no long waits)

**Protected endpoints to test:**
- `/api/shell/exec` — uses `verify_jwt_or_local` (requires auth in cloud mode)
- `/efemera/channels` — no auth check currently, but may be added later

**Key differences from E2E tests:**
- E2E starts a subprocess server (local mode)
- Smoke tests hit deployed production URL (cloud mode)
- Smoke tests must skip gracefully if URL unreachable

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` — E2E test patterns (httpx usage, async tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\shell.py` — Shell execute endpoint (protected)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` — Auth verification routes

## Deliverables

Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\test_production_api.py`:

```python
"""Smoke tests for production API endpoints.

Run against deployed production URL (configurable via DEPLOY_URL env var).
Tests verify health endpoint and protected route rejection.

Usage:
    pytest tests/smoke/test_production_api.py -v
    DEPLOY_URL=https://shiftcenter.com pytest tests/smoke/test_production_api.py -v
"""
import pytest
import httpx
import os

# Production URL (default to dev.shiftcenter.com)
DEPLOY_URL = os.environ.get("DEPLOY_URL", "https://dev.shiftcenter.com")


@pytest.fixture
async def client():
    """HTTP client for production smoke tests."""
    async with httpx.AsyncClient(base_url=DEPLOY_URL, timeout=10.0) as client:
        yield client


@pytest.mark.asyncio
async def test_health_endpoint_returns_200():
    """Test GET /health returns 200 and healthy status."""
    try:
        async with httpx.AsyncClient(base_url=DEPLOY_URL, timeout=5.0) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] in ["ok", "healthy"]
    except (httpx.ConnectError, httpx.ReadTimeout) as e:
        pytest.skip(f"Production URL unreachable: {DEPLOY_URL} - {e}")


@pytest.mark.asyncio
async def test_shell_exec_rejects_without_auth(client):
    """Test POST /api/shell/exec rejects unauthenticated requests."""
    try:
        response = await client.post("/api/shell/exec", json={
            "command": "echo",
            "args": ["test"]
        })
        # In cloud mode, should return 401 (unauthorized) or 403 (forbidden)
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403, got {response.status_code}"
    except (httpx.ConnectError, httpx.ReadTimeout) as e:
        pytest.skip(f"Production URL unreachable: {DEPLOY_URL} - {e}")


@pytest.mark.asyncio
async def test_efemera_channels_rejects_without_auth(client):
    """Test GET /efemera/channels rejects unauthenticated requests.

    NOTE: Efemera routes currently have no auth checks. If auth is added later,
    this test will verify it. If not, this may return 200 (expected behavior).
    """
    try:
        response = await client.get("/efemera/channels")

        # Current behavior: no auth check, returns 200
        # Future behavior: auth check added, returns 401/403
        # Accept both for now
        if response.status_code == 200:
            # No auth check yet - log but don't fail
            print("INFO: /efemera/channels returned 200 (no auth check)")
        else:
            # Auth check exists - verify rejection
            assert response.status_code in [401, 403], \
                f"Expected 401, 403, or 200, got {response.status_code}"
    except (httpx.ConnectError, httpx.ReadTimeout) as e:
        pytest.skip(f"Production URL unreachable: {DEPLOY_URL} - {e}")
```

## Test Requirements

- [ ] Tests written first (TDD) — N/A, testing existing production deployment
- [ ] `tests/smoke/test_production_api.py` created with 3 tests
- [ ] Test 1: `/health` returns 200 with "ok" or "healthy" status
- [ ] Test 2: `/api/shell/exec` rejects without auth (401 or 403)
- [ ] Test 3: `/efemera/channels` behavior verified (200 if no auth, 401/403 if auth added)
- [ ] All tests use `pytest.skip()` if production URL unreachable
- [ ] All tests use `httpx.AsyncClient` with 5-10s timeout
- [ ] Run tests: `pytest tests/smoke/test_production_api.py -v`
- [ ] All tests pass or skip gracefully
- [ ] File stays under 150 lines

## Edge Cases

- Production URL unreachable → pytest.skip with reason
- Health endpoint may return "ok" or "healthy" (accept both)
- Shell exec may return 401 or 403 depending on implementation (accept both)
- Efemera routes may have no auth yet → test logs INFO but passes on 200
- Network timeout → pytest.skip with reason

## Constraints

- Rule 4: File must stay under 500 lines (target: < 150 lines)
- Rule 5: TDD (tests are testing existing prod deployment, so N/A)
- Rule 6: No stubs (all tests fully implemented)
- Use `os.environ.get("DEPLOY_URL", "https://dev.shiftcenter.com")` for URL
- Use `httpx.AsyncClient` with timeout=5-10s (no retries)
- Tests must be FAST (< 5 seconds total runtime)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-242-B-RESPONSE.md`

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

## Run Commands

```bash
# Run smoke tests against dev.shiftcenter.com
pytest tests/smoke/test_production_api.py -v

# Run against custom URL
DEPLOY_URL=https://shiftcenter.com pytest tests/smoke/test_production_api.py -v

# Run all smoke tests (Playwright + backend)
cd browser && npx playwright test --config=playwright.deploy.config.ts
cd .. && pytest tests/smoke/test_production_api.py -v
```

## Dependencies

- `httpx` package must be installed (already in requirements)
- `pytest` and `pytest-asyncio` must be installed (already in dev deps)
- Production URL must be deployed and accessible
- TASK-241 (Production URLs verified) should be complete first
