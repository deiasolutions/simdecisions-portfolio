# BRIEFING: BUG-044 — Add missing ReliabilityMetadata class to RAG module

**To:** Q33N (Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18
**Spec:** SPEC-TASK-BUG044-rag-reliability-metadata-missing
**Priority:** P0
**Model:** sonnet

---

## Objective

Fix RAG module collection error by adding missing `ReliabilityMetadata` class to `hivenode/rag/indexer/models.py`.

---

## Problem

RAG module tests cannot run due to import error:

```
ImportError: cannot import name 'ReliabilityMetadata' from 'hivenode.rag.indexer.models'
```

**Impact:** All RAG tests blocked. Cannot run any tests in `tests/hivenode/rag/`.

---

## Root Cause Analysis

The file `hivenode/rag/indexer/models.py` contains a class called `ReliabilityMetrics` (line 84-90), but tests are trying to import `ReliabilityMetadata` (different name).

**Current state:**
- `ReliabilityMetrics` exists with fields: `reliability_score`, `availability`, `latency_ms`, `last_updated`
- `ReliabilityMetadata` is MISSING

**What tests expect (from `tests/hivenode/rag/test_models.py` lines 233-257):**

`ReliabilityMetadata` class with these fields:
- `availability` (float, default 1.0)
- `hit_rate` (float, default 0.0)
- `last_load_success` (Optional[datetime], default None)
- `last_load_failure` (Optional[datetime], default None)
- `failure_count` (int, default 0)
- `consecutive_failures` (int, default 0)

**Note:** These are TWO DIFFERENT classes serving different purposes:
- `ReliabilityMetrics` = overall reliability score for an artifact
- `ReliabilityMetadata` = load/failure tracking metadata

---

## Task Requirements

Create ONE task file for a BEE to:

1. **Add `ReliabilityMetadata` class** to `hivenode/rag/indexer/models.py`
   - Must be a Pydantic BaseModel
   - Must have all 6 fields listed above with correct types and defaults
   - Place it BEFORE `ReliabilityMetrics` class (around line 84)

2. **Verify tests can collect**
   - Run: `python -m pytest tests/hivenode/rag/ --collect-only`
   - Should not see ImportError

3. **Verify ReliabilityMetadata tests pass**
   - Run: `python -m pytest tests/hivenode/rag/test_models.py::TestReliabilityMetadata -v`
   - All tests in that class should pass

4. **Verify all RAG tests can run**
   - Run: `python -m pytest tests/hivenode/rag/ -v`
   - May have other failures, but NO collection errors

---

## Files to Work With

**Primary file:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (ADD class here)

**Test files (read to understand requirements):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py` (lines 233-257 show expected API)

**Reference:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-FULL-TEST-SWEEP-REPORT.md` (full context)

---

## Success Criteria

- [ ] `ReliabilityMetadata` class exists in `hivenode/rag/indexer/models.py`
- [ ] Class has all 6 required fields with correct types and defaults
- [ ] RAG tests can be collected (no ImportError)
- [ ] `TestReliabilityMetadata` tests pass (6 tests in test_models.py)
- [ ] All RAG module tests can run (may have other failures unrelated to this bug)

---

## Constraints

- **TDD:** Not applicable here — tests already exist and are failing due to missing class
- **No stubs:** Class must be fully implemented (all fields with defaults)
- **File size:** models.py is 153 lines, well under 500-line limit
- **Model:** Assign to **Haiku** (simple model addition)

---

## Expected Deliverable

One task file:
- `TASK-BUG-044-A: Add ReliabilityMetadata to RAG models`

The task should be bee-sized (15-30 minutes) and have clear acceptance criteria matching the success criteria above.

---

## Notes

- Do NOT modify `ReliabilityMetrics` class — keep it as-is
- Do NOT rename `ReliabilityMetrics` to `ReliabilityMetadata` — they are separate classes
- Platform repo has no reference implementation (checked `platform/efemera/src/efemera/rag/indexer/`)
- This is a pure addition, not a refactor

---

**Q33N: Please write the task file and return it for review. Do NOT dispatch the bee yet.**
