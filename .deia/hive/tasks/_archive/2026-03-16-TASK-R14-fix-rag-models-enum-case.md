# TASK-R14: Fix RAG models enum case mismatch

## Objective
Change enum string values in `hivenode/rag/indexer/models.py` from uppercase to lowercase to match the API contract and existing tests.

## Context
R13 verification found 43 test failures in `tests/hivenode/rag/test_models.py`. All enums use uppercase values (`"CODE"`, `"PHASE_IR"`, etc.) but the tests and API contract expect lowercase (`"code"`, `"phase_ir"`).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R13-RESPONSE.md`

## Deliverables
- [ ] Change all enum string values to lowercase in models.py:
  - `ArtifactType`: CODE="code", PHASE_IR="phase_ir", DOCUMENT="document", CONFIG="config", TEST="test"
  - `StorageTier`: EDGE="edge", WARM="warm", COLD="cold", ARCHIVE="archive"
  - `IRStatus`: UNTESTED="untested", VERIFIED="verified", FAILED="failed", STALE="stale"
  - Any other enums with uppercase string values
- [ ] Do NOT modify tests — tests define the contract
- [ ] Run: `python -m pytest tests/hivenode/rag/test_models.py -v`
- [ ] All 50 tests must pass (43 currently failing + 7 already passing)

## Constraints
- Only modify `models.py` enum values — nothing else
- Do NOT change enum member NAMES (keep `CODE`, `PHASE_IR` etc.), only the string VALUES

## Acceptance Criteria
- [ ] All enum string values are lowercase in models.py
- [ ] All 50 tests in test_models.py pass
- [ ] No regressions in other RAG tests

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R14-RESPONSE.md`
All 8 sections required.
