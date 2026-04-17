# TASK-R09: Add IndexerService export to RAG __init__.py

**Priority:** P0.45
**Original:** TASK-161 (RAG init fixes)
**Rebuild Batch:** 02
**Date:** 2026-03-15

---

## Objective

Restore the missing `IndexerService` export from `hivenode/rag/indexer/__init__.py` that was lost in the git reset.

---

## Context

After `git reset --hard HEAD`, a simple one-line fix from TASK-161 was lost:
- The `IndexerService` class was not exported from `hivenode/rag/indexer/__init__.py`
- This prevents the class from being imported as `from hivenode.rag.indexer import IndexerService`

This is a trivial fix but required for proper module API.

**Dependencies:**
- This task depends on TASK-R06 completing first (IndexerService needs fixed imports before export)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state — missing export)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (verify class exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-161-RESPONSE.md` (original fix details)

---

## Deliverables

### 1. Add Import Statement

- [ ] In `hivenode/rag/indexer/__init__.py`, add:
  ```python
  from hivenode.rag.indexer.indexer_service import IndexerService
  ```
- [ ] Place import after existing imports but before `__all__`

### 2. Add to `__all__` List

- [ ] Add `"IndexerService"` to the `__all__` list in same file
- [ ] Maintain alphabetical order in `__all__` list

### 3. Verify Import Works

- [ ] Run verification command:
  ```bash
  python -c "from hivenode.rag.indexer import IndexerService; print('OK')"
  ```
- [ ] Expected output: `OK`

---

## Test Requirements

### Tests Written FIRST (TDD)
- [ ] No new tests needed — existing tests verify IndexerService functionality

### All Tests Pass
- [ ] Run storage tests: `python -m pytest tests/hivenode/rag/indexer/test_storage.py -v`
- [ ] Expected: **22 tests PASSING**
- [ ] Run scanner tests: `python -m pytest tests/hivenode/rag/indexer/test_scanner.py -v`
- [ ] Expected: **32 tests PASSING**
- [ ] Total expected: **54 tests PASSING** (22 storage + 32 scanner)

### Import Verification
- [ ] Verify import works from Python REPL
- [ ] Verify no circular import errors

---

## Constraints

- No file over 500 lines (`__init__.py` is currently ~20 lines — well within limits)
- No stubs (just adding an import and export)
- Do NOT modify `indexer_service.py` — only touch `__init__.py`

---

## Acceptance Criteria

- [x] Import added: `from hivenode.rag.indexer.indexer_service import IndexerService`
- [x] Export added: `"IndexerService"` in `__all__`
- [x] Import verification command prints "OK"
- [x] 22 storage tests pass
- [x] 32 scanner tests pass
- [x] No circular import errors

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R09-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary (include import verification output)
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Haiku (trivial one-line export)
**Estimated Duration:** 3 minutes
**Depends On:** TASK-R06 (IndexerService must have fixed imports first)
