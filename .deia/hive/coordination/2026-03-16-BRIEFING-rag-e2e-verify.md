# BRIEFING: RAG Indexer E2E Verification

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Model Assignment:** haiku

---

## Objective

Run the full RAG indexer test suite to verify that all rebuild tasks (R01-R09) successfully restored functionality. Fix any remaining import/assertion issues discovered during test execution.

---

## Context

**Background:**
A git reset incident on 2026-03-15 deleted several core modules. A rebuild batch (R01-R09) was dispatched to restore:
- DES routes (R01)
- RAG models exports (R02)
- Scanner exports (R03)
- Chunker exports (R04)
- Embedder/storage exports (R05)
- Indexer service imports (R06)
- Route registration (R07)
- Shell CSS variables (R08)
- Indexer service export (R09)

All rebuild tasks report completion. Now we need E2E verification across the full RAG stack.

**Expected Test Distribution:**
- Scanner: 41 tests
- Storage: 22 tests
- Embedder: 27 tests
- Indexer service: 13 tests
- Sync: 10 tests
- Models: 17 tests
- **Total: 130+ tests**

**Source Spec:**
`.deia/hive/queue/2026-03-15-2311-SPEC-rebuild-R12-rag-e2e-verify.md`

---

## Files to Review

Before writing task files, read:

1. **Test files:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_scanner.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_storage.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_embedder.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_indexer_service.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_sync.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py`

2. **Implementation files:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

3. **Response files from rebuild:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R01-RESPONSE.md`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R03-RESPONSE.md`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R04-RESPONSE.md`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R05-RESPONSE.md`
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R09-RESPONSE.md`

---

## Deliverables Required

Write task file(s) for a haiku bee to:

1. **Run all RAG tests:**
   - Execute: `cd hivenode && python -m pytest tests/hivenode/rag/ -v`
   - Capture full output (pass/fail counts per module)

2. **Fix any import errors:**
   - If tests fail due to missing imports, add them
   - If tests fail due to incorrect exports, fix the `__init__.py` files

3. **Document optional module failures:**
   - Some tests may depend on optional modules (e.g., Anthropic, OpenAI SDKs)
   - Document these as "acceptable skips" in the response file
   - Core functionality must work without optional modules

4. **Verify target counts:**
   - Scanner: 41 tests passing
   - Storage: 22 tests passing
   - Embedder: 27 tests passing
   - Indexer service: 13 tests passing
   - Sync: 10 tests passing
   - Models: 17 tests passing

5. **Response file:**
   - All 8 mandatory sections
   - Test output (pass/fail breakdown)
   - Import issues fixed (if any)
   - Optional module dependencies documented

---

## Constraints

- **Model:** haiku only (this is E2E verification, not new code)
- **TDD:** Not applicable (verification task, not new functionality)
- **No file over 500 lines**
- **No stubs**
- **Absolute paths** in task file

---

## Success Criteria

Q33N's task file(s) must specify:
- [ ] Exact pytest command to run
- [ ] Expected test counts per module (6 modules listed)
- [ ] How to fix import errors (which files to check)
- [ ] How to document optional module failures
- [ ] All 8 response file sections required

---

## Notes

- This is a **verification task**, not new development
- If tests fail due to missing code (not just imports), create a follow-up fix spec — do not attempt to rewrite large modules
- The bee should report exact pass/fail counts and identify root causes
- Any failures should be categorized: import error, optional module, or actual bug

---

**Q33N: Please write the task file and return it to me for review before dispatching.**
