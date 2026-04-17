# TASK-003A: Fix Named Volume Storage Test Failures -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-10

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\conftest.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_transport.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_provenance.py`

## What Was Done

### Issue 1: Windows PermissionError on temp dir cleanup (24 errors)
- Modified `mock_ledger_writer` fixture in `conftest.py` to use `yield` pattern and explicitly close the SQLite connection
- Added explicit `close()` calls to all 13 transport test functions to close `FileTransport`, `LedgerWriter`, and `LedgerReader` instances before temp directory cleanup
- Added explicit `close()` calls to all 11 provenance test functions to close `ProvenanceStore` instances before temp directory cleanup

### Issue 2: Registry allows system volume names to be declared (1 failure)
- Fixed `declare_volume` method in `hivenode/storage/registry.py` to reject ALL system volume names upfront, regardless of whether they are already loaded in `self._volumes`
- Changed validation order: check system volume names first, then validate length for user-defined volumes
- This ensures `ValueError` is raised when attempting to declare "work", "home", "local", or "cloud" volumes

### Issue 3: Possible test API mismatch (1 failure)
- Verified that all tests already use correct `reader.query()` API (not `get_events()`)
- No changes needed for this issue (it was already fixed)

## Test Results

### Storage Tests
```
============================= 84 passed in 0.87s ==============================
```

All storage tests pass:
- 37 local adapter tests
- 12 provenance tests
- 13 transport tests
- 10 registry tests
- 9 cloud adapter tests
- 3 other tests (config, resolver)

### Ledger Tests (No Regressions)
```
============================= 46 passed in 1.39s ==============================
```

All ledger tests still pass:
- 8 aggregation tests
- 9 export tests
- 12 reader tests
- 7 schema tests
- 10 writer tests

## Build Verification

Not applicable (no build step required for Python library).

## Acceptance Criteria

- [x] All storage tests pass (84/84)
- [x] No regressions in ledger tests (46/46)
- [x] Fixed Windows PermissionError on temp directory cleanup
- [x] Fixed system volume name validation logic
- [x] All SQLite connections properly closed in tests

## Clock/Cost/Carbon

- **Model:** Sonnet 4.5
- **Time:** ~5 minutes
- **Cost:** Estimated $0.02 (based on typical Sonnet 4.5 token usage)
- **Carbon:** Negligible

## Issues/Follow-ups

None. All test failures resolved. The storage system is now fully functional on Windows with proper resource cleanup.
