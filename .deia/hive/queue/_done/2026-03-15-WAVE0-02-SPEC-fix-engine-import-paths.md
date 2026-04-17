# WAVE0-02: Fix Engine Import Paths

## Priority
P0.005

## Model Assignment
haiku

## Objective
Fix import path error in `tests/engine/des/test_des_ledger_emission.py` which is trying to import from old platform path `src.simdecisions.runtime.ledger` instead of the correct shiftcenter path `engine`.

## Acceptance Criteria
- [ ] `test_des_ledger_emission.py` imports from correct paths (engine module, not src.simdecisions)
- [ ] All engine tests collect without import errors
- [ ] All engine tests pass (or existing failures are documented)

## Constraints
- TDD: Run tests before and after fix
- No stubs
- Max 500 lines per file
- Only fix import paths — do not refactor other code

## Smoke Test
- [ ] `python -m pytest tests/engine/ -v` runs without import errors
- [ ] No new test failures introduced
