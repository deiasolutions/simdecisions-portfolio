# TASK-BUG-044-A: Add ReliabilityMetadata to RAG models

**Assigned to:** BEE (Haiku)
**Created:** 2026-03-18
**Parent:** BUG-044
**Priority:** P0

---

## Objective

Add missing `ReliabilityMetadata` class to `hivenode/rag/indexer/models.py` to fix ImportError blocking all RAG tests.

---

## Context

RAG module tests are failing with:
```
ImportError: cannot import name 'ReliabilityMetadata' from 'hivenode.rag.indexer.models'
```

The file currently contains `ReliabilityMetrics` class (line 84-90) but tests require a SEPARATE class called `ReliabilityMetadata`. These are two different classes serving different purposes:
- `ReliabilityMetrics` = overall reliability score for an artifact (keep as-is)
- `ReliabilityMetadata` = load/failure tracking metadata (MISSING, needs to be added)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (ADD class here, line ~84)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py` (lines 233-257 show expected API)

---

## Deliverables

- [ ] Add `ReliabilityMetadata` class to `hivenode/rag/indexer/models.py`
- [ ] Class must be a Pydantic BaseModel
- [ ] Class must have all 6 required fields with correct types and defaults (see below)
- [ ] Place class BEFORE `ReliabilityMetrics` class (around line 84)
- [ ] Do NOT modify `ReliabilityMetrics` class
- [ ] Verify RAG tests can be collected (no ImportError)
- [ ] Verify TestReliabilityMetadata tests pass

---

## Required Fields for ReliabilityMetadata

```python
class ReliabilityMetadata(BaseModel):
    """Load/failure tracking metadata for artifact reliability."""

    availability: float = 1.0
    hit_rate: float = 0.0
    last_load_success: Optional[datetime] = None
    last_load_failure: Optional[datetime] = None
    failure_count: int = 0
    consecutive_failures: int = 0
```

**Field descriptions (add to docstring):**
- `availability`: Availability score (0-1), default 1.0
- `hit_rate`: Cache hit rate (0-1), default 0.0
- `last_load_success`: Timestamp of last successful load
- `last_load_failure`: Timestamp of last failed load
- `failure_count`: Total number of load failures
- `consecutive_failures`: Current streak of consecutive failures

---

## Test Requirements

**Run these commands to verify:**

1. **Collection test (no ImportError):**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
   python -m pytest tests/hivenode/rag/ --collect-only
   ```
   Expected: Should collect tests without ImportError

2. **ReliabilityMetadata tests:**
   ```bash
   python -m pytest tests/hivenode/rag/test_models.py::TestReliabilityMetadata -v
   ```
   Expected: All 6 tests in TestReliabilityMetadata class should pass
   - test_reliability_metadata_defaults
   - test_reliability_metadata_custom
   - (and any others in that class)

3. **Full RAG test suite:**
   ```bash
   python -m pytest tests/hivenode/rag/ -v
   ```
   Expected: All tests should be able to run (may have other failures unrelated to this bug)

---

## Constraints

- **No file over 500 lines:** models.py is currently 153 lines, adding ~10 lines keeps it well under limit
- **TDD:** NOT applicable here — tests already exist and are failing due to missing class
- **No stubs:** Class must be fully implemented with all fields and defaults
- **Do NOT rename ReliabilityMetrics:** Keep it as-is, these are two separate classes
- **Placement:** Add ReliabilityMetadata BEFORE ReliabilityMetrics (around line 84)

---

## Acceptance Criteria

- [ ] `ReliabilityMetadata` class exists in `hivenode/rag/indexer/models.py`
- [ ] Class is a Pydantic BaseModel
- [ ] All 6 fields present with correct types: availability (float), hit_rate (float), last_load_success (Optional[datetime]), last_load_failure (Optional[datetime]), failure_count (int), consecutive_failures (int)
- [ ] All fields have correct defaults: 1.0, 0.0, None, None, 0, 0
- [ ] Class has descriptive docstring
- [ ] RAG tests can be collected without ImportError
- [ ] `pytest tests/hivenode/rag/test_models.py::TestReliabilityMetadata -v` shows all tests passing
- [ ] No changes to existing `ReliabilityMetrics` class
- [ ] File remains under 500 lines

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG-044-A-RESPONSE.md`

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

## Notes

- This is a pure addition, not a refactor
- Platform repo has no reference implementation (already checked)
- Two different classes coexist: `ReliabilityMetadata` (new) and `ReliabilityMetrics` (existing)
- Import `datetime` is already at top of file
- `Optional` is already imported from typing
