# SPEC-PORT-RAG-001: RAG Pipeline Full Port

**Status:** Draft
**Priority:** P0
**Source:** `platform/efemera/src/efemera/` (indexer/, entities/, bok/, rag/synthesizer.py)
**Target:** `shiftcenter/hivenode/rag/` (extend existing) + `shiftcenter/hivenode/entities/` (new)
**Rule:** PORT, NOT REWRITE. Same classes, same methods, same algorithms. Acceptable changes: import paths, SQLAlchemy session handling to match hivenode patterns, env var names.

---

## Mandate

The current `hivenode/rag/` has the skeleton (engine, routes, chunkers, embedder, schemas). What's missing is everything that makes it production-grade. Every module listed below MUST be ported from the old repo. The port must preserve the original classes, methods, algorithms, and data models.

Acceptable changes:
1. Import paths updated to `hivenode.*`
2. SQLAlchemy session management adapted to hivenode's async patterns (if applicable)
3. Environment variable names prefixed with `HIVE_` if needed for consistency
4. Pydantic v1 → v2 if hivenode uses v2
5. `events.ledger` references → hivenode's Event Ledger equivalent

Unacceptable changes:
- Removing classes or methods
- Changing algorithms (TF-IDF, cosine similarity, decay windows, confidence formulas)
- Simplifying the data model (dropping fields from IndexRecord, EntityProfile, etc.)
- Skipping files
- Replacing the entity vector system with "something simpler"

---

## Module 1: Indexer Service (3,060 lines → `hivenode/rag/indexer/`)

Port from `efemera/src/efemera/indexer/` to `hivenode/rag/indexer/`.

### 1.1 models.py (179 lines)

**Port the full data model:**

```python
# Enums
class ArtifactType(str, Enum):
    CODE, PHASE_IR, ADR, SPEC, DOCUMENT, CONVERSATION_TURN,
    CONVERSATION_SEGMENT, HUMAN_INPUT, EXTERNAL

class StorageTier(str, Enum):
    EDGE, CLOUD, REMOTE_NODE, ARCHIVE

class IRStatus(str, Enum):
    VERIFIED, UNVERIFIED, FAILED, UNTESTED

# Pydantic Models — ALL fields required
class IRPair          # intent, result, status, test_ref, verified_at, verified_by
class Chunk           # content, char_count, token_estimate, start_line, end_line, ir_pairs
class EmbeddingRecord # vector, engine, created_at
class CCCMetadata     # clock_ms, coin_usd_per_load, carbon_kg_per_load, token_estimate, model_for_cost
class ReliabilityMetadata  # availability, hit_rate, last_load_success/failure, failure_count, consecutive_failures
class RelevanceMetadata    # retrieval_count, user_feedback_helpful/not_helpful, llm_used/ignored, is_canon
class StalenessMetadata    # content_hash, last_modified, last_indexed, dependent_code_changed_since, stale_flag
class ProvenanceMetadata   # created_by, parent_artifact_id, parent_conversation_id, conversation_snapshot_id
class IRSummary            # total, verified, failed, untested, verification_rate
class IndexRecord          # artifact_id, type, path, storage_tier, content_preview, chunks, embeddings, all metadata, timestamps
```

**Do NOT simplify this model.** Every field exists for a reason in the harness spec.

---

### 1.2 scanner.py (164 lines)

**Port the file classifier:**
- `Scanner(root_path)` — validate repo root
- `scan() -> Iterator[tuple[Path, ArtifactType]]` — walk tree, classify files
- `_detect_type(file_path) -> ArtifactType | None` — extension + filename pattern matching
- `_is_phase_ir_file(file_path) -> bool` — check JSON for "nodes"/"edges" keys
- `scan_single(file_path) -> ArtifactType | None` — classify one file

**Detection rules:**
- `.py, .js, .jsx, .ts, .tsx` → CODE
- `.json` with nodes/edges → PHASE_IR
- `ADR-*.md` → ADR
- `SPEC-*.md` → SPEC
- Other `.md` → DOCUMENT

**Skip dirs:** node_modules, .git, __pycache__, .venv, venv, dist, build, .next, coverage, .pytest_cache, .mypy_cache

---

### 1.3 chunker.py (324 lines)

**Port the type-specific chunker** (extends existing `hivenode/rag/chunkers.py`):

The old chunker has type-specific strategies that the current chunkers.py lacks:

- `_chunk_python(content)` — **AST-based** chunking per function/method/class; tracks IR pairs
- `_chunk_javascript(content)` — **regex-based** with brace-matching for JS/TS scope detection
- `_chunk_phase_ir(content)` — **JSON per-node** chunking for PHASE-IR v2.0 format
- `_chunk_adr(content)` — per "## Decision N" sections
- `_chunk_spec(content)` — per ## heading (capability claims)
- `_chunk_document(content)` — per ## sections
- `_chunk_by_headings(content, heading_level)` — generic heading-based
- `_create_chunk(content, start_line, end_line)` — factory with char count + token estimate (`len(content) // 4`)

**Critical:** The AST-based Python chunker and IR pair tracking do NOT exist in the current chunkers.py. They must be ported.

---

### 1.4 embedder.py (181 lines)

**Port the TF-IDF embedder** (extends existing `hivenode/rag/embedder.py`):

```python
class TFIDFEmbedder:
    def __init__(self, max_features=500)
    def fit(self, documents: list[str]) -> None        # Build vocab, compute IDF
    def transform(self, text: str) -> list[float]      # Compute TF-IDF vector, L2 normalize
    def fit_transform(self, documents, current_doc) -> list[float]
    def create_embedding_record(self, vector) -> EmbeddingRecord
    def _tokenize(self, text) -> list[str]              # Lowercase, split, filter stopwords
```

**Algorithms:**
- TF = term_freq / total_terms
- IDF = log(corpus_size / document_frequency)
- Vocabulary = top-N by document frequency
- L2 normalization on output vector

---

### 1.5 storage.py (463 lines)

**Port the SQLite index storage:**

```python
class IndexStorage:
    def __init__(self, db_path=None)          # Default ~/hive/local/index.db
    def _create_schema(self)                   # 3 tables: index_records, chunks, embeddings + indexes
    def insert(self, record: IndexRecord)      # Serialize JSON fields; insert main + chunks + embeddings
    def get_by_id(self, artifact_id) -> Optional[IndexRecord]
    def get_by_path(self, path) -> Optional[IndexRecord]
    def update(self, record)                   # Delete old + re-insert
    def delete(self, artifact_id)              # Cascade delete
    def list_all(self, artifact_type=None) -> list[IndexRecord]
    def close(self)
```

**Standalone:** `compute_content_hash(content) -> str` — SHA256 hex digest

**Schema (3 tables):**
- `index_records`: artifact_id PK, type, path, tier, preview, char/token counts, JSON columns for keywords, engines, ir_summary, ccc, reliability, relevance, staleness, provenance, timestamps
- `chunks`: chunk_id PK, artifact_id FK, content, counts, ir_pairs_json
- `embeddings`: (artifact_id, engine) PK, vector_json, created_at
- Indexes on: artifact_type, storage_tier, path

---

### 1.6 indexer_service.py (301 lines)

**Port the indexing orchestrator:**

```python
class IndexerService:
    def __init__(self, repo_path, db_session, storage, actor_id, node_id)
    def index_repository(self) -> dict[str, int]    # Two-pass: scan all → fit TF-IDF → index each
    def index_file(self, file_path) -> Optional[str] # Index single file
    def _index_single_file(self, file_path, artifact_type) -> str
        # Pipeline: read → chunk → embed → compute IR summary → create record → store → emit event
    def _compute_ir_summary(self, chunks) -> IRSummary
    def _emit_context_indexed_event(self, record, is_reindex) -> None
        # Emit CONTEXT_INDEXED per Gate G1
```

**Key:** Two-pass indexing — first pass collects corpus for TF-IDF fit, second pass indexes each file. CCC estimation: 10ms clock, $0.0001 coin, 0.000002kg carbon per file.

---

### 1.7 reliability.py (296 lines)

**Port the four-factor reliability model:**

```python
class ReliabilityCalculator:
    def calculate_reliability(self, artifact_id) -> float
        # 0.5 × (llm_used/(llm_used+llm_ignored)) + 0.3 × helpful_feedback + 0.2 × ir_verification_rate
    def calculate_availability(self, artifact_id) -> float
        # success_loads / total_loads
    def calculate_latency(self, artifact_id, storage_tier=None) -> int
        # Average duration_ms (last 100 loads)
    def calculate_cost(self, artifact_id) -> CCCMetadata
    def is_canon(self, artifact_id) -> bool
        # retrieval_count > 1000 AND reliability > 0.90 AND verification_rate > 0.80
    def update_reliability_metrics(self, artifact_id) -> None
```

---

### 1.8 metrics_updater.py (355 lines)

**Port the async metrics processor:**

```python
class MetricsUpdater:
    def __init__(self, db, index_storage, poll_interval_seconds)
    async def start(self) -> None                    # Run event processing loop
    def stop(self) -> None
    async def _process_new_events(self) -> None      # Poll for 5 event types
    def _handle_context_loaded(self, event, record)  # Increment retrieval_count, llm_used/ignored
    def _handle_ir_pair_verified(self, event, record) # Update chunk IR pair status
    def _handle_ir_pair_failed(self, event, record)
    def _handle_human_responded(self, event, record) # Increment helpful/not_helpful feedback
    def _recalculate_ir_summary(self, record)        # Recount all IR pairs by status
```

**Event types watched:** CONTEXT_LOADED, CONTEXT_LOAD_FAILED, IR_PAIR_VERIFIED, IR_PAIR_FAILED, HUMAN_RESPONDED

---

### 1.9 markdown_exporter.py (195 lines)

**Port the dual-storage exporter:**

```python
class MarkdownExporter:
    def __init__(self, markdown_dir=None)        # Default .deia/index/
    def export_to_markdown(self, record) -> str  # Format record as markdown
    def write_markdown_file(self, artifact_id, storage) -> Path
    def sync_all_to_markdown(self, storage) -> list[Path]
```

**Sections:** Title, Keywords, IR Pairs (with status symbols ✓✗~?), Embedding Engines, CCC, Reliability, Staleness, Content Preview

---

### 1.10 cloud_sync.py (319 lines)

**Port the SQLite→Postgres sync:**

```python
class CloudSyncService:
    def __init__(self, storage, exporter, db_url=None)
    def connect(self) -> None                       # psycopg2
    def ensure_schema(self) -> None                 # CREATE EXTENSION vector; matching tables
    def sync_to_cloud(self, artifact_id) -> None    # Upsert main + chunks + embeddings
    def sync_all(self) -> dict[str, int]            # Batch sync; return synced/failed counts
```

**Port note:** Cloud schema uses pgvector for embeddings. IVFFlat index for cosine similarity search.

---

### 1.11 sync_daemon.py (267 lines)

**Port the background sync orchestrator:**

```python
class SyncPolicy(str, Enum): IMMEDIATE, BATCHED, MANUAL

class SyncDaemon:
    def __init__(self, storage, exporter, cloud_sync, config)
    def start(self) -> None                          # Spawn daemon thread
    def stop(self) -> None
    def on_context_indexed(self, artifact_id) -> None # Route by policy
    def force_sync_all(self) -> dict                 # Override policy, sync everything
    def get_status(self) -> dict                     # running, policy, pending_count, etc.
```

**Factory:** `create_daemon_from_env() -> SyncDaemon` reads SYNC_POLICY, SYNC_BATCH_INTERVAL, SYNC_ENABLE_CLOUD, SYNC_ENABLE_MARKDOWN

---

## Module 2: Entity Embeddings (1,234 lines → `hivenode/entities/`)

Port from `efemera/src/efemera/entities/` to `hivenode/entities/`.

### 2.1 vectors.py (686 lines)

**Port the full entity vector system. This is the core of entity profiling.**

**Vector computations (all must be ported):**

```python
def compute_alpha(entity_id, domain, db) -> tuple[float, float, int]
    # Autonomy: internal_signals / total_signals, 30-day decay

def compute_sigma(entity_id, domain, db) -> tuple[float, float, int]
    # Quality: sigma_outcome × (1 - sigma_rework)
    # sigma_outcome = avg outcome_score from completed tasks
    # sigma_rework = fraction of tasks with failure before completion

def compute_rho(entity_id, domain, db) -> tuple[float, float, int]
    # Reliability: tasks meeting SLA / total attempts
    # SLA from EntitySLAConfig, default 1 hour

def compute_pi_bot(entity_id, domain, db) -> tuple[float, float]
    # Bot preference: cosine(prompt_embedding, archetype_embedding) → [0,1]

def compute_pi_human(entity_id, domain, db) -> tuple[float, float, int, str]
    # Human preference: observed (high-alpha) then declared fallback

def compute_global_vector(entity_id, vector_type, db) -> tuple[float, float]
    # Confidence-weighted average across domains

def get_entity_vector(entity_id, domain, vector_type, db) -> tuple[float, float]
    # Cold-start cascade: local → domain defaults → neutral baseline

def recalculate_entity(entity_id, domain=None, db=None) -> dict
    # Full recalculation of all vectors; upsert profiles; append history
```

**Helper functions:**
- `_fetch_events(entity_id, domain, db, event_types, decay_days)` — 30-day window query
- `_get_sla_target(entity_id, domain, db)` — SLA lookup with 3.6M ms fallback
- `_get_entity_prompt(entity_id, domain, db)` — fetch prompt from component store
- `_upsert_profile(db, entity_id, domain, vector_type, value, confidence, sample_size)`
- `_upsert_component(db, entity_id, domain, component, value, sample_size, source)`

**Key algorithms — DO NOT CHANGE:**
- Confidence: `(sample_size / (sample_size + 10)) × source_multiplier`
- Source multipliers: computed=1.0, observed=1.0, declared=0.6, imported=0.5
- 30-day decay window for all event queries
- Cold-start cascade: 3-tier fallback (local → domain average → 0.5 neutral)
- Domain defaults: average of all entities in domain with confidence > 0.1
- Sigma rework: group events by task_id, detect failure→completion sequences

---

### 2.2 embeddings.py (281 lines)

**Port the bot embedding system:**

```python
# ORM
class BotEmbeddingStore(Base):
    # id, entity_id (unique), system_prompt_hash, embedding (LargeBinary),
    # embedding_model_version, created_at

# Functions
def get_or_compute_bot_embedding(entity_id, system_prompt, db) -> list[float]
    # Cache by prompt SHA256 hash; Voyage AI if key set, else hash_embedding fallback

def compute_pi_bot_full(entity_id, domain, system_prompt, task_text=None, db=None) -> tuple
    # pi = (domain_sim + task_sim) / 2 if task_text, else domain_sim
    # confidence = 0.8 if archetype.confidence > 0.0

def check_bot_drift(entity_id, new_system_prompt, threshold=0.3, db=None) -> dict
    # Compare old vs new embedding; drifted if similarity < (1 - threshold)
    # Returns: drifted, similarity, old_hash, new_hash

def register_bot_profile(entity_id, system_prompt, model_id=None, db=None) -> dict
    # Create/update cache entry; return registration metadata
```

---

### 2.3 voyage_embedding.py (142 lines)

**Port the Voyage AI client:**

```python
VOYAGE_API_URL = "https://api.voyageai.com/v1/embeddings"
_DEFAULT_MODEL = "voyage-2"

def get_embedding(text: str, model: Optional[str] = None) -> list[float]
    # If VOYAGE_API_KEY set: call API with in-memory cache
    # If not set: WARNING log, fallback to hash_embedding()

def clear_cache() -> None  # For tests
```

**Error handling:** Timeout (30s), ConnectionError, HTTPError (4xx/5xx), unexpected response structure

---

### 2.4 embedding_routes.py (129 lines)

**Port the FastAPI routes:**

```python
# Router prefix: /api/bots, tags: ["bot-embeddings"]

POST /{entity_id}/register     # register_bot_profile()
GET  /{entity_id}/pi/{domain}  # compute pi with optional ?task_text
POST /{entity_id}/check-drift  # check_bot_drift()
```

**Port note:** Integrate into hivenode's existing router registration pattern.

---

## Module 3: BOK Services (142 lines → `hivenode/rag/bok/`)

### 3.1 embedding_service.py (79 lines)

```python
def generate_embedding(text: str) -> List[float]
    # POST to Voyage AI with voyage-large-2 model
    # Requires VOYAGE_API_KEY env var
```

### 3.2 rag_service.py (65 lines)

```python
def search_bok(query, db, limit=5) -> list[BokEntry]
    # Keyword search: split on whitespace, LIKE match on title + content
    # Relevance = matched word count

def format_bok_for_prompt(entries) -> str
    # Markdown block: "## Relevant Knowledge (from BOK)"

def enrich_prompt(base_prompt, query, db, max_entries=3) -> tuple
    # search_bok() + format + append to prompt
```

---

## Module 4: RAG Synthesizer (122 lines → `hivenode/rag/synthesizer.py`)

**This file does NOT exist in the current hivenode/rag/. Port it.**

```python
class Synthesizer:
    def __init__(self, api_key=None, model=None, base_url=None)
        # Read from env: ANTHROPIC_API_KEY, RAG_MODEL (default haiku)

    def answer(self, query: str, chunks: list) -> dict
        # Build sources from chunks (file_path, lines, score)
        # Format context via _format_context()
        # POST to Claude /messages with system prompt + formatted context
        # Return: {answer, sources, model_used, cost_tokens, cost_usd, duration_ms}

    @staticmethod
    def _format_context(chunks) -> str
        # "--- Chunk N: path (L-L, score=X) ---\ncontent"
```

**Token cost formula:** `(input_tokens × 0.001 + output_tokens × 0.005) / 1000`

---

## Integration with Existing hivenode/rag/

The current `hivenode/rag/` has 5 files (engine.py, routes.py, chunkers.py, embedder.py, schemas.py). The ported code must integrate with these, not replace them:

1. **chunkers.py** — extend with AST-based Python chunker, JS regex chunker, PHASE-IR chunker from old `chunker.py`
2. **embedder.py** — extend with TF-IDF embedder from old `embedder.py` (current may only have simple embedding)
3. **schemas.py** — extend with full IndexRecord model from old `models.py`
4. **engine.py** — wire in IndexerService, ReliabilityCalculator, Synthesizer
5. **routes.py** — add indexer endpoints, bot embedding endpoints, BOK endpoints

If the current files conflict with the ported code, the ported code's data model wins — it's more complete.

---

## New Routes to Register

After porting, register these in `hivenode/main.py`:

```python
# Indexer
POST /rag/index-repo          # IndexerService.index_repository()
POST /rag/index-file           # IndexerService.index_file()
GET  /rag/index/{artifact_id}  # IndexStorage.get_by_id()
GET  /rag/index                # IndexStorage.list_all()

# Bot embeddings
POST /api/bots/{entity_id}/register
GET  /api/bots/{entity_id}/pi/{domain}
POST /api/bots/{entity_id}/check-drift

# BOK
GET  /rag/bok/search?query=...
POST /rag/bok/enrich

# Sync
POST /rag/sync/{artifact_id}  # CloudSyncService.sync_to_cloud()
POST /rag/sync-all             # CloudSyncService.sync_all()
GET  /rag/sync/status          # SyncDaemon.get_status()
```

---

## Verification

### Unit Tests (port from old + new)

For each module:
1. Scanner: test file classification for each ArtifactType
2. Chunker: test Python AST chunking, JS regex chunking, PHASE-IR chunking, markdown heading chunking
3. TF-IDF Embedder: test fit, transform, L2 normalization
4. Storage: test insert/get/update/delete/list with SQLite
5. IndexerService: test two-pass indexing pipeline
6. ReliabilityCalculator: test four-factor formula, canon detection
7. MetricsUpdater: test event handling for all 5 event types
8. Entity vectors: test alpha, sigma, rho, pi computations with known inputs
9. Bot embeddings: test cache hit/miss, drift detection
10. Voyage client: test with mocked API (don't call real API in tests)
11. Synthesizer: test context formatting, answer extraction
12. BOK: test keyword search, prompt enrichment

### Integration Test

End-to-end: index a small repo (3 files) → query → get synthesized answer with sources.

---

## Total Scope

| Module | Files | Lines | Target |
|---|---|---|---|
| Indexer Service | 11 | 3,060 | `hivenode/rag/indexer/` |
| Entity Embeddings | 4 | 1,234 | `hivenode/entities/` |
| BOK Services | 2 | 142 | `hivenode/rag/bok/` |
| RAG Synthesizer | 1 | 122 | `hivenode/rag/synthesizer.py` |
| **TOTAL** | **18** | **4,558** | |

**This is not optional. This is the difference between a demo RAG and a production RAG.**
