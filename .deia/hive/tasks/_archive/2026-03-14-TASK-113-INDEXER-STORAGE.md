# TASK-113: Indexer Storage (SQLite)

**Wave:** 2
**Model:** sonnet
**Role:** bee
**Depends on:** TASK-110

---

## Objective

Build SQLite-based persistence layer for IndexRecord, chunks, and embeddings with cascade delete and content hashing.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (from TASK-110 — IndexRecord schema)
- Source file in `platform/efemera/src/efemera/indexer/storage.py` (reference for schema)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_storage.py`

## Files to Modify

None

## Deliverables

### storage.py (463 lines)

**Database Schema (3 tables):**

1. **`index_records` table:**
   - `artifact_id` TEXT PRIMARY KEY
   - `path` TEXT NOT NULL
   - `artifact_type` TEXT NOT NULL
   - `storage_tier` TEXT NOT NULL
   - `keywords` TEXT (JSON array)
   - `content_hash` TEXT NOT NULL
   - `engines` TEXT (JSON array)
   - `ir_summary` TEXT (JSON object: {verified_count, failed_count, untested_count})
   - `ccc` TEXT (JSON object: {clock_ms, coin_usd, carbon_kg})
   - `reliability` TEXT (JSON object: {reliability_score, availability, latency_ms, last_updated})
   - `relevance` TEXT (JSON object: {retrieval_count, llm_used, llm_ignored, helpful_feedback, not_helpful_feedback})
   - `staleness` TEXT (JSON object: {indexed_at, modified_at, days_stale})
   - `provenance` TEXT (JSON object: {source, actor_id, node_id, indexed_by})
   - `created_at` TEXT NOT NULL
   - `updated_at` TEXT NOT NULL
   - Indexes: `CREATE INDEX idx_artifact_type ON index_records(artifact_type)`
   - Indexes: `CREATE INDEX idx_storage_tier ON index_records(storage_tier)`
   - Indexes: `CREATE INDEX idx_path ON index_records(path)`

2. **`chunks` table:**
   - `chunk_id` TEXT PRIMARY KEY (UUID)
   - `artifact_id` TEXT NOT NULL (FK to index_records, ON DELETE CASCADE)
   - `content` TEXT NOT NULL
   - `start_line` INTEGER
   - `end_line` INTEGER
   - `char_count` INTEGER
   - `token_estimate` INTEGER
   - `ir_pairs` TEXT (JSON array of objects)
   - `created_at` TEXT NOT NULL
   - Foreign key: `FOREIGN KEY(artifact_id) REFERENCES index_records(artifact_id) ON DELETE CASCADE`

3. **`embeddings` table:**
   - `artifact_id` TEXT NOT NULL (FK to index_records, ON DELETE CASCADE)
   - `engine` TEXT NOT NULL
   - `vector` BLOB NOT NULL (pickled list[float])
   - `dimension` INTEGER NOT NULL
   - `created_at` TEXT NOT NULL
   - Composite primary key: `PRIMARY KEY(artifact_id, engine)`
   - Foreign key: `FOREIGN KEY(artifact_id) REFERENCES index_records(artifact_id) ON DELETE CASCADE`

**Class:** `IndexStorage`

**Attributes:**
- `db_path: Path` — path to SQLite file (default: `~/hive/local/index.db`)
- `conn: sqlite3.Connection` — database connection

**Methods:**

1. **`__init__(db_path: Optional[Path] = None)`**
   - Default path: `Path.home() / "hive" / "local" / "index.db"`
   - Create parent directories if not exist
   - Connect to SQLite
   - Enable foreign keys: `PRAGMA foreign_keys = ON`
   - Call `_create_schema()`

2. **`_create_schema()`**
   - Create 3 tables if not exist
   - Create indexes

3. **`insert(record: IndexRecord, chunks: list[CodeChunk] = None, embeddings: list[EmbeddingRecord] = None) -> str`**
   - Serialize IndexRecord to row (convert Pydantic models to JSON strings)
   - INSERT into `index_records`
   - If chunks provided: INSERT each chunk into `chunks` table
   - If embeddings provided: INSERT each embedding into `embeddings` table (pickle vector)
   - Return artifact_id

4. **`get_by_id(artifact_id: str) -> Optional[IndexRecord]`**
   - SELECT from `index_records` WHERE artifact_id = ?
   - Deserialize JSON fields back to Pydantic models
   - Return IndexRecord or None

5. **`get_by_path(path: str) -> Optional[IndexRecord]`**
   - SELECT from `index_records` WHERE path = ?
   - Deserialize and return

6. **`update(record: IndexRecord, chunks: list[CodeChunk] = None, embeddings: list[EmbeddingRecord] = None) -> None`**
   - DELETE FROM index_records WHERE artifact_id = ? (cascade deletes chunks + embeddings)
   - Call `insert(record, chunks, embeddings)` to re-insert

7. **`delete(artifact_id: str) -> None`**
   - DELETE FROM index_records WHERE artifact_id = ? (cascade delete)

8. **`list_all(artifact_type: Optional[str] = None, storage_tier: Optional[str] = None, limit: int = 100, offset: int = 0) -> list[IndexRecord]`**
   - SELECT with optional filters on artifact_type, storage_tier
   - LIMIT and OFFSET for pagination
   - Deserialize all rows
   - Return list of IndexRecord

9. **`get_chunks(artifact_id: str) -> list[CodeChunk]`**
   - SELECT from `chunks` WHERE artifact_id = ?
   - Deserialize ir_pairs from JSON
   - Return list of CodeChunk

10. **`get_embeddings(artifact_id: str) -> list[EmbeddingRecord]`**
    - SELECT from `embeddings` WHERE artifact_id = ?
    - Unpickle vector
    - Return list of EmbeddingRecord

11. **`close()`**
    - Close database connection

**Standalone function:**

12. **`compute_content_hash(content: str) -> str`**
    - SHA256 hash of content (UTF-8 bytes)
    - Return hex digest

### test_storage.py (12+ tests)

**Test cases:**
- Test database schema creation (verify 3 tables exist with correct columns)
- Test `insert()` creates record in index_records table
- Test `insert()` with chunks creates entries in chunks table
- Test `insert()` with embeddings creates entries in embeddings table
- Test `get_by_id()` retrieves correct record
- Test `get_by_path()` retrieves correct record
- Test `update()` deletes old record and re-inserts (verify old chunks deleted)
- Test cascade delete (delete index_record → verify chunks + embeddings deleted)
- Test `list_all()` with no filters returns all records
- Test `list_all()` with artifact_type filter returns only matching records
- Test `list_all()` pagination (limit + offset)
- Test `compute_content_hash()` produces consistent SHA256 hex
- Test `get_chunks()` and `get_embeddings()` return correct data

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/test_storage.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same 3-table schema, same cascade delete, same JSON serialization as platform/efemera
- [ ] TDD: tests written first
- [ ] 12+ tests covering insert, get, update, delete, list with filters, cascade delete, content hash
- [ ] Default DB path uses `~/hive/local/` NOT `~/.shiftcenter/`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-113-RESPONSE.md`

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
