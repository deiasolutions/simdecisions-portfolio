# TASK-122: RAG Integration + Route Registration

**Wave:** 6
**Model:** sonnet
**Role:** bee
**Depends on:** ALL prior tasks (TASK-110 through TASK-121)

---

## Objective

Integrate all RAG components (indexer, entities, BOK, synthesizer) with hivenode, register routes, extend engine.py factories, and write end-to-end integration tests.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- All files created in TASK-110 through TASK-121 (indexer, entities, BOK, synthesizer)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (FastAPI app setup)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\engine.py` (existing RAG engine)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py` (existing RAG routes)

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (register new routers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\engine.py` (add factories for new services)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py` (extend with indexer endpoints)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\routes.py` (indexer-specific routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\routes.py` (BOK routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_integration.py`

## Deliverables

### NEW FILE: hivenode/rag/indexer/routes.py (130 lines)

**Router:** Indexer routes

```python
from fastapi import APIRouter, Depends, HTTPException
from hivenode.auth import verify_jwt_or_local
from hivenode.rag.indexer.indexer_service import IndexerService
from hivenode.rag.indexer.storage import IndexStorage
from hivenode.rag.indexer.cloud_sync import CloudSyncService
from hivenode.rag.indexer.sync_daemon import SyncDaemon
from hivenode.database import get_db
from pydantic import BaseModel
from pathlib import Path

router = APIRouter(prefix="/rag", tags=["indexer"])
```

**Endpoints:**

1. **`POST /rag/index-repo`**
   - Auth: `verify_jwt_or_local()`
   - Body: `{"repo_path": str}`
   - Call: `IndexerService.index_repository()`
   - Return: stats dict

2. **`POST /rag/index-file`**
   - Auth: `verify_jwt_or_local()`
   - Body: `{"file_path": str}`
   - Call: `IndexerService.index_file()`
   - Return: `{"artifact_id": str}`

3. **`GET /rag/index/{artifact_id}`**
   - Auth: `verify_jwt_or_local()`
   - Call: `IndexStorage.get_by_id(artifact_id)`
   - Return: IndexRecord (serialized to JSON)

4. **`GET /rag/index`**
   - Auth: `verify_jwt_or_local()`
   - Query params: `artifact_type: Optional[str]`, `storage_tier: Optional[str]`, `limit: int = 100`, `offset: int = 0`
   - Call: `IndexStorage.list_all()`
   - Return: list of IndexRecord

5. **`POST /rag/sync/{artifact_id}`**
   - Auth: `verify_jwt_or_local()`
   - Call: `CloudSyncService.sync_to_cloud(artifact_id)`
   - Return: `{"success": bool}`

6. **`POST /rag/sync-all`**
   - Auth: `verify_jwt_or_local()`
   - Call: `CloudSyncService.sync_all()`
   - Return: stats dict

7. **`GET /rag/sync/status`**
   - Auth: `verify_jwt_or_local()`
   - Call: `SyncDaemon.get_status()`
   - Return: status dict

---

### NEW FILE: hivenode/rag/bok/routes.py (60 lines)

**Router:** BOK routes

```python
from fastapi import APIRouter, Depends, Query
from hivenode.auth import verify_jwt_or_local
from hivenode.rag.bok.rag_service import search_bok, enrich_prompt
from hivenode.database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/rag", tags=["bok"])
```

**Endpoints:**

1. **`GET /rag/bok/search`**
   - Auth: `verify_jwt_or_local()`
   - Query param: `query: str`
   - Call: `search_bok(query, db)`
   - Return: list of BokEntry

2. **`POST /rag/bok/enrich`**
   - Auth: `verify_jwt_or_local()`
   - Body: `{"base_prompt": str, "query": str, "max_entries": int = 3}`
   - Call: `enrich_prompt(base_prompt, query, db, max_entries)`
   - Return: `{"enriched_prompt": str, "bok_entries": list[BokEntry]}`

---

### MODIFY: hivenode/main.py (add router registrations)

**Add imports:**
```python
from hivenode.rag.indexer.routes import router as indexer_router
from hivenode.rag.bok.routes import router as bok_router
from hivenode.entities.routes import router as entities_router
```

**Register routers:**
```python
app.include_router(indexer_router, prefix="/rag", tags=["indexer"])
app.include_router(bok_router, prefix="/rag", tags=["bok"])
app.include_router(entities_router, prefix="/api", tags=["entities"])
```

**Note:** Existing `/rag/index`, `/rag/ingest-chat`, `/rag/search` routes remain UNCHANGED (backward compatibility).

---

### MODIFY: hivenode/rag/engine.py (add factory methods)

**Add imports:**
```python
from hivenode.rag.indexer.indexer_service import IndexerService
from hivenode.rag.indexer.storage import IndexStorage
from hivenode.rag.indexer.reliability import ReliabilityCalculator
from hivenode.rag.indexer.cloud_sync import CloudSyncService
from hivenode.rag.indexer.markdown_exporter import MarkdownExporter
from hivenode.rag.indexer.sync_daemon import SyncDaemon, create_daemon_from_env
from hivenode.rag.synthesizer import Synthesizer
```

**Add factory methods (singleton pattern, lazy init):**

```python
_indexer_service: Optional[IndexerService] = None
_reliability_calculator: Optional[ReliabilityCalculator] = None
_synthesizer: Optional[Synthesizer] = None
_sync_daemon: Optional[SyncDaemon] = None

def get_indexer_service(repo_path: Path, db_session: Session) -> IndexerService:
    global _indexer_service
    if _indexer_service is None:
        storage = IndexStorage()
        _indexer_service = IndexerService(
            repo_path=repo_path,
            db_session=db_session,
            storage=storage,
            actor_id="indexer-service",
            node_id="local-hive"
        )
    return _indexer_service

def get_reliability_calculator(db_session: Session) -> ReliabilityCalculator:
    global _reliability_calculator
    if _reliability_calculator is None:
        storage = IndexStorage()
        _reliability_calculator = ReliabilityCalculator(storage, db_session)
    return _reliability_calculator

def get_synthesizer() -> Synthesizer:
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = Synthesizer()
    return _synthesizer

def get_sync_daemon() -> SyncDaemon:
    global _sync_daemon
    if _sync_daemon is None:
        storage = IndexStorage()
        exporter = MarkdownExporter()
        cloud_sync = CloudSyncService(storage, exporter)
        cloud_sync.connect()  # Connect to Postgres if HIVE_CLOUD_DB_URL set
        _sync_daemon = create_daemon_from_env(storage, exporter, cloud_sync)
        _sync_daemon.start()  # Start background thread
    return _sync_daemon
```

---

### MODIFY: hivenode/rag/routes.py (extend with convenience endpoint)

**Add endpoint:**

```python
@router.post("/rag/query")
async def query_rag(
    query: str,
    repo_path: Optional[str] = None,
    db: Session = Depends(get_db),
    auth: dict = Depends(verify_jwt_or_local)
):
    """
    End-to-end RAG query: search index → retrieve chunks → synthesize answer
    """
    from hivenode.rag.engine import get_indexer_service, get_synthesizer
    from pathlib import Path

    # Default repo path
    if not repo_path:
        repo_path = Path.cwd()

    # Search index (simple keyword search for now)
    # TODO: Replace with vector search when available
    storage = IndexStorage()
    records = storage.list_all(limit=10)

    # Get chunks from top records
    chunks = []
    for record in records[:5]:
        chunks.extend(storage.get_chunks(record.artifact_id))

    # Synthesize answer
    synthesizer = get_synthesizer()
    result = synthesizer.answer(query, chunks[:10])  # Top 10 chunks

    return result
```

---

### NEW FILE: tests/hivenode/rag/test_integration.py (8 tests)

**End-to-end integration tests:**

1. **Test full indexing pipeline:**
   - Create test repo with 3 files (Python, TypeScript, Markdown)
   - Call `IndexerService.index_repository()`
   - Verify: 3 IndexRecord created, chunks stored, embeddings stored

2. **Test query pipeline:**
   - Index test files
   - Call `/rag/query` endpoint with query
   - Verify: synthesizer returns answer with sources

3. **Test BOK enrichment:**
   - Insert 2 BOK entries in DB
   - Call `enrich_prompt()` with query matching BOK keywords
   - Verify: enriched prompt includes BOK content

4. **Test entity vectors:**
   - Insert mock Event Ledger events (task.completed, task.failed)
   - Call `recalculate_entity()` for test entity
   - Verify: alpha, sigma, rho computed correctly

5. **Test cloud sync:**
   - Index 2 files
   - Call `CloudSyncService.sync_all()`
   - Verify: records synced to Postgres (use testcontainers)

6. **Test sync daemon IMMEDIATE policy:**
   - Create SyncDaemon with IMMEDIATE policy
   - Index 1 file
   - Verify: file immediately synced to markdown

7. **Test backward compatibility:**
   - Existing `/rag/index` endpoint still works
   - Existing `/rag/search` endpoint still works

8. **Test error handling:**
   - Index file with syntax error → logs warning, continues
   - Query with no results → synthesizer returns "No context available"

**Test setup:**
- Use real server via TestClient
- Use temporary directories for test repos
- Use in-memory SQLite for DB
- Use testcontainers Postgres for cloud sync tests

## Acceptance Criteria

- [ ] All listed files created/modified
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/test_integration.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same route structure, same factory pattern as platform/efemera
- [ ] TDD: tests written first
- [ ] 8+ integration tests covering full pipeline, BOK enrichment, entity vectors, cloud sync, errors
- [ ] Backward compatibility: existing `/rag/index`, `/rag/ingest-chat`, `/rag/search` routes UNCHANGED
- [ ] New routes coexist with existing routes (no conflicts)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-122-RESPONSE.md`

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
