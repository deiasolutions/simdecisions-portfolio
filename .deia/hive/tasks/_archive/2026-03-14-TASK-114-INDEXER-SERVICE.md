# TASK-114: Indexer Service (Two-Pass Orchestrator)

**Wave:** 2
**Model:** sonnet
**Role:** bee
**Depends on:** TASK-110, TASK-111, TASK-112, TASK-113

---

## Objective

Build the orchestration layer that coordinates scanning, chunking, embedding, and indexing with two-pass TF-IDF fitting and Event Ledger integration.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (IndexRecord schema)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py` (scan function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py` (chunking functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\embedder.py` (TFIDFEmbedder)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (IndexStorage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\events\ledger.py` (Event Ledger schema for event emission)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_indexer_service.py`

## Files to Modify

None

## Deliverables

### indexer_service.py (301 lines)

**Class:** `IndexerService`

**Attributes:**
- `repo_path: Path` — repository to index
- `db_session: Optional[Session]` — SQLAlchemy session for Event Ledger (can be None for tests)
- `storage: IndexStorage` — IndexStorage instance
- `actor_id: str` — entity ID of indexer (for provenance)
- `node_id: str` — hive node ID (for provenance)
- `embedder: TFIDFEmbedder` — shared embedder instance (fitted once per repository)

**Methods:**

1. **`__init__(repo_path: Path, db_session: Optional[Session], storage: IndexStorage, actor_id: str, node_id: str)`**
   - Store all parameters
   - Initialize embedder = TFIDFEmbedder(vocab_size=500)

2. **`index_repository() -> dict`**
   - **Two-pass indexing:**
     - **Pass 1:** Scan all files, read all content, collect corpus
     - **Pass 2:** Fit TF-IDF embedder on full corpus, then index each file
   - Steps:
     1. Call `scan(repo_path)` to get list of (file_path, artifact_type)
     2. Read all file content into memory (list of strings)
     3. Call `embedder.fit(corpus)` to build vocabulary
     4. For each file: call `_index_single_file(file_path, artifact_type, use_fitted_embedder=True)`
     5. Return stats: `{"total_files": count, "indexed": success_count, "failed": fail_count, "vocab_size": embedder.vocab_size}`

3. **`index_file(file_path: Path) -> Optional[str]`**
   - Index a single file (cold-start, no pre-fitted embedder)
   - Detect artifact type using `scanner` logic
   - Call `_index_single_file(file_path, artifact_type, use_fitted_embedder=False)`
   - If use_fitted_embedder=False: fit embedder on single document only
   - Return artifact_id or None if failed

4. **`_index_single_file(file_path: Path, artifact_type: ArtifactType, use_fitted_embedder: bool = True) -> Optional[str]`**
   - Pipeline:
     1. Read file content
     2. Compute content_hash = `compute_content_hash(content)`
     3. Check if already indexed: `storage.get_by_path(str(file_path))`
     4. If exists and content_hash matches: skip (already indexed)
     5. Chunk content using `chunkers.chunk_code()` or `chunkers.chunk_document()` based on artifact_type
     6. If not use_fitted_embedder: fit embedder on this document only
     7. Embed chunks: `embedder.transform([chunk.content for chunk in chunks])`
     8. Compute IR summary: `ir_summary = _compute_ir_summary(chunks)`
     9. Create IndexRecord with all metadata
     10. Create EmbeddingRecord(s) (one per chunk or one combined)
     11. Call `storage.insert(record, chunks, embeddings)`
     12. Call `_emit_context_indexed_event(record)`
     13. Return artifact_id
   - Error handling: catch FileNotFoundError, SyntaxError, JSONDecodeError → log warning, return None

5. **`_compute_ir_summary(chunks: list[CodeChunk]) -> IRSummary`**
   - Flatten all ir_pairs from all chunks
   - Count by status: verified_count, failed_count, untested_count
   - Return IRSummary(verified_count=..., failed_count=..., untested_count=...)

6. **`_emit_context_indexed_event(record: IndexRecord) -> None`**
   - If db_session is None: skip (test mode)
   - Else: append event to Event Ledger
   - Event schema (from `hivenode/events/ledger.py`):
     ```python
     {
       "event_id": str(uuid4()),
       "event_type": "context.indexed",
       "timestamp": datetime.utcnow().isoformat(),
       "actor_id": self.actor_id,
       "node_id": self.node_id,
       "data": {
         "artifact_id": record.artifact_id,
         "path": record.path,
         "artifact_type": record.artifact_type,
         "keywords": record.keywords,
         "ccc": record.ccc.dict()
       }
     }
     ```
   - Use `append_event(db_session, event)` from ledger.py

**CCC Estimation (constants):**
```python
CCC_PER_FILE = CCCMetadata(
    clock_ms=10,        # 10ms per file
    coin_usd=0.0001,    # $0.0001 per file
    carbon_kg=0.000002  # 2 micrograms CO2e per file
)
```

**Helper constants:**
```python
DEFAULT_ACTOR_ID = "indexer-service"
DEFAULT_NODE_ID = "local-hive"
```

### test_indexer_service.py (10+ tests)

**Test cases:**
- Test `index_repository()` scans and indexes 5 files (Python, JS, Markdown, JSON, ADR)
- Test two-pass indexing: verify embedder.fit() called once with full corpus
- Test `index_file()` indexes single file with cold-start embedder
- Test `_compute_ir_summary()` counts IR pairs correctly (2 verified, 1 failed, 3 untested)
- Test `_emit_context_indexed_event()` appends event to ledger (use mock db_session)
- Test skip already-indexed file (same content_hash)
- Test re-index file with changed content (different content_hash)
- Test error handling: missing file → logs warning, returns None
- Test error handling: syntax error in Python file → logs warning, returns None
- Test CCC metadata attached to IndexRecord
- Test provenance fields (actor_id, node_id) in IndexRecord

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/test_indexer_service.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same two-pass indexing, same IR summary logic, same event schema as platform/efemera
- [ ] TDD: tests written first
- [ ] 10+ tests covering two-pass indexing, single file, IR summary, event emission, errors (missing files, syntax errors)
- [ ] CCC estimation: 10ms clock, $0.0001 coin, 0.000002kg carbon per file

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-114-RESPONSE.md`

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
