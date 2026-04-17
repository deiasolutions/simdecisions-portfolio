# TASK-R12: RAG Indexer E2E Verification

## Objective

Run the complete RAG indexer test suite to verify that all rebuild tasks (R01-R09) successfully restored functionality. Fix any remaining import/assertion issues discovered during test execution.

---

## Context

**Background:**
A git reset incident on 2026-03-15 deleted several core RAG modules. A rebuild batch (R01-R09) restored:
- DES routes registration (R01)
- RAG models exports (R02)
- Scanner exports (R03)
- Chunker exports (R04)
- Embedder/storage exports (R05)
- Indexer service imports (R06)
- Route registration (R07)
- Shell CSS variables (R08)
- Indexer service export (R09)

All rebuild tasks reported completion. This task performs comprehensive E2E verification across the full RAG stack.

**Expected Test Distribution (130+ tests across 6 modules):**
- Scanner: 41 tests
- Storage: 22 tests
- Embedder: 27 tests
- Indexer service: 13 tests
- Sync: 10 tests
- Models: 17 tests

**Key Files:**
- Test suite root: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\`
- Implementation root: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\`
- Main exports: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_scanner.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_storage.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_embedder.py`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_indexer_service.py`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_sync_daemon.py`
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py`
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`
9. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
10. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`

---

## Deliverables

- [ ] Run complete RAG test suite: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/rag/ -v`
- [ ] Capture full test output (pass/fail counts per module)
- [ ] Fix any import errors in implementation files
- [ ] Fix any assertion errors in test files
- [ ] Document optional module failures (e.g., Anthropic SDK, OpenAI SDK)
- [ ] Verify target test counts:
  - [ ] Scanner: 41 tests passing
  - [ ] Storage: 22 tests passing
  - [ ] Embedder: 27 tests passing
  - [ ] Indexer service: 13 tests passing
  - [ ] Sync: 10 tests passing
  - [ ] Models: 17 tests passing
  - [ ] **Total: 130+ tests passing**

---

## Test Requirements

- [ ] **No import errors** across the RAG test suite
- [ ] **All core tests pass** (scanner, storage, embedder, indexer service, sync, models)
- [ ] **Optional module failures documented** (if any—e.g., Anthropic, OpenAI SDKs not installed)
- [ ] **Root causes identified** for any failures (import error, optional module, actual bug)
- [ ] **Response file written with all 8 sections**

---

## Constraints

- Model: Haiku only (verification task)
- TDD: Not applicable (verification task, not new functionality)
- No file over 500 lines
- No stubs
- Absolute paths in responses

---

## Acceptance Criteria

- [x] All 8 response file sections required
- [x] Exact pass/fail test counts per module documented
- [x] Import issues fixed (if any)
- [x] Optional module failures documented
- [x] Root cause analysis for any test failures
- [x] Command used to run tests specified
- [x] Expected test counts verified (130+)
- [x] No stubs shipped

---

## Response Requirements — MANDATORY

Write response file: `.deia/hive/responses/20260316-TASK-R12-RESPONSE.md`

**Must include all 8 sections:**

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — any files edited (implementation or test files)
3. **What Was Done** — concrete changes (import fixes, assertion fixes, etc.)
4. **Test Results** — test files run, pass/fail counts per module
5. **Build Verification** — test output summary (final 5-10 lines from pytest)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — wall time, estimated USD, estimated CO2e
8. **Issues / Follow-ups** — any failures, root causes, next steps

**Example Test Results format:**

```
## Test Results

**RAG Test Suite:**
- Scanner: 41/41 passed ✓
- Storage: 22/22 passed ✓
- Embedder: 27/27 passed ✓
- Indexer service: 13/13 passed ✓
- Sync: 10/10 passed ✓
- Models: 17/17 passed ✓
- **Total: 130/130 passed** ✓

Optional module tests (acceptable skips):
- test_anthropic_embedder: SKIPPED (Anthropic SDK not installed)
- test_openai_embedder: SKIPPED (OpenAI SDK not installed)
```

---

## Notes

- This is a **verification task**, not new development
- If tests fail due to missing code (not just imports), create a follow-up fix spec — do NOT attempt to rewrite large modules
- Report exact pass/fail counts and identify root causes
- Categorize any failures: import error, optional module, or actual bug
- Q33N will review response and report results to Q33NR

