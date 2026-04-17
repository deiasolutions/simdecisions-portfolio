# TASK-162: Verify RAG Indexer End-to-End

## Objective
Verify RAG indexer works end-to-end by running all indexer tests.

## Context
After TASK-161 fixes import errors, we need to verify the entire RAG indexer pipeline works:
1. Scanning files in a repo
2. Chunking content
3. Embedding chunks with TF-IDF
4. Storing index records
5. Querying by similarity

The indexer was ported from platform/efemera and all test files were ported as well.

**Test directory:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_scanner.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_storage.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_embedder.py` (if exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\conftest.py`

## Deliverables
- [ ] Run all tests in `tests/hivenode/rag/indexer/` directory
- [ ] Fix any failing tests (no stubs)
- [ ] Document any missing test coverage
- [ ] All tests pass

## Test Requirements
- [ ] Run `cd hivenode && python -m pytest tests/hivenode/rag/indexer/ -v`
- [ ] All tests must pass (0 failures, 0 errors)
- [ ] Document pass/fail count in response

## Constraints
- No file over 500 lines
- No stubs — if code is broken, fix it properly
- TDD: If tests are missing, write them first

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-162-RESPONSE.md`

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
