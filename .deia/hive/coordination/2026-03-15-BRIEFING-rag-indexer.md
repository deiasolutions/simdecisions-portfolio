# BRIEFING: Port RAG Indexer Service

**From:** Q33NR (regent)
**To:** Q33N (queen coordinator)
**Date:** 2026-03-15
**Spec:** 2026-03-15-1238-SPEC-w1-10-rag-indexer
**Model:** sonnet
**Priority:** P0.50

---

## Objective

Port the RAG (Retrieval-Augmented Generation) indexer service from platform repo to shiftcenter. This is a local artifact indexing system with document chunking, TF-IDF embedding generation, vector storage, and similarity search. Critical for context harness and BABOK interview bot (BL-043).

---

## Source Material

**Platform repo:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\`

**Source files (3,060 lines total):**
- `__init__.py` (27 lines) — exports
- `chunker.py` (323 lines) — artifact-type-aware chunking
- `cloud_sync.py` (318 lines) — sync to cloud storage (skip for now)
- `embedder.py` (180 lines) — TF-IDF embedding generation
- `indexer_service.py` (300 lines) — orchestration: scan → chunk → embed → store → emit
- `markdown_exporter.py` (194 lines) — export index to markdown (lower priority)
- `metrics_updater.py` (354 lines) — CCC + relevance + reliability tracking
- `models.py` (178 lines) — Pydantic models (IndexRecord, Chunk, IRPair, etc.)
- `reliability.py` (295 lines) — four-factor reliability model
- `scanner.py` (163 lines) — file system scanner with artifact type detection
- `storage.py` (462 lines) — SQLite storage for index records
- `sync_daemon.py` (266 lines) — background sync daemon (skip for now)

**Test files (3,872 lines total):**
- Platform tests: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\indexer\`
- 11 test files covering chunker, embedder, scanner, storage, service, events, metrics, reliability, cloud sync, markdown export, sync daemon

**API routes:**
- Platform RAG routes: `platform/efemera/src/efemera/rag/routes.py`
- Endpoints: `/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, `/api/rag/stats`

---

## Target Structure

**Destination:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\`

**Port these modules (priority order):**

1. **models.py** (foundation)
   - Port all Pydantic models
   - ArtifactType, Chunk, IRPair, IndexRecord, EmbeddingRecord, CCCMetadata, ReliabilityMetadata, etc.
   - Max 500 lines (may need split if platform version grows)

2. **scanner.py** (file discovery)
   - Scans filesystem for indexable artifacts
   - Detects artifact type from file extension/path
   - Yields (Path, ArtifactType) tuples

3. **chunker.py** (document chunking)
   - Type-aware chunking logic
   - Code: per function/method
   - PHASE-IR: per node
   - ADR: per decision section
   - Spec: per capability claim
   - Document: per section heading

4. **embedder.py** (TF-IDF embeddings)
   - TFIDFEmbedder class
   - Fit on corpus, transform chunks to vectors
   - Returns list[float] for each chunk

5. **storage.py** (SQLite vector store)
   - IndexStorage class
   - SQLite tables: index_records, chunks, embeddings
   - CRUD operations
   - Similarity search using cosine similarity

6. **indexer_service.py** (orchestration)
   - IndexerService class
   - Methods: index_repository(), index_file(), search()
   - Two-pass: scan corpus → fit embedder → index files
   - Emits CONTEXT_INDEXED events to ledger

7. **routes.py** (API endpoints)
   - FastAPI router under `/api/rag/`
   - POST /api/rag/index — index a folder
   - POST /api/rag/query — similarity search
   - GET /api/rag/chunks — list chunks for artifact
   - GET /api/rag/stats — index statistics

**Skip for now (future iteration):**
- cloud_sync.py (not needed for local indexing)
- sync_daemon.py (background process, add later)
- markdown_exporter.py (nice-to-have, not critical)
- reliability.py (four-factor model, add after core works)
- metrics_updater.py (CCC tracking, add after core works)

---

## Key Architectural Patterns (from MEMORY.md)

- **SQLite for vector storage** — use SQLite instead of pgvector (per spec constraint)
- **Event Ledger integration** — emit CONTEXT_INDEXED events when artifacts indexed
- **TDD required** — tests first, implementation second
- **No stubs** — every function fully implemented
- **Max 500 lines per file** — modularize if over 500
- **Absolute paths** — all file paths in task files must be absolute

---

## Dependencies

**Backend (hivenode):**
- FastAPI (already present)
- SQLAlchemy (already present for phase_ir)
- scikit-learn (for TF-IDF) — add to pyproject.toml if missing
- numpy (for vector operations) — add if missing

**Event Ledger:**
- Port depends on Event Ledger schema. Check if `hivenode/events/ledger.py` exists. If not, flag dependency.

---

## Acceptance Criteria (from spec)

- [ ] Indexer service ported with document chunking
- [ ] Embedding generation working (TF-IDF)
- [ ] Vector storage using SQLite (not pgvector)
- [ ] Similarity search API endpoint
- [ ] Tests written and passing

**Additional mechanical criteria:**
- [ ] All files under 500 lines
- [ ] No hardcoded colors (N/A — backend only)
- [ ] TDD: tests first
- [ ] No stubs
- [ ] Response file with all 8 sections

---

## Test Requirements

**Minimum test coverage:**
- Scanner tests: detect artifact types, skip ignored files, handle errors
- Chunker tests: chunk by artifact type, extract IR pairs, handle edge cases
- Embedder tests: fit corpus, transform chunks, handle empty input
- Storage tests: CRUD operations, similarity search, handle duplicates
- Service tests: index repository, index single file, emit events
- Routes tests: all 4 endpoints, error cases, authentication

**Target test count:** 40+ tests (11 test files in platform, can consolidate to ~6 files)

**Smoke test (from spec):**
```bash
python -m pytest tests/hivenode/test_rag_indexer.py -v
```

---

## File Paths to Reference

**Platform source:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\*.py`

**Platform tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\indexer\*.py`

**Platform RAG routes (for reference):**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\rag\routes.py`

**Destination:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\*.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rag_indexer.py`

**Related files (already ported):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\` (PHASE-IR port)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (DES routes port)

---

## Q33N: Write Task Files

Based on this briefing:

1. **Read the platform source files** to understand implementation details
2. **Check for dependencies** (Event Ledger, scikit-learn, numpy)
3. **Write bee task files** (one per module or logical group)
   - TASK-151: Port models.py + tests
   - TASK-152: Port scanner.py + tests
   - TASK-153: Port chunker.py + tests
   - TASK-154: Port embedder.py + tests
   - TASK-155: Port storage.py + tests
   - TASK-156: Port indexer_service.py + tests
   - TASK-157: Port rag_routes.py + tests
4. **Return task files to Q33NR for review** (do NOT dispatch bees yet)

---

## Constraints from Spec

- Max 500 lines per file (hard limit 1,000)
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only (N/A — backend only)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-15-1238-SPEC-w1-10-rag-indexer", "status": "running", "model": "sonnet", "message": "working"}
  ```

---

## Q33NR Review Checklist

When Q33N returns task files, I (Q33NR) will verify:

- [ ] All acceptance criteria covered
- [ ] File paths absolute
- [ ] Test requirements specified
- [ ] No files over 500 lines
- [ ] No stubs allowed
- [ ] Response file template included
- [ ] Dependencies identified

---

## Next Steps

1. Q33N reads this briefing
2. Q33N explores platform source
3. Q33N writes 7 task files (TASK-151 through TASK-157)
4. Q33N returns to Q33NR for review
5. Q33NR reviews and approves (or requests corrections)
6. Q33N dispatches bees
7. Bees complete work
8. Q33N reports results to Q33NR
9. Q33NR reports to Q88N

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-1238-SPE
**Briefing complete. Awaiting Q33N task files.**
