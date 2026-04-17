# RAG Pipeline Port — Task Decomposition

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-14
**Briefing:** BRIEFING-PORT-RAG-PIPELINE

---

## Summary

I have read:
- SPEC-PORT-RAG-001-rag-pipeline-port.md (516 lines)
- Existing hivenode RAG files (engine.py, routes.py, chunkers.py, embedder.py, schemas.py — 1,098 lines)
- Source repo structure (4,558 lines across 18 files in 4 modules)

**Scope:** Port 18 files from `platform/efemera/src/efemera/` to `hivenode/rag/` and `hivenode/entities/`. This adds production-grade indexing, entity profiling, BOK enrichment, and LLM synthesis to the existing RAG skeleton.

**Decomposition:** 10 tasks across 6 waves (matching briefing guidance + dependency graph).

**Dispatch order:** AFTER Shell Chrome bees are dispatched (per briefing instruction).

---

## Wave 1: Indexer Data Model + Foundation (3 tasks)

### TASK-110: Indexer Models + Scanner
**Model:** Sonnet (data model is comprehensive, scanner has nuanced file type detection)
**Lines:** 343 (models.py 179 + scanner.py 164)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_scanner.py`

**Deliverables:**
- 11 Pydantic models (ArtifactType, StorageTier, IRStatus enums + 8 metadata models + IndexRecord)
- Scanner with file type detection (9 types: CODE, PHASE_IR, ADR, SPEC, DOCUMENT, etc.)
- `scan()` iterator yields (Path, ArtifactType)
- `_is_phase_ir_file()` detects PHASE-IR JSON by keys
- Skip 12 directories (node_modules, .git, __pycache__, etc.)
- Tests: 15+ covering all ArtifactTypes, skip logic, PHASE-IR detection

---

### TASK-111: Enhanced Chunkers (AST Python + JS + PHASE-IR + ADR + SPEC)
**Model:** Sonnet (AST chunking is algorithmic, must preserve IR pair tracking)
**Lines:** 324 (chunker.py — extends existing chunkers.py)
**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py` (extend, NOT replace)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_enhanced_chunkers.py`

**Deliverables:**
- Extend `CodeChunk` dataclass with `ir_pairs: list[dict] = field(default_factory=list)`
- `_chunk_python()` — AST-based per function/method/class (REPLACES current regex approach)
- `_chunk_javascript()` — regex + brace-matching for JS/TS scope
- `_chunk_phase_ir()` — JSON per-node chunking for PHASE-IR v2.0
- `_chunk_adr()` — per "## Decision N" sections
- `_chunk_spec()` — per ## heading (capability claims)
- `_chunk_by_headings()` — generic heading-based (refactor from current markdown chunker)
- `_create_chunk()` — factory with char count + token estimate (len // 4)
- IR pair tracking: extract `# IR: <intent> → <result>` comments from Python docstrings
- Tests: 20+ covering all new chunkers, IR pair extraction, edge cases (empty files, syntax errors)

---

### TASK-112: TF-IDF Embedder
**Model:** Haiku (TF-IDF is algorithmic but straightforward)
**Lines:** 181 (embedder.py — extends existing)
**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\embedder.py` (ADD TFIDFEmbedder class)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_tfidf_embedder.py`

**Deliverables:**
- `class TFIDFEmbedder` with `fit()`, `transform()`, `fit_transform()`
- Vocabulary: top-N by document frequency (default N=500)
- TF = term_freq / total_terms
- IDF = log(corpus_size / document_frequency)
- L2 normalization on output vector
- Stopwords filtered (the, a, an, is, are, etc. — 25 common words)
- `create_embedding_record(vector) -> EmbeddingRecord` (matching models.py schema)
- Tests: 8+ covering fit, transform, L2 norm, empty corpus, single doc

---

## Wave 2: Indexer Storage + Service (2 tasks)

**Dependencies:** Requires TASK-110 (models), TASK-111 (chunkers), TASK-112 (embedder)

### TASK-113: Indexer Storage (SQLite)
**Model:** Sonnet (storage is 463 lines, complex schema with 3 tables + JSON fields)
**Lines:** 463 (storage.py)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_storage.py`

**Deliverables:**
- `class IndexStorage` — SQLite persistence
- 3 tables: `index_records` (PK: artifact_id), `chunks` (FK to index_records), `embeddings` (composite PK: artifact_id + engine)
- JSON columns: keywords, engines, ir_summary, ccc, reliability, relevance, staleness, provenance
- Indexes on: artifact_type, storage_tier, path
- CRUD: `insert()`, `get_by_id()`, `get_by_path()`, `update()`, `delete()`, `list_all()`
- `update()` = delete old + re-insert (cascade delete chunks + embeddings)
- `compute_content_hash(content) -> str` standalone function (SHA256)
- Default DB path: `~/hive/local/index.db` (NOT ~/.shiftcenter — use hive paths)
- Tests: 12+ covering insert, get, update, delete, list with filters, cascade delete, content hash

---

### TASK-114: Indexer Service (Two-Pass Orchestrator)
**Model:** Sonnet (orchestration logic, two-pass indexing, event emission)
**Lines:** 301 (indexer_service.py)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_indexer_service.py`

**Deliverables:**
- `class IndexerService(repo_path, db_session, storage, actor_id, node_id)`
- `index_repository() -> dict` — two-pass: scan all → fit TF-IDF → index each
- `index_file(file_path) -> Optional[str]` — index single file (returns artifact_id)
- `_index_single_file()` — pipeline: read → chunk → embed → compute IR summary → create IndexRecord → store → emit event
- `_compute_ir_summary(chunks) -> IRSummary` — count IR pairs by status (verified/failed/untested)
- `_emit_context_indexed_event()` — append to hivenode Event Ledger (see `hivenode/events/ledger.py` for schema)
- CCC estimation: 10ms clock, $0.0001 coin, 0.000002kg carbon per file
- Tests: 10+ covering two-pass indexing, single file, IR summary computation, event emission, errors (missing files, syntax errors)

---

## Wave 3: Indexer Reliability + Metrics + Sync (3 tasks)

**Dependencies:** Requires TASK-113 (storage), TASK-114 (service)

### TASK-115: Reliability Calculator + Metrics Updater
**Model:** Sonnet (reliability formulas are nuanced, metrics updater has async event polling)
**Lines:** 651 (reliability.py 296 + metrics_updater.py 355)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\reliability.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\metrics_updater.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_reliability.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_metrics_updater.py`

**Deliverables (reliability.py):**
- `class ReliabilityCalculator`
- `calculate_reliability() -> float` — 0.5×LLM_used + 0.3×helpful + 0.2×IR_verification_rate
- `calculate_availability() -> float` — success_loads / total_loads
- `calculate_latency() -> int` — avg duration_ms (last 100 loads)
- `calculate_cost() -> CCCMetadata` — sum clock/coin/carbon from retrieval events
- `is_canon() -> bool` — retrieval_count > 1000 AND reliability > 0.90 AND verification_rate > 0.80
- `update_reliability_metrics()` — recalculate + update storage
- Tests: 8+ covering all formulas, canon detection, edge cases (zero loads, no feedback)

**Deliverables (metrics_updater.py):**
- `class MetricsUpdater(db, index_storage, poll_interval_seconds)`
- `start()` — async event processing loop
- `stop()` — graceful shutdown
- `_process_new_events()` — poll Event Ledger for 5 event types
- Event handlers: `_handle_context_loaded()`, `_handle_ir_pair_verified()`, `_handle_ir_pair_failed()`, `_handle_human_responded()`
- `_recalculate_ir_summary()` — recount IR pairs by status after verification events
- Increment: retrieval_count, llm_used/ignored, helpful/not_helpful feedback
- Tests: 10+ covering all event types, increments, IR recalculation, poll loop (use mock events)

---

### TASK-116: Markdown Exporter + Cloud Sync
**Model:** Sonnet (cloud sync uses psycopg2 + pgvector, complex upsert logic)
**Lines:** 514 (markdown_exporter.py 195 + cloud_sync.py 319)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\markdown_exporter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\cloud_sync.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_markdown_exporter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_cloud_sync.py`

**Deliverables (markdown_exporter.py):**
- `class MarkdownExporter(markdown_dir=None)` — default: `.deia/index/`
- `export_to_markdown(record: IndexRecord) -> str` — format as markdown
- Sections: Title, Keywords, IR Pairs (✓✗~? status symbols), Embedding Engines, CCC, Reliability, Staleness, Content Preview
- `write_markdown_file(artifact_id, storage) -> Path` — write to disk
- `sync_all_to_markdown(storage) -> list[Path]` — batch export
- Tests: 6+ covering markdown format, all sections, write to disk, sync all

**Deliverables (cloud_sync.py):**
- `class CloudSyncService(storage, exporter, db_url=None)` — Postgres sync
- `connect()` — psycopg2 connection
- `ensure_schema()` — CREATE EXTENSION vector; 3 tables matching SQLite schema; IVFFlat index on embeddings
- `sync_to_cloud(artifact_id)` — upsert main + chunks + embeddings (3 transactions)
- `sync_all() -> dict` — batch sync; return {synced: count, failed: count}
- Environment: `HIVE_CLOUD_DB_URL` (default: None → skip cloud sync)
- Tests: 8+ covering schema creation, single sync, batch sync, upsert idempotency (use testcontainers Postgres)

---

### TASK-117: Sync Daemon
**Model:** Haiku (daemon is straightforward orchestration)
**Lines:** 267 (sync_daemon.py)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\sync_daemon.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_sync_daemon.py`

**Deliverables:**
- `class SyncPolicy(str, Enum): IMMEDIATE, BATCHED, MANUAL`
- `class SyncDaemon(storage, exporter, cloud_sync, config)`
- `start()` — spawn daemon thread
- `stop()` — graceful shutdown
- `on_context_indexed(artifact_id)` — route by policy (IMMEDIATE→sync now, BATCHED→queue, MANUAL→skip)
- `force_sync_all()` — override policy, sync everything
- `get_status() -> dict` — running, policy, pending_count, last_sync_time
- `create_daemon_from_env() -> SyncDaemon` factory — read SYNC_POLICY, SYNC_BATCH_INTERVAL, SYNC_ENABLE_CLOUD, SYNC_ENABLE_MARKDOWN
- Tests: 6+ covering all policies, batch timer, force sync, status, env factory

---

## Wave 4: Entity Embeddings (3 tasks)

**Dependencies:** Independent of indexer (can run parallel with Wave 2/3)

### TASK-118: Voyage AI Client + Bot Embeddings
**Model:** Haiku (Voyage client is simple HTTP, bot embeddings are cache + drift logic)
**Lines:** 423 (voyage_embedding.py 142 + embeddings.py 281)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\voyage_embedding.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\embeddings.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_voyage_embedding.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_embeddings.py`

**Deliverables (voyage_embedding.py):**
- `get_embedding(text, model=None) -> list[float]` — POST to Voyage API
- URL: `https://api.voyageai.com/v1/embeddings`
- Model: `voyage-2` (default)
- Env: `VOYAGE_API_KEY` — if not set, WARNING + fallback to `hash_embedding()` (dummy hash-based vector)
- In-memory cache (LRU, max 1000 entries)
- Error handling: timeout (30s), ConnectionError, HTTPError, unexpected response
- `clear_cache()` — for tests
- Tests: 6+ covering API call (mocked), cache hit/miss, fallback, errors

**Deliverables (embeddings.py):**
- ORM: `class BotEmbeddingStore(Base)` — SQLAlchemy table (id, entity_id unique, system_prompt_hash, embedding blob, model_version, created_at)
- `get_or_compute_bot_embedding(entity_id, system_prompt, db) -> list[float]` — cache by SHA256(prompt)
- `compute_pi_bot_full(entity_id, domain, system_prompt, task_text=None, db=None) -> tuple` — pi = (domain_sim + task_sim)/2 if task_text else domain_sim
- `check_bot_drift(entity_id, new_system_prompt, threshold=0.3, db=None) -> dict` — cosine similarity; drifted if < (1 - threshold)
- `register_bot_profile(entity_id, system_prompt, model_id=None, db=None) -> dict` — create/update cache
- Tests: 8+ covering cache, pi computation, drift detection, DB persistence

---

### TASK-119: Entity Vector System (Alpha, Sigma, Rho, Pi)
**Model:** Sonnet (vectors.py is 686 lines, MUST split into two files per Rule 4)
**Lines:** 686 (vectors.py → split into `vectors_core.py` 350 + `vectors_compute.py` 336)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_core.py` (data model + helpers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_compute.py` (5 compute functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_vectors.py`

**Deliverables (vectors_core.py — ~350 lines):**
- `_fetch_events()` — 30-day decay window query
- `_get_sla_target()` — SLA lookup with 3.6M ms fallback
- `_get_entity_prompt()` — fetch from component store
- `_upsert_profile()` — DB upsert for EntityProfile table
- `_upsert_component()` — DB upsert for EntityComponent table
- `get_entity_vector()` — cold-start cascade (local → domain avg → neutral 0.5)
- `compute_global_vector()` — confidence-weighted average across domains
- Confidence formula: `(sample_size / (sample_size + 10)) × source_multiplier`
- Source multipliers: computed=1.0, observed=1.0, declared=0.6, imported=0.5

**Deliverables (vectors_compute.py — ~336 lines):**
- `compute_alpha()` — autonomy: internal_signals / total_signals (30-day decay)
- `compute_sigma()` — quality: outcome × (1 - rework); rework = fraction with failure→completion sequences
- `compute_rho()` — reliability: tasks meeting SLA / total attempts
- `compute_pi_bot()` — bot preference: cosine(prompt_embedding, archetype_embedding)
- `compute_pi_human()` — human preference: observed (high-alpha) then declared fallback
- `recalculate_entity()` — full recalculation of all vectors; upsert profiles; append history
- Tests: 20+ covering all 5 vectors with known inputs, cold-start cascade, domain averages, edge cases (zero events, no SLA, rework detection)

---

### TASK-120: Entity Embedding Routes
**Model:** Haiku (thin FastAPI routes)
**Lines:** 129 (embedding_routes.py)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_routes.py`

**Deliverables:**
- Router prefix: `/api/bots`, tags: ["bot-embeddings"]
- `POST /{entity_id}/register` → `register_bot_profile()`
- `GET /{entity_id}/pi/{domain}?task_text=...` → `compute_pi_bot_full()`
- `POST /{entity_id}/check-drift` → `check_bot_drift()`
- Auth: `verify_jwt_or_local()` (local bypasses auth)
- Tests: 6+ covering all 3 endpoints, auth bypass, 401 on missing JWT (cloud mode)

---

## Wave 5: BOK + Synthesizer (1 task)

**Dependencies:** Independent (can run parallel with all other waves)

### TASK-121: BOK Services + RAG Synthesizer
**Model:** Haiku (BOK is simple keyword search, synthesizer is HTTP client)
**Lines:** 264 (bok/ 142 + synthesizer.py 122)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\embedding_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\rag_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\synthesizer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\bok\test_bok_services.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_synthesizer.py`

**Deliverables (bok/embedding_service.py):**
- `generate_embedding(text) -> list[float]` — POST to Voyage AI with `voyage-large-2`
- Env: `VOYAGE_API_KEY` required
- Tests: 2+ (mocked API)

**Deliverables (bok/rag_service.py):**
- `search_bok(query, db, limit=5) -> list[BokEntry]` — keyword search (split on whitespace, LIKE match on title + content)
- `format_bok_for_prompt(entries) -> str` — markdown block: "## Relevant Knowledge (from BOK)"
- `enrich_prompt(base_prompt, query, db, max_entries=3) -> tuple` — search + format + append
- Tests: 4+ covering search, format, enrichment, no results

**Deliverables (synthesizer.py):**
- `class Synthesizer(api_key=None, model=None, base_url=None)` — read from env: ANTHROPIC_API_KEY, RAG_MODEL (default haiku)
- `answer(query, chunks) -> dict` — build sources from chunks; format context; POST to Claude /messages
- Return: {answer, sources, model_used, cost_tokens, cost_usd, duration_ms}
- `_format_context(chunks) -> str` — "--- Chunk N: path (L-L, score=X) ---\ncontent"
- Token cost: `(input_tokens × 0.001 + output_tokens × 0.005) / 1000`
- Tests: 6+ covering answer generation (mocked Claude API), context formatting, cost calculation, errors

---

## Wave 6: Integration + Routes (1 task)

**Dependencies:** Requires ALL prior tasks (integrates everything)

### TASK-122: RAG Integration + Route Registration
**Model:** Sonnet (integration wiring, route registration, backward compatibility)
**Lines:** ~150 (modifications across 3 files + new route file)
**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (register new routers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\engine.py` (add factory for IndexerService + ReliabilityCalculator + Synthesizer)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py` (extend with indexer endpoints)
**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\routes.py` (indexer-specific routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\routes.py` (BOK routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_integration.py`

**Deliverables:**
- **New indexer routes** (in `hivenode/rag/indexer/routes.py`):
  - `POST /rag/index-repo` → `IndexerService.index_repository()`
  - `POST /rag/index-file` → `IndexerService.index_file()`
  - `GET /rag/index/{artifact_id}` → `IndexStorage.get_by_id()`
  - `GET /rag/index` → `IndexStorage.list_all()`
  - `POST /rag/sync/{artifact_id}` → `CloudSyncService.sync_to_cloud()`
  - `POST /rag/sync-all` → `CloudSyncService.sync_all()`
  - `GET /rag/sync/status` → `SyncDaemon.get_status()`

- **New BOK routes** (in `hivenode/rag/bok/routes.py`):
  - `GET /rag/bok/search?query=...` → `search_bok()`
  - `POST /rag/bok/enrich` → `enrich_prompt()`

- **Entity routes** (already in hivenode/entities/routes.py from TASK-120):
  - `POST /api/bots/{entity_id}/register`
  - `GET /api/bots/{entity_id}/pi/{domain}`
  - `POST /api/bots/{entity_id}/check-drift`

- **Main.py router registration:**
  ```python
  from hivenode.rag.indexer.routes import router as indexer_router
  from hivenode.rag.bok.routes import router as bok_router
  from hivenode.entities.routes import router as entities_router

  app.include_router(indexer_router, prefix="/rag", tags=["indexer"])
  app.include_router(bok_router, prefix="/rag", tags=["bok"])
  app.include_router(entities_router, prefix="/api", tags=["entities"])
  ```

- **Engine.py extensions:**
  - Add factory methods: `get_indexer_service()`, `get_reliability_calculator()`, `get_synthesizer()`
  - Wire IndexStorage, SyncDaemon (singleton pattern, lazy init)

- **Backward compatibility:**
  - Existing `/rag/index`, `/rag/ingest-chat`, `/rag/search` routes UNCHANGED
  - New indexer routes coexist with existing simple index route

- **Integration test:**
  - End-to-end: index 3 files (Python, TS, Markdown) → query → synthesize answer with sources
  - Verify: IndexRecord created, chunks embedded, search works, synthesizer returns answer
  - Test count: 8+ covering full pipeline, BOK enrichment, entity vectors, errors

---

## Test Summary

| Task | Unit Tests | Integration Tests | Total |
|---|---|---|---|
| TASK-110 | 15 | 0 | 15 |
| TASK-111 | 20 | 0 | 20 |
| TASK-112 | 8 | 0 | 8 |
| TASK-113 | 12 | 0 | 12 |
| TASK-114 | 10 | 0 | 10 |
| TASK-115 | 18 | 0 | 18 |
| TASK-116 | 14 | 0 | 14 |
| TASK-117 | 6 | 0 | 6 |
| TASK-118 | 14 | 0 | 14 |
| TASK-119 | 20 | 0 | 20 |
| TASK-120 | 6 | 0 | 6 |
| TASK-121 | 12 | 0 | 12 |
| TASK-122 | 0 | 8 | 8 |
| **TOTAL** | **155** | **8** | **163** |

---

## Dependency Graph

```
Wave 1 (parallel):
  TASK-110 (models + scanner)
  TASK-111 (enhanced chunkers) — extends existing chunkers.py
  TASK-112 (TF-IDF embedder) — extends existing embedder.py

Wave 2 (sequential after Wave 1):
  TASK-113 (storage) ← depends on TASK-110
  TASK-114 (service) ← depends on TASK-110, TASK-111, TASK-112, TASK-113

Wave 3 (sequential after Wave 2):
  TASK-115 (reliability + metrics) ← depends on TASK-113, TASK-114
  TASK-116 (markdown + cloud sync) ← depends on TASK-113
  TASK-117 (sync daemon) ← depends on TASK-116

Wave 4 (parallel, independent):
  TASK-118 (Voyage + bot embeddings)
  TASK-119 (entity vectors) ← depends on TASK-118
  TASK-120 (entity routes) ← depends on TASK-118, TASK-119

Wave 5 (parallel, independent):
  TASK-121 (BOK + synthesizer)

Wave 6 (final integration):
  TASK-122 (integration) ← depends on ALL prior tasks
```

---

## Parallelization Strategy

**Round 1:** Dispatch TASK-110, TASK-111, TASK-112 (Wave 1 — all independent)
**Round 2:** Wait for Wave 1 → dispatch TASK-113
**Round 3:** Wait for TASK-113 → dispatch TASK-114
**Round 4:** Wait for TASK-114 → dispatch TASK-115, TASK-116 in parallel
**Round 5:** Wait for TASK-116 → dispatch TASK-117
**Round 6:** (parallel with Rounds 2-5) Dispatch TASK-118
**Round 7:** Wait for TASK-118 → dispatch TASK-119
**Round 8:** Wait for TASK-119 → dispatch TASK-120
**Round 9:** (parallel with all) Dispatch TASK-121
**Round 10:** Wait for ALL → dispatch TASK-122

**Max concurrent:** 3 bees (Rounds 1, 4)
**Total bees:** 13

---

## File Count

**New files:** 46
**Modified files:** 3
**Total files touched:** 49

**New production code files:** 22
**New test files:** 24
**Total lines added:** ~4,700

---

## Cost Estimate

| Task | Model | Est. Clock (min) | Est. Cost (USD) |
|---|---|---|---|
| TASK-110 | Sonnet | 15 | $1.20 |
| TASK-111 | Sonnet | 18 | $1.50 |
| TASK-112 | Haiku | 8 | $0.30 |
| TASK-113 | Sonnet | 20 | $1.60 |
| TASK-114 | Sonnet | 18 | $1.50 |
| TASK-115 | Sonnet | 25 | $2.00 |
| TASK-116 | Sonnet | 22 | $1.80 |
| TASK-117 | Haiku | 10 | $0.40 |
| TASK-118 | Haiku | 12 | $0.50 |
| TASK-119 | Sonnet | 30 | $2.50 |
| TASK-120 | Haiku | 8 | $0.30 |
| TASK-121 | Haiku | 12 | $0.50 |
| TASK-122 | Sonnet | 15 | $1.20 |
| **TOTAL** | — | **213 min (3.6 hrs)** | **$15.30** |

---

## Constraints Verified

✅ No file over 500 lines (TASK-119 splits vectors.py into 2 files)
✅ TDD: tests first for every module
✅ No stubs (spec mandates full port)
✅ All file paths absolute
✅ PORT not rewrite (briefing rule)
✅ Algorithms preserved (TF-IDF, cosine sim, entity formulas, decay windows)
✅ Data model complete (all IndexRecord fields, all entity vector components)

---

## Dispatch Order

**Per briefing instruction:** "Do Shell first. Start RAG after Shell bees are dispatched."

I will hold these task files and await your approval. Once Shell Chrome bees are dispatched, I will dispatch RAG bees in the wave order above.

---

## Next Steps

1. **Q33NR reviews** this decomposition
2. **Q33NR approves** or requests changes
3. **Q33N writes** 13 task files (TASK-110 through TASK-122) to `.deia/hive/tasks/`
4. **Q33N waits** for Shell Chrome dispatch to complete
5. **Q33N dispatches** RAG bees in wave order (after Q33NR approval)

Ready for your review.
