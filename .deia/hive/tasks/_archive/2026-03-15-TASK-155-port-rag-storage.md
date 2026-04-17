# TASK-155: Port RAG SQLite Storage Module

## Objective
Port the SQLite vector storage module that persists index records with full schema, chunks, and embeddings, and provides similarity search via cosine distance.

## Context
The IndexStorage class manages SQLite persistence for the RAG index. It stores index records, chunks (one-to-many), and embeddings (many-to-many with engines). Includes similarity search using cosine similarity.

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\storage.py` (463 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`

**Dependencies:** TASK-151 (models.py) must be complete.

**IMPORTANT:** This file is 463 lines. Per constraints, no file can exceed 500 lines. If porting verbatim pushes it over 500 lines, split into:
- `storage.py` (core CRUD operations)
- `search.py` (similarity search functions)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\storage.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (from TASK-151)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
- [ ] Port IndexStorage class with methods:
  - `__init__(db_path)` — initialize SQLite connection, create schema if missing
  - `_create_schema()` — create tables: index_records, chunks, embeddings
  - `insert(record)` → None — insert IndexRecord with chunks and embeddings
  - `get_by_id(artifact_id)` → IndexRecord | None — retrieve by ID
  - `get_by_path(path)` → IndexRecord | None — retrieve by file path
  - `update(record)` → None — update existing record
  - `delete(artifact_id)` → None — delete record and cascade to chunks/embeddings
  - `list_all(artifact_type)` → list[IndexRecord] — list all records, optionally filtered
  - `_row_to_record(row)` → IndexRecord — reconstruct from SQLite row
  - `_load_chunks(artifact_id)` → list[Chunk] — load chunks for artifact
  - `_load_embeddings(artifact_id)` → dict[str, EmbeddingRecord] — load embeddings
  - `close()` → None — close DB connection
- [ ] Port utility function: `compute_content_hash(content)` → str
- [ ] If over 500 lines, create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\search.py` for similarity search
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` to export IndexStorage
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_storage.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test _create_schema() creates all 3 tables
- [ ] Test _create_schema() creates indexes
- [ ] Test insert() stores record with chunks and embeddings
- [ ] Test insert() handles empty chunks list
- [ ] Test insert() handles empty embeddings dict
- [ ] Test get_by_id() retrieves complete record
- [ ] Test get_by_id() returns None for missing ID
- [ ] Test get_by_path() retrieves by file path
- [ ] Test update() modifies existing record
- [ ] Test delete() removes record and cascades
- [ ] Test list_all() returns all records
- [ ] Test list_all(artifact_type=CODE) filters by type
- [ ] Test _row_to_record() reconstructs IndexRecord correctly
- [ ] Test _load_chunks() loads chunks with IR pairs
- [ ] Test _load_embeddings() loads embeddings keyed by engine
- [ ] Test compute_content_hash() generates SHA256 hash
- [ ] Test concurrent access (multiple threads)
- [ ] Edge cases:
  - Insert duplicate artifact_id (should fail or replace)
  - Very large embeddings (10k+ dimensions)
  - Unicode content
  - Missing optional fields in models

**Target test count:** 20+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_storage.py -v
```

## Constraints
- No file over 500 lines (storage.py is 463 lines — close to limit)
- If over 500, split into storage.py + search.py
- No stubs — all methods fully implemented
- TDD: tests first
- Port verbatim — do NOT modify logic from platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-155-RESPONSE.md`

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

---

**Priority:** P0.50
**Model:** sonnet (complex storage logic + potential split decision)
**Estimated time:** 35 minutes
**Dependency:** TASK-151
