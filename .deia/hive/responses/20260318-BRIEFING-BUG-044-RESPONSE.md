# BRIEFING-BUG-044: Add missing ReliabilityMetadata class -- TASK FILE READY

**Status:** TASK FILE READY FOR REVIEW
**Role:** Q33N (Coordinator)
**Date:** 2026-03-18

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-044-A-add-reliability-metadata.md`

**Task breakdown:**
- **TASK-BUG-044-A:** Add ReliabilityMetadata to RAG models (Haiku, 15-30 min)

---

## What the Task Does

Adds the missing `ReliabilityMetadata` class to `hivenode/rag/indexer/models.py` to fix ImportError blocking all RAG tests.

**Key points:**
- Adds new Pydantic BaseModel class with 6 fields (availability, hit_rate, last_load_success, last_load_failure, failure_count, consecutive_failures)
- Does NOT modify existing `ReliabilityMetrics` class (these are two separate classes)
- Pure addition, not a refactor
- Tests already exist and are failing due to missing class (not TDD, just fix)

---

## Files Affected

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (add ReliabilityMetadata class around line 84)

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py::TestReliabilityMetadata` (6 tests should pass)

---

## Acceptance Criteria (Task Level)

- [ ] `ReliabilityMetadata` class exists with all 6 fields
- [ ] All fields have correct types and defaults
- [ ] RAG tests can be collected (no ImportError)
- [ ] `TestReliabilityMetadata` tests pass (6 tests)
- [ ] No changes to existing `ReliabilityMetrics` class
- [ ] File remains under 500 lines

---

## Model Assignment

**Haiku** — This is a simple model addition (add one class with 6 fields and defaults). No complex logic, no architecture decisions. Estimated 15-30 minutes.

---

## Constraints Applied

- TDD not applicable (tests already exist)
- No stubs (class must be fully implemented)
- File size OK (currently 153 lines, adding ~10 lines)
- No hardcoded colors (not applicable)
- All file paths absolute

---

## Ready for Review

Q33NR: Please review the task file. If approved, I will dispatch the bee.

**Dispatch command (when approved):**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG-044-A-add-reliability-metadata.md --model haiku --role bee --inject-boot
```

---

## Notes

- This is P0 priority (blocks all RAG tests)
- Root cause: class name mismatch (ReliabilityMetadata missing, ReliabilityMetrics exists)
- Platform repo has no reference implementation
- Two classes serve different purposes and must coexist
