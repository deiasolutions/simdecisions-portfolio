# YOUR ROLE
BEE — You write code and fix tests. You do not orchestrate.

# TASK-019A: Fix Hivenode FastAPI Test Suite (36 failures)

**Priority:** HIGH — blocks deployment verification
**Estimated complexity:** Medium (test fixture plumbing, no new features)
**Parent:** TASK-019 (Hivenode FastAPI Server)

## Problem Statement

TASK-019 delivered 55 tests across 7 files. 36 fail, 19 pass. All failures stem from **three root causes**, not 36 separate bugs.

## Root Cause Analysis

### Root Cause 1: Global `settings` at import time (affects ALL test files)

`hivenode/config.py:95` creates a module-level singleton:
```python
settings = HivenodeConfig()  # evaluated ONCE at import
```

Every test that does `monkeypatch.setenv("HIVENODE_RA96IT_PUBLIC_KEY", ...)` patches the env AFTER `settings` is already created. The settings object never sees the patched values. This breaks:
- All auth-dependent tests (auth, ledger, storage, node routes)
- Config tests that expect fresh instances but get the cached global

### Root Cause 2: No `app.dependency_overrides` for `verify_jwt` (affects 30+ tests)

All route tests create `AsyncClient(transport=ASGITransport(app=app))` but never override `verify_jwt`. The dependency reads from the import-time `settings`, finds no public key, and returns 401 for every authenticated request.

Routes affected:
- `POST /node/announce`, `GET /node/discover`, `POST /node/heartbeat` — 7 tests
- `GET /ledger/events`, `GET /ledger/events/{id}`, `GET /ledger/query`, `GET /ledger/cost` — 10 tests
- `POST /storage/write`, `GET /storage/read`, `GET /storage/list`, `GET /storage/stat`, `DELETE /storage/delete` — 9 tests
- `GET /auth/verify`, `GET /auth/whoami` — 4 tests

### Root Cause 3: `NODE_ID_FILE` computed at import time (affects 2 tests)

`hivenode/node_identity.py:6`:
```python
NODE_ID_FILE = Path.home() / ".shiftcenter" / "node_id"
```

Tests monkeypatch HOME/USERPROFILE but `NODE_ID_FILE` is already resolved. The tests write to the real home directory instead of `tmp_path`.

## Fix Strategy

### Fix A: Create `tests/hivenode/conftest.py` with shared fixtures

Create a `conftest.py` that provides:

1. **`mock_settings` fixture** — Creates a fresh `HivenodeConfig` per test with temp paths, patches `hivenode.config.settings` and `hivenode.dependencies.settings`:
   ```python
   @pytest.fixture
   def mock_settings(tmp_path, monkeypatch):
       config = HivenodeConfig(
           mode="local",
           database_url=f"sqlite+aiosqlite:///[REDACTED].db'}",
           storage_root=str(tmp_path / "storage"),
           ledger_db_path=str(tmp_path / "ledger.db"),
           node_db_path=str(tmp_path / "nodes.db"),
           ra96it_public_key=TEST_PUBLIC_KEY,
       )
       monkeypatch.setattr("hivenode.config.settings", config)
       monkeypatch.setattr("hivenode.dependencies.settings", config)
       return config
   ```

2. **`mock_verify_jwt` fixture** — Overrides `verify_jwt` dependency so authenticated routes accept test tokens without needing a real public key:
   ```python
   @pytest.fixture
   def mock_verify_jwt():
       async def _override():
           return {"sub": "test-user", "email": "test@example.com", "tier": "free"}
       app.dependency_overrides[verify_jwt] = _override
       yield
       app.dependency_overrides.pop(verify_jwt, None)
   ```

3. **`test_client` fixture** — Wraps `AsyncClient` with dependency overrides applied.

4. **`cloud_mode_settings` fixture** — Like `mock_settings` but with `mode="cloud"` and a temp node store, for node route tests.

### Fix B: Fix `node_identity.py` — make path injectable

Change `get_or_create_node_id()` to accept an optional `base_dir: Path = None` parameter. When `None`, use `Path.home() / ".shiftcenter"`. This lets tests pass `tmp_path`.

Remove the module-level `NODE_ID_FILE` constant or keep it as a default only.

### Fix C: Fix config test assertions

- `test_invalid_mode_raises_error`: Pydantic `Literal["local", "remote", "cloud"]` raises `ValidationError`, NOT `ValueError`. Change to `pytest.raises(ValidationError)` or `pytest.raises((ValueError, ValidationError))`.
- `test_cloud_mode_requires_database_url`: May need to construct with keyword args to bypass Pydantic env loading: `HivenodeConfig(mode="cloud")`.

### Fix D: Fix health/status test dependency initialization

- `test_status_returns_extended_info` and `test_status_includes_node_id` need `get_ledger_reader` and `get_volume_registry` to be initialized. Override these dependencies with test instances:
  ```python
  app.dependency_overrides[get_ledger_reader] = lambda: mock_reader
  app.dependency_overrides[get_volume_registry] = lambda: mock_registry
  ```

### Fix E: Fix ledger, storage, and node route tests

- All 10 ledger tests: Use `mock_verify_jwt` + override `get_ledger_reader` with a test reader pointing at the temp DB
- All 9 storage tests: Use `mock_verify_jwt` + override `get_transport` and `get_volume_registry` with test instances
- All 7 node tests: Use `cloud_mode_settings` + `mock_verify_jwt` + override `get_node_store` with test NodeStore

### Fix F: Delete junk files

Delete these two files created by TASK-019 bee's failed fix attempts:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\fix_tests.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\fix_all_issues.py`

Also delete the `_tools/` directory if empty after deletion.

## Files to Create

| # | File | Description |
|---|------|-------------|
| 1 | `tests/hivenode/conftest.py` | Shared fixtures: mock_settings, mock_verify_jwt, test_client, cloud_mode_settings |

## Files to Modify

| # | File | What Changes |
|---|------|-------------|
| 2 | `hivenode/node_identity.py` | Make path injectable (optional `base_dir` param) |
| 3 | `tests/hivenode/test_config.py` | Fix exception types (ValidationError vs ValueError) |
| 4 | `tests/hivenode/test_health.py` | Add dependency overrides for status tests |
| 5 | `tests/hivenode/test_auth_routes.py` | Use conftest fixtures instead of manual monkeypatch |
| 6 | `tests/hivenode/test_ledger_routes.py` | Use conftest fixtures, override ledger reader |
| 7 | `tests/hivenode/test_storage_routes.py` | Use conftest fixtures, override transport/registry |
| 8 | `tests/hivenode/test_node_routes.py` | Use cloud_mode_settings fixture, override node store |
| 9 | `tests/hivenode/test_node_identity.py` | Pass base_dir to get_or_create_node_id |

## Files to Delete

| # | File | Reason |
|---|------|--------|
| 10 | `_tools/fix_tests.py` | Junk from TASK-019 bee's failed attempts |
| 11 | `_tools/fix_all_issues.py` | Junk from TASK-019 bee's failed attempts |

## Test Execution

Run after all fixes:
```bash
python -m pytest tests/hivenode/ -v
```

**Target: 55/55 passing (0 failures)**

## Acceptance Criteria

- [ ] `conftest.py` provides reusable fixtures for all test files
- [ ] `node_identity.py` accepts optional `base_dir` parameter
- [ ] Config tests catch correct exception types
- [ ] All 55 tests pass: `python -m pytest tests/hivenode/ -v`
- [ ] No test writes to the real `~/.shiftcenter/` directory
- [ ] `_tools/fix_tests.py` deleted
- [ ] `_tools/fix_all_issues.py` deleted
- [ ] `_tools/` directory deleted if empty
- [ ] Commit: `[BEE-HAIKU] TASK-019A: fix hivenode test fixtures and dependency overrides`

## Important Notes

- Do NOT modify route handlers or source logic — only test files and `node_identity.py`
- Do NOT add new tests — fix the existing 55
- Do NOT change `config.py` module-level `settings` pattern — that's intentional for production. Tests must work around it.
- The `app.dependency_overrides` dict MUST be cleaned up after each test (use yield fixtures)
- All temp files must use `tmp_path` — no test should touch the user's real filesystem
