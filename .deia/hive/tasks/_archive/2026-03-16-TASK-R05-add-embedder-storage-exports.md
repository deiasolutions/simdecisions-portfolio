# TASK-R05: Add TFIDFEmbedder and IndexStorage exports

## Objective

Add three missing exports to `hivenode/rag/indexer/__init__.py`: `TFIDFEmbedder`, `IndexStorage`, and `compute_content_hash`. These classes already exist in their respective modules but are not exposed in the public API.

## Context

The RAG indexer module has three separate files:
- `hivenode/rag/indexer/embedder.py` contains `TFIDFEmbedder` (line 16)
- `hivenode/rag/indexer/storage.py` contains `IndexStorage` (line 47) and `compute_content_hash` (line 35)

The `__init__.py` currently exports Chunker, Scanner, scan, and various model classes, but the embedder and storage layer exports are missing. This prevents external code from importing these critical classes directly from the `hivenode.rag.indexer` package.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py` (confirm TFIDFEmbedder exists at line 16)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (confirm IndexStorage at line 47 and compute_content_hash at line 35)

## Deliverables

- [ ] TFIDFEmbedder imported and exported from `hivenode/rag/indexer/__init__.py`
- [ ] IndexStorage imported and exported from `hivenode/rag/indexer/__init__.py`
- [ ] compute_content_hash imported and exported from `hivenode/rag/indexer/__init__.py`
- [ ] `__all__` list updated with three new exports in alphabetical order
- [ ] All 34 embedder tests pass
- [ ] All storage tests pass
- [ ] Build verification complete

## Test Requirements

- [ ] Tests written first (TDD) — but these are pre-existing tests, no new tests needed for this export task
- [ ] Run: `cd hivenode && python -m pytest tests/rag/indexer/test_embedder.py -v`
- [ ] Run: `cd hivenode && python -m pytest tests/rag/indexer/test_storage.py -v`
- [ ] All tests pass before and after the change
- [ ] No regressions in other RAG indexer tests

## Constraints

- No file over 500 lines (this change keeps `__init__.py` well under 50 lines)
- No stubs
- Maintain alphabetical ordering in `__all__` list
- Follow existing import/export pattern in the file

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-R05-RESPONSE.md`

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
