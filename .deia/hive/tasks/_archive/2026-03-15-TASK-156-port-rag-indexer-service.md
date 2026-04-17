# TASK-156: Port RAG Indexer Service (Orchestration)

## Objective
Port the high-level indexer orchestration service that coordinates scan → chunk → embed → store → emit event pipeline.

## Context
The IndexerService is the top-level coordinator that ties together Scanner, Chunker, TFIDFEmbedder, and IndexStorage. It implements a two-pass indexing process:
1. Scan all files, collect corpus
2. Fit embedder on corpus, then index each file

It also emits CONTEXT_INDEXED events to the Event Ledger (if available).

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\indexer_service.py` (301 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`

**Dependencies:**
- TASK-151 (models.py)
- TASK-152 (scanner.py)
- TASK-153 (chunker.py)
- TASK-154 (embedder.py)
- TASK-155 (storage.py)

**Event Ledger Dependency:** The platform version imports `from ..events.ledger import log_event`. ShiftCenter does NOT have this module yet. You have two options:
1. **Stub the event emission** for now (add TODO comment, emit events will be added later)
2. **Check if Event Ledger exists** in shiftcenter and only emit if available

**Recommended approach:** Stub event emission with clear TODO comment. The spec says "critical for BABOK interview bot" but the indexer should work without event logging for now.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\indexer_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py` (from TASK-152)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py` (from TASK-153)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py` (from TASK-154)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (from TASK-155)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
- [ ] Port IndexerService class with methods:
  - `__init__(repo_path, db_session, storage, actor_id, node_id)` — initialize with dependencies
  - `index_repository()` → dict[str, int] — two-pass full repository indexing
  - `index_file(file_path)` → str | None — index single file, return artifact_id
  - `_index_single_file(file_path, artifact_type)` → str — full pipeline for one file
  - `_compute_ir_summary(chunks)` → IRSummary — rollup IR verification stats
  - `_emit_context_indexed_event(record, is_reindex)` → None — emit event (STUB for now)
  - `close()` → None — cleanup resources
- [ ] Stub event emission with clear TODO comment (no Event Ledger in shiftcenter yet)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` to export IndexerService
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_indexer_service.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test index_repository() scans and indexes multiple files
- [ ] Test index_repository() returns correct stats (indexed, skipped, errors)
- [ ] Test index_repository() fits embedder on corpus before indexing
- [ ] Test index_file() indexes single Python file
- [ ] Test index_file() indexes single JavaScript file
- [ ] Test index_file() indexes single markdown file
- [ ] Test index_file() returns artifact_id on success
- [ ] Test index_file() returns None for unsupported file type
- [ ] Test _index_single_file() creates complete IndexRecord
- [ ] Test _index_single_file() stores record in SQLite
- [ ] Test _index_single_file() computes IR summary correctly
- [ ] Test _compute_ir_summary() rollup logic
- [ ] Test close() cleans up storage connection
- [ ] Test error handling:
  - File read errors (UnicodeDecodeError)
  - Invalid JSON in PHASE-IR files
  - Missing files
- [ ] Edge cases:
  - Empty repository
  - Repository with only excluded files
  - Very large repository (100+ files)

**Target test count:** 18+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_indexer_service.py -v
```

## Constraints
- No file over 500 lines (indexer_service.py is 301 lines, under limit)
- No stubs — all methods fully implemented EXCEPT event emission (stub with TODO)
- TDD: tests first
- Port verbatim from platform, except stub `_emit_context_indexed_event()`

## Event Emission Stub Template

```python
def _emit_context_indexed_event(self, record: IndexRecord, is_reindex: bool) -> None:
    """
    Emit CONTEXT_INDEXED event to Event Ledger.

    TODO(TASK-156): Event Ledger not yet ported to shiftcenter.
    This will emit events once hivenode/events/ledger.py exists.
    See platform/efemera/src/efemera/events/ledger.py for reference.

    Args:
        record: Indexed record
        is_reindex: Whether this is a re-index operation
    """
    # STUB: Event emission pending Event Ledger port
    pass
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-156-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks (MUST note Event Ledger pending)

DO NOT skip any section.

---

**Priority:** P0.50
**Model:** sonnet (orchestration logic, dependency integration)
**Estimated time:** 35 minutes
**Dependencies:** TASK-151, TASK-152, TASK-153, TASK-154, TASK-155
