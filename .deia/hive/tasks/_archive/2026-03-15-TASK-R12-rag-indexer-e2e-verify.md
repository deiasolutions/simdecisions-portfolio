# TASK-R12: RAG Indexer E2E Verification (Rebuild)

## Objective
Run the full RAG indexer test suite to verify that all batch 1 and batch 2 rebuild tasks have successfully restored the RAG indexer functionality. Fix any remaining test issues discovered during verification.

## Context
This is a rebuild of TASK-162, which verified the RAG indexer end-to-end after the original port. Now, after the git reset and batch 1+2 rebuilds (TASK-R02 through TASK-R06, TASK-R09), we need to re-verify that everything works.

**Batch 1 rebuilt:**
- TASK-R02: Restored rag.models exports and CCC metadata fix
- TASK-R03: Added Scanner class to exports
- TASK-R04: Added Chunker to exports
- TASK-R05: Added embedder and storage exports
- TASK-R06: Fixed indexer_service.py imports

**Batch 2 rebuilt:**
- TASK-R09: RAG core 3-module set (Scanner, Chunker, VectorSearchService)

**What this bee must do:**
Run the full RAG test suite and verify 130+ core tests pass. If any import errors or assertion failures remain, fix them.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (should export all necessary classes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (should have correct imports after R06)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\` (test directory structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1438-BEE-HAIKU-2026-03-15-TASK-162-VERIFY-RAG-INDEXER-E2E-RAW.txt` (original verification report)

## Deliverables

### 1. Run Full RAG Test Suite
- [ ] Run: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/rag/ -v`
- [ ] Document which test files pass and which fail
- [ ] Note any import errors or missing dependencies

### 2. Fix Any Remaining Issues
- [ ] If import errors exist in test files, fix them
- [ ] If assertion failures exist due to missing exports, add exports to `__init__.py`
- [ ] If indexer_service.py has import issues, fix imports
- [ ] Re-run tests after each fix

### 3. Document Results
- [ ] Report test count by module:
  - Scanner tests (target: 41 passing)
  - Storage tests (target: 22 passing)
  - Embedder tests (target: 27 passing)
  - Indexer service tests (target: 13 passing)
  - Sync daemon tests (target: 10 passing)
  - Models tests (target: 17 passing)
- [ ] Total target: **130+ core tests passing**
- [ ] Note which optional modules have failures (markdown_exporter, metrics_updater, reliability, cloud_sync — these are OK to fail)

## Test Requirements
- [ ] Core RAG tests pass (130+)
- [ ] Scanner: 41 tests passing
- [ ] Storage: 22 tests passing
- [ ] Embedder: 27 tests passing
- [ ] Indexer service: 13 tests passing
- [ ] Sync daemon: 10 tests passing
- [ ] Models: 17 tests passing
- [ ] Document which optional modules fail (if any)

## Expected Test Output
Based on TASK-162 original verification:
```
✅ Scanner (41 tests) - File detection and filtering
✅ Storage (22 tests) - SQLite persistence and CRUD
✅ Embedder (27 tests) - TF-IDF vectorization
✅ Indexer Service (13 tests) - Two-pass pipeline
✅ Sync Daemon (10 tests) - Cloud/markdown export
✅ Models (17 tests) - Schema validation

Total: 130 core tests passing
```

## Constraints
- Fix only import errors and missing exports — DO NOT refactor test logic
- If a test fails due to a missing export, add it to `__init__.py`
- If a test fails due to wrong import path, fix the import
- If a test fails for another reason (logic bug), document it but don't fix it (out of scope)
- No file over 500 lines

## Acceptance Criteria
- [ ] RAG test suite runs without import errors
- [ ] 130+ core tests passing across 6 modules
- [ ] Scanner: 41 tests passing
- [ ] Storage: 22 tests passing
- [ ] Embedder: 27 tests passing
- [ ] Indexer service: 13 tests passing
- [ ] Sync daemon: 10 tests passing
- [ ] Models: 17 tests passing
- [ ] Optional module failures documented (markdown_exporter, metrics_updater, reliability, cloud_sync)
- [ ] All fixes applied to source files (if needed)
- [ ] Response file written with full test output summary

## Dependencies
This task MUST run AFTER all batch 1 and batch 2 rebuild tasks complete:
- TASK-R02 (rag.models exports)
- TASK-R03 (Scanner exports)
- TASK-R04 (Chunker exports)
- TASK-R05 (embedder/storage exports)
- TASK-R06 (indexer_service imports)
- TASK-R09 (RAG core 3-module set)

Do NOT start this task until all batch 1+2 tasks are confirmed complete.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R12-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths (if none, state "No files modified")
3. **What Was Done** — bullet list of concrete actions (ran tests, fixed N imports, etc.)
4. **Test Results** — full test output summary with pass/fail counts by module
5. **Build Verification** — pytest exit code, summary line
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — which optional modules failed (if any), next steps

DO NOT skip any section.
