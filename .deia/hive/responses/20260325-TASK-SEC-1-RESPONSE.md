# TASK-SEC-1: Clean Hardcoded Credentials from config.py -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-25

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (modified)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_config_inventory_url.py` (modified)

## What Was Done
- Replaced `inventory_database_url` fallback logic in `_set_defaults()` method (lines 106-115)
- Removed fallback to `DATABASE_URL` environment variable for inventory database
- Changed "local" keyword behavior from `docs/feature-inventory.db` to `~/.shiftcenter/inventory.db`
- Empty string or no `HIVENODE_INVENTORY_DATABASE_URL` now defaults to local SQLite at `~/.shiftcenter/inventory.db`
- Custom PostgreSQL URLs are preserved as-is when explicitly set via `HIVENODE_INVENTORY_DATABASE_URL`
- Updated 5 existing tests to match new behavior
- Added 1 new test to verify PostgreSQL URLs are preserved
- Verified NO hardcoded Railway constants exist in the module
- Verified NO `postgresql://` strings remain in `hivenode/config.py`
- Verified `database_url` field reads from environment only with no hardcoded production fallback

## Test Results

### Test Files Run
- `tests/hivenode/test_config_inventory_url.py` — 8 tests
- `tests/hivenode/test_config.py` — 8 tests
- All config-related tests in `tests/hivenode/` — 83 tests

### Pass/Fail Counts
- **16 tests passed** (test_config.py + test_config_inventory_url.py)
- **83 tests passed** (all config-related tests)
- **0 tests failed**

### Specific Test Coverage
✅ `test_inventory_url_no_env_uses_local_sqlite` — No env → local SQLite at ~/.shiftcenter/
✅ `test_inventory_url_local_keyword` — "local" keyword → local SQLite at ~/.shiftcenter/
✅ `test_inventory_url_empty_string_uses_local_sqlite` — Empty string → local SQLite
✅ `test_inventory_url_postgres_preserved` — PostgreSQL URL preserved as-is
✅ `test_inventory_url_respects_env_override` — Custom env var respected
✅ `test_inventory_url_sqlite_path_is_absolute` — Absolute path validation
✅ `test_existing_database_url_tests_unaffected` — Existing database_url config unaffected
✅ `test_no_hardcoded_credential_in_module` — No hardcoded Railway constants exist

## Build Verification

### Command
```bash
python -m pytest tests/hivenode/test_config.py tests/hivenode/test_config_inventory_url.py -v --tb=short
```

### Result
```
16 passed, 1 warning in 0.26s
```

### Command (broader verification)
```bash
python -m pytest tests/hivenode/ -k "config" -v
```

### Result
```
83 passed, 1816 deselected, 1 warning in 5.20s
```

### Grep Verification
```bash
grep -r "postgresql://" hivenode/config.py  # No matches found
grep -r "RAILWAY" hivenode/                  # No matches found
```

## Acceptance Criteria

- [x] Remove any hardcoded `RAILWAY_DATABASE_URL` constant if it exists
- [x] Remove any hardcoded `RAILWAY_DATABASE_PUBLIC_URL` constant if it exists
- [x] Replace `inventory_database_url` fallback logic in `_set_defaults()` method with clean env-var logic
- [x] Verify NO `postgresql://` strings remain anywhere in the file (grep verification)
- [x] Verify `database_url` reads from `os.environ.get("DATABASE_URL")` with NO hardcoded production fallback
- [x] Update test assertions in `test_config.py` if they expect old hardcoded URLs
- [x] Tests written FIRST (TDD)
- [x] All existing config tests pass
- [x] New test: config with `HIVENODE_INVENTORY_DATABASE_URL="local"` creates SQLite in ~/.shiftcenter/
- [x] New test: config with `HIVENODE_INVENTORY_DATABASE_URL=<postgres-url>` uses that URL
- [x] Edge case: Empty string for inventory URL falls back to local
- [x] Edge case: Valid postgres URL is preserved as-is
- [x] Edge case: No postgresql:// strings remain in config.py

## Clock / Cost / Carbon

**Clock:** 8 minutes (TDD cycle: tests first, implementation, verification)
**Cost:** ~$0.03 (Sonnet-4.5, 46.6k input tokens, ~2k output tokens)
**Carbon:** ~0.8g CO₂ (estimated for Sonnet inference)

## Issues / Follow-ups

### Edge Cases Handled
- Empty string env var → defaults to local SQLite
- No env var set → defaults to local SQLite
- "local" keyword → local SQLite at ~/.shiftcenter/inventory.db
- Custom PostgreSQL URL → preserved as-is
- Absolute path verification for SQLite URLs on Windows

### Breaking Changes
This is a **breaking change** from previous behavior:
- **Old behavior:** No `HIVENODE_INVENTORY_DATABASE_URL` → fallback to `DATABASE_URL`
- **New behavior:** No `HIVENODE_INVENTORY_DATABASE_URL` → local SQLite at `~/.shiftcenter/inventory.db`
- **Old "local" keyword:** `docs/feature-inventory.db` (project-relative)
- **New "local" keyword:** `~/.shiftcenter/inventory.db` (user home directory)

Users who relied on the `DATABASE_URL` fallback must now explicitly set `HIVENODE_INVENTORY_DATABASE_URL`.

### Dependencies
None — this task is independent and complete.

### Next Tasks
Per TASK-SEC-1 spec, the following are separate tasks:
- TASK-SEC-2: Verify `.env` and `.gitignore` (separate task)
- TASK-SEC-3: Add rate limiting to auth endpoints (separate task)

### Notes
- The config module now has **zero hardcoded credentials**
- All Railway URLs removed
- All tests pass, including 83 config-related integration tests
- Code is clean, no stubs, no TODOs
- File under 500 lines (currently 197 lines)
