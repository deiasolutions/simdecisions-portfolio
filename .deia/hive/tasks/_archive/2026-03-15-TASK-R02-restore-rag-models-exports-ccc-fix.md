# TASK-R02: Restore RAG models exports + CCC_PER_FILE fix

**Priority:** P0.10
**Model:** Haiku
**Original:** TASK-151 (RAG models port)

---

## Objective

Restore two lost modifications from TASK-151:
1. Fix the `CCC_PER_FILE` constant in `indexer_service.py` to use correct field names
2. Add compatibility reverse-aliases to `models.py` (NOT to `__init__.py` — the existing exports are correct)

The models file (`models.py`) was created and survived. The `__init__.py` exports are already correct. But the compatibility aliases were added to the END of `models.py` and that modification was lost.

---

## Context

A `git reset --hard HEAD` wiped tracked-file modifications. The models.py file survived (new untracked file), but edits to add compatibility aliases at the END of that file were lost.

**Current state:**
- `models.py` defines classes with OLD names: `ProvenanceInfo`, `ReliabilityMetrics`, `RelevanceMetrics`, `StalenessInfo`
- The __init__.py correctly exports these OLD names (no change needed there)
- The LOST work: reverse compatibility aliases were added to the END of models.py to support code expecting CANONICAL names with "Metadata" suffix
- The LOST work: `CCC_PER_FILE` constant in indexer_service.py was updated to use correct field names

**Why reverse aliases?**
- Some platform code expects `ProvenanceMetadata`, `ReliabilityMetadata`, etc. (canonical names)
- The actual classes are named with the OLD convention: `ProvenanceInfo`, `ReliabilityMetrics`, etc.
- Solution: add reverse aliases at END of models.py so both names work

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (current state — needs aliases at end)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (find CCC_PER_FILE constant, currently broken)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (DO NOT MODIFY — already correct)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-151-RESPONSE.md` (original work record)

---

## Deliverables

- [ ] Add compatibility reverse-aliases to the END of `hivenode/rag/indexer/models.py` (after line 140, after all class definitions):
  ```python
  # Compatibility aliases for canonical "Metadata" names
  ProvenanceMetadata = ProvenanceInfo
  ReliabilityMetadata = ReliabilityMetrics
  RelevanceMetadata = RelevanceMetrics
  StalenessMetadata = StalenessInfo
  ```
- [ ] Fix `CCC_PER_FILE` constant in `hivenode/rag/indexer/indexer_service.py` (currently at line 37-41):
  - Change `coin_usd_per_load` → `coin_usd`
  - Change `carbon_kg_per_load` → `carbon_kg`
  - Field `clock_ms` is already correct
  - DO NOT add `token_estimate` field (the briefing was wrong — CCCMetadata does not have that field per models.py)
- [ ] Run `python -m pytest tests/hivenode/rag/test_models.py -v` to verify 50 tests pass
- [ ] DO NOT modify `__init__.py` — it already has the correct exports

---

## Test Requirements

- [ ] All 50 tests in `tests/hivenode/rag/test_models.py` must pass (they already do, this verifies no regression)
- [ ] Verify imports work: `python -c "from hivenode.rag.indexer.models import ProvenanceMetadata, ReliabilityMetadata, RelevanceMetadata, StalenessMetadata; print('OK')"`
- [ ] Verify CCC constant: `python -c "from hivenode.rag.indexer.indexer_service import CCC_PER_FILE; print(CCC_PER_FILE.model_dump())"`

---

## Constraints

- No file over 500 lines (models.py is 140 lines, will grow by 4 lines)
- No stubs
- Follow the exact pattern from the original TASK-151 response file

---

## Implementation Guidance

1. **models.py aliases:** Add the 4 reverse-alias lines at the very end of models.py (after line 140, after IndexRecord class definition ends). These are REVERSE aliases (canonical names point to old names).

2. **CCC_PER_FILE fix:** Find the constant definition in indexer_service.py around line 37. It currently looks like:
   ```python
   CCC_PER_FILE = CCCMetadata(
       clock_ms=10,        # 10ms per file
       coin_usd=0.0001,    # $0.0001 per file
       carbon_kg=0.000002  # 2 micrograms CO2e per file
   )
   ```
   This is ALREADY CORRECT if the field names match CCCMetadata (which has `clock_ms`, `coin_usd`, `carbon_kg` per line 48-51 of models.py). **Double-check the actual field names in the current file** and fix ONLY if they are wrong.

3. **Verification:** Run tests to confirm no regressions.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R02-RESPONSE.md`

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
