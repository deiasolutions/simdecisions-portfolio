# TASK-161: Fix RAG Indexer Import Errors

## Objective
Fix import errors in RAG indexer code so tests can run.

## Context
The RAG indexer code was ported from platform/efemera but has incorrect import paths:

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`

**Current imports (lines 17-18):**
```python
from hivenode.rag.chunkers import CodeChunk, chunk_file
from hivenode.rag.embedder import TFIDFEmbedder
```

**Issue:** Line 17 is CORRECT (chunkers.py exists in hivenode/rag/). Line 18 is also CORRECT (embedder.py exists in hivenode/rag/ with TFIDFEmbedder that takes vocab_size param).

**Actual issue:** The `__init__.py` file does not export `IndexerService`, which is needed by routes and other modules.

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

This file imports and exports many symbols but is missing `IndexerService` in both the import statement and the `__all__` list.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

## Deliverables
- [ ] Add `IndexerService` import to `hivenode/rag/indexer/__init__.py`
- [ ] Add `IndexerService` to `__all__` list in same file
- [ ] Verify import works: `from hivenode.rag.indexer import IndexerService`

## Test Requirements
- [ ] Run `python -c "from hivenode.rag.indexer import IndexerService; print('OK')"` — should print "OK"
- [ ] Run `pytest tests/hivenode/rag/indexer/test_storage.py -v` — should pass
- [ ] Run `pytest tests/hivenode/rag/indexer/test_scanner.py -v` — should pass

## Constraints
- No file over 500 lines
- No stubs
- Only modify `__init__.py` — do not modify `indexer_service.py`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-161-RESPONSE.md`

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
