# TASK-116: Markdown Exporter + Cloud Sync

**Wave:** 3
**Model:** sonnet
**Role:** bee
**Depends on:** TASK-113

---

## Objective

Build markdown export system (for `.deia/index/` human-readable cache) and PostgreSQL cloud sync with pgvector for embedding search.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (IndexRecord schema)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (IndexStorage)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\markdown_exporter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\cloud_sync.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_markdown_exporter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_cloud_sync.py`

## Files to Modify

None

## Deliverables

### markdown_exporter.py (195 lines)

**Class:** `MarkdownExporter`

**Attributes:**
- `markdown_dir: Path` — directory for markdown files (default: `.deia/index/`)

**Methods:**

1. **`__init__(markdown_dir: Optional[Path] = None)`**
   - Default: `Path(".deia/index/")`
   - Create directory if not exists

2. **`export_to_markdown(record: IndexRecord) -> str`**
   - Format IndexRecord as markdown with these sections:
     ```markdown
     # {artifact_id}

     **Path:** {path}
     **Type:** {artifact_type}
     **Tier:** {storage_tier}
     **Indexed:** {indexed_at}
     **Modified:** {modified_at}
     **Stale:** {days_stale} days

     ## Keywords
     {comma-separated keywords}

     ## IR Pairs
     {for each IR pair:}
     - {status_symbol} {intent} → {result}

     Status symbols: ✓ (VERIFIED), ✗ (FAILED), ~ (UNTESTED), ? (UNKNOWN)

     ## Embedding Engines
     {comma-separated engines}

     ## CCC
     - Clock: {clock_ms} ms
     - Coin: ${coin_usd}
     - Carbon: {carbon_kg} kg CO2e

     ## Reliability
     - Score: {reliability_score} ({reliability_score * 100}%)
     - Availability: {availability}
     - Latency: {latency_ms} ms

     ## Relevance
     - Retrievals: {retrieval_count}
     - LLM used: {llm_used} / ignored: {llm_ignored}
     - Feedback: {helpful_feedback} helpful / {not_helpful_feedback} not helpful

     ## Content Preview
     {first 500 chars of content}
     ```

3. **`write_markdown_file(artifact_id: str, storage: IndexStorage) -> Path`**
   - Fetch IndexRecord from storage
   - Call `export_to_markdown(record)`
   - Write to `{markdown_dir}/{artifact_id}.md`
   - Return file path

4. **`sync_all_to_markdown(storage: IndexStorage) -> list[Path]`**
   - Get all records: `storage.list_all()`
   - For each record: call `write_markdown_file()`
   - Return list of written file paths

### test_markdown_exporter.py (6+ tests)

**Test cases:**
- Test `export_to_markdown()` produces correct markdown format
- Test all sections present (Keywords, IR Pairs, Embedding Engines, CCC, Reliability, Relevance, Content Preview)
- Test IR pair status symbols (✓ ✗ ~ ?)
- Test `write_markdown_file()` writes to disk
- Test `sync_all_to_markdown()` exports multiple records
- Test directory creation if not exists

---

### cloud_sync.py (319 lines)

**Class:** `CloudSyncService`

**Attributes:**
- `storage: IndexStorage` — local SQLite storage
- `exporter: MarkdownExporter` — for markdown sync
- `db_url: Optional[str]` — Postgres connection string (from env: `HIVE_CLOUD_DB_URL`)
- `conn: Optional[psycopg2.connection]` — Postgres connection (None if db_url not set)

**Methods:**

1. **`__init__(storage: IndexStorage, exporter: MarkdownExporter, db_url: Optional[str] = None)`**
   - Default db_url: `os.getenv("HIVE_CLOUD_DB_URL")`
   - Store parameters
   - conn = None (call `connect()` explicitly)

2. **`connect() -> None`**
   - If db_url is None: log WARNING "Cloud sync disabled (no HIVE_CLOUD_DB_URL)", return
   - Create psycopg2 connection: `psycopg2.connect(db_url)`
   - Call `ensure_schema()`

3. **`ensure_schema() -> None`**
   - Execute SQL:
     ```sql
     CREATE EXTENSION IF NOT EXISTS vector;

     CREATE TABLE IF NOT EXISTS cloud_index_records (
       artifact_id TEXT PRIMARY KEY,
       path TEXT NOT NULL,
       artifact_type TEXT NOT NULL,
       storage_tier TEXT NOT NULL,
       keywords JSONB,
       content_hash TEXT NOT NULL,
       engines JSONB,
       ir_summary JSONB,
       ccc JSONB,
       reliability JSONB,
       relevance JSONB,
       staleness JSONB,
       provenance JSONB,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
     );

     CREATE TABLE IF NOT EXISTS cloud_chunks (
       chunk_id TEXT PRIMARY KEY,
       artifact_id TEXT NOT NULL REFERENCES cloud_index_records(artifact_id) ON DELETE CASCADE,
       content TEXT NOT NULL,
       start_line INTEGER,
       end_line INTEGER,
       char_count INTEGER,
       token_estimate INTEGER,
       ir_pairs JSONB,
       created_at TIMESTAMP NOT NULL
     );

     CREATE TABLE IF NOT EXISTS cloud_embeddings (
       artifact_id TEXT NOT NULL REFERENCES cloud_index_records(artifact_id) ON DELETE CASCADE,
       engine TEXT NOT NULL,
       vector vector(500),  -- pgvector type, dimension 500 (matches TF-IDF vocab_size)
       dimension INTEGER NOT NULL,
       created_at TIMESTAMP NOT NULL,
       PRIMARY KEY (artifact_id, engine)
     );

     CREATE INDEX IF NOT EXISTS idx_cloud_embeddings_vector
       ON cloud_embeddings USING ivfflat (vector vector_cosine_ops)
       WITH (lists = 100);
     ```

4. **`sync_to_cloud(artifact_id: str) -> bool`**
   - If conn is None: return False
   - Fetch IndexRecord from local storage
   - Fetch chunks from local storage
   - Fetch embeddings from local storage
   - Upsert into Postgres (3 transactions):
     1. UPSERT cloud_index_records (ON CONFLICT DO UPDATE)
     2. DELETE old chunks, INSERT new chunks
     3. DELETE old embeddings, INSERT new embeddings (convert vector to pgvector format)
   - Return True on success, False on error

5. **`sync_all() -> dict`**
   - Get all records: `storage.list_all()`
   - For each record: call `sync_to_cloud(artifact_id)`
   - Return stats: `{"synced": success_count, "failed": fail_count}`

6. **`close() -> None`**
   - If conn: close connection

**Helper function:**

7. **`_vector_to_pgvector(vector: list[float]) -> str`**
   - Convert Python list to pgvector string format: `"[0.1, 0.2, 0.3, ...]"`
   - Return string

### test_cloud_sync.py (8+ tests — use testcontainers Postgres)

**Test setup:**
- Use `testcontainers` library to spawn Postgres container with pgvector extension
- Create CloudSyncService with test Postgres URL
- Create test IndexRecord + chunks + embeddings

**Test cases:**
- Test `ensure_schema()` creates 3 tables and vector extension
- Test `sync_to_cloud()` inserts record + chunks + embeddings
- Test `sync_to_cloud()` upserts (update existing record)
- Test `sync_all()` syncs multiple records
- Test cascade delete (delete cloud_index_records → verify chunks + embeddings deleted)
- Test IVFFlat index exists on embeddings.vector
- Test `_vector_to_pgvector()` converts list to string correctly
- Test cloud sync disabled (db_url=None) → logs warning, returns False

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/test_markdown_exporter.py tests/hivenode/rag/indexer/test_cloud_sync.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same markdown format, same Postgres schema with pgvector as platform/efemera
- [ ] TDD: tests written first
- [ ] 14+ tests total (6 markdown + 8 cloud sync)
- [ ] Cloud sync uses environment variable `HIVE_CLOUD_DB_URL` (default None → disabled)
- [ ] Markdown default directory: `.deia/index/` NOT `.shiftcenter/index/`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-116-RESPONSE.md`

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
