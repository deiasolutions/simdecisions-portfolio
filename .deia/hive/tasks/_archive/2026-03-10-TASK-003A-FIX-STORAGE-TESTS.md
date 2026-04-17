# TASK-003A: Fix Named Volume Storage Test Failures (2 failures, 24 errors)

## Objective

Fix the 26 test issues in `tests/hivenode/storage/`. The storage code is structurally solid (82 tests passing). The issues are: 1 registry logic bug, 1 possible test API mismatch, and 24 Windows PermissionError on temp dir cleanup.

## Dependencies

- TASK-003 must be complete (it is).

## Root Cause Analysis — 3 Issues

### Issue 1: Windows PermissionError on temp dir cleanup (24 errors)

**File:** `tests/hivenode/storage/conftest.py`

SQLite connections (LedgerWriter, ProvenanceStore) opened during tests are not closed before `TemporaryDirectory` cleanup. Windows locks open database files, so `PermissionError: [WinError 32]` occurs when the temp dir tries to delete them.

**Affected tests:** All provenance and transport tests (24 total).

**Fix:** Two changes needed:

1. Change the `mock_ledger_writer` fixture to `yield` and close the connection:
```python
@pytest.fixture
def mock_ledger_writer(temp_ledger_db):
    """Create a ledger writer for transport tests."""
    from hivenode.ledger.writer import LedgerWriter
    writer = LedgerWriter(temp_ledger_db)
    yield writer
    writer.close()
```

2. In every test function that creates a `ProvenanceStore`, `FileTransport`, or `LedgerWriter` directly, close them before the test ends. The cleanest approach: change test functions to use context managers or add explicit `close()` calls. Example:

```python
def test_something(temp_volumes_yaml, temp_ledger_db, temp_provenance_db):
    from hivenode.storage.transport import FileTransport
    from hivenode.storage.registry import VolumeRegistry
    from hivenode.ledger.writer import LedgerWriter

    registry = VolumeRegistry(temp_volumes_yaml)
    ledger = LedgerWriter(temp_ledger_db)
    transport = FileTransport(registry, ledger, temp_provenance_db)

    # ... test operations ...

    # Close connections before temp dir cleanup
    transport.close()
    ledger.close()
```

Apply this pattern to ALL provenance and transport tests. Also close any `LedgerReader` instances created in tests.

### Issue 2: Registry allows system volume names to be declared (1 failure)

**File:** `hivenode/storage/registry.py`, method `declare_volume`

**Test:** `test_reject_short_custom_volume_name`

Current logic on lines 60-67:
```python
if len(name) <= 7:
    if name not in SYSTEM_VOLUMES:
        raise ValueError("User-defined volume names must be >=8 characters")
    if name in self._volumes:
        raise ValueError("Cannot redeclare system volume")
```

Problem: If `name` is "work" (in SYSTEM_VOLUMES) but NOT yet in `self._volumes` (not loaded from YAML), no error is raised. The test sends "work" and expects `ValueError`.

**Fix:** System volume names should ALWAYS be rejected from `declare_volume`, whether loaded or not:
```python
if name in SYSTEM_VOLUMES:
    raise ValueError(f"Cannot redeclare system volume: {name}")
if len(name) <= 7:
    raise ValueError(
        f"User-defined volume names must be >=8 characters, got: {name}"
    )
```

### Issue 3: Possible test API mismatch (1 failure — may be resolved)

**File:** `tests/hivenode/storage/test_transport.py` (test_transport_delete_emits_ledger_event)

An earlier test run showed `reader.get_events()` but `LedgerReader` has no such method (correct method is `reader.query()`). The current file may already have the fix. Verify when running tests — if it still uses `get_events()`, change to `reader.query()`.

## What to Do

1. Fix all 3 issues above
2. Run `python -m pytest tests/hivenode/storage/ -v` and verify all tests pass (should be ~82+ tests)
3. Also run `python -m pytest tests/hivenode/ledger/ -v` to verify no regressions

## Constraints

- Do NOT restructure or refactor any code beyond the specific fixes
- Do NOT add new tests
- Do NOT change any passing test behavior
- Keep all files under 500 lines
- Ensure ALL SQLite connections are properly closed in tests

## Files to Modify

- `tests/hivenode/storage/conftest.py` — fix mock_ledger_writer to yield + close
- `hivenode/storage/registry.py` — fix declare_volume namespace logic
- `tests/hivenode/storage/test_transport.py` — add close() calls to all tests
- `tests/hivenode/storage/test_provenance.py` — add close() calls to all tests
- `tests/hivenode/storage/test_transport.py` — fix get_events() if still present

## Deliverables

- [ ] All storage tests pass (82+)
- [ ] No regressions in ledger tests (46)

## Response Requirements -- MANDATORY

Write response to: `.deia/hive/responses/YYYYMMDD-TASK-003A-RESPONSE.md`

Sections: Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups.
