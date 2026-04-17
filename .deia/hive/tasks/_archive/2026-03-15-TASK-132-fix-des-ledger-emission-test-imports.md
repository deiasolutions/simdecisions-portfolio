# TASK-132: Fix DES Ledger Emission Test Import Paths

## Objective
Fix import path errors in `test_des_ledger_emission.py` which is importing from the old platform path `src.simdecisions.runtime.ledger` instead of the correct shiftcenter paths. The test file needs to be updated to use the current ledger implementation or removed if it's obsolete.

## Context
This is part of WAVE0 cleanup — fixing residual import paths from the platform port. The engine module was ported from `platform/efemera/src/efemera/` to `engine/` in shiftcenter, but the test file `test_des_ledger_emission.py` still references the old platform path `src.simdecisions.runtime.ledger`.

**Current Issue:**
- Line 22 imports: `from src.simdecisions.runtime.ledger import EventLedger`
- The `EventLedger` class does not exist in shiftcenter
- The current ledger implementation uses `LedgerWriter` and `LedgerReader` from `hivenode.ledger`

**Investigation Findings:**
- Other engine test files (e.g., `test_ledger_adapter.py`) successfully import from `engine.des.*` and `hivenode.ledger.*`
- Current ledger API: `hivenode.ledger.writer.LedgerWriter` and `hivenode.ledger.reader.LedgerReader`
- The DES engine has a `ledger_adapter.py` that bridges DES events to the ShiftCenter ledger

**Decision Required:**
You must determine whether to:
1. Update the test to use the current `LedgerWriter`/`LedgerReader` API
2. Remove the test if it's testing functionality that no longer exists or is covered elsewhere
3. Update the test to use the `LedgerAdapter` from `engine.des.ledger_adapter`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\des\test_des_ledger_emission.py` (file to fix)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\des\test_ledger_adapter.py` (example of correct imports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\ledger_adapter.py` (current ledger integration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` (current ledger API)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\engine.py` (to understand if ledger emission is built-in)

## Deliverables
- [ ] Run tests BEFORE fix to document current error state
- [ ] Either:
  - [ ] Update `test_des_ledger_emission.py` to use current ledger API (LedgerWriter/LedgerReader or LedgerAdapter)
  - [ ] OR: Delete `test_des_ledger_emission.py` if functionality is covered by `test_ledger_adapter.py`
- [ ] All engine tests collect without import errors
- [ ] All engine tests pass (or existing failures are documented as pre-existing)
- [ ] Document decision in response file

## Test Requirements
- [ ] Run `python -m pytest tests/engine/des/test_des_ledger_emission.py -v` BEFORE changes (document error)
- [ ] Run `python -m pytest tests/engine/des/ -v` AFTER changes (all tests collect)
- [ ] Run `python -m pytest tests/engine/ -v` AFTER changes (no regressions)
- [ ] If test is updated (not deleted): verify test logic is correct for current API
- [ ] If test is deleted: document why and confirm coverage exists elsewhere

## Constraints
- **TDD:** Run tests before and after fix
- **No stubs:** If updating the test, fully implement it with current API
- **Max 500 lines per file:** (not applicable - this is a simple fix)
- **Only fix import paths and update to current API** — do not refactor unrelated code

## Acceptance Criteria from Spec
- [ ] `test_des_ledger_emission.py` imports from correct paths (engine module, not src.simdecisions) OR is deleted with justification
- [ ] All engine tests collect without import errors
- [ ] All engine tests pass (or existing failures are documented as pre-existing, not caused by this change)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-132-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (e.g., "deleted test_des_ledger_emission.py" OR "updated imports on lines 22, 20, 21")
4. **Test Results** — test files run, pass/fail counts BEFORE and AFTER
5. **Build Verification** — test output summary showing all tests collect
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — document decision rationale (update vs delete), any edge cases

DO NOT skip any section.
