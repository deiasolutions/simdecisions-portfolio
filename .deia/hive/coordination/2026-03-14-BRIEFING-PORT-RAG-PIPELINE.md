# BRIEFING: Port RAG Pipeline (Indexer + Entities + BOK + Synthesizer)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-14
**Priority:** P0

---

## Objective

Port the 4 missing RAG subsystems from the old repo (`platform/efemera/src/efemera/`) to shiftcenter (`hivenode/`). This is a PORT, not a rewrite. Same classes, same methods, same algorithms. Import path changes + hivenode integration patterns only.

## Why

The current `hivenode/rag/` has the skeleton (engine, routes, chunkers, embedder, schemas — 1,098 lines). But everything that makes RAG production-grade is missing:

- **Indexer service** (3,060 lines) — file scanning, AST-based chunking, TF-IDF embedding, SQLite storage, reliability metrics, cloud sync, background daemon. Without this, there's no way to index a repo.
- **Entity embeddings** (1,234 lines) — the 5-vector profiling system (alpha/sigma/rho/pi), cold-start cascade, Voyage AI, drift detection. Without this, entities have no identity.
- **BOK services** (142 lines) — knowledge base search and prompt enrichment. Without this, the AI has no domain knowledge.
- **Synthesizer** (122 lines) — LLM-powered answer generation from retrieved chunks. Without this, RAG returns raw chunks instead of answers.

Total: 4,558 lines across 18 files.

## Spec

Read the full spec: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`

It has every class, method, algorithm, and data model documented.

## Source Files (OLD repo — READ ONLY, DO NOT MODIFY)

### Module 1: Indexer Service (3,060 lines)
`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\`

| File | Lines | Role |
|---|---|---|
| models.py | 179 | Enums (ArtifactType, StorageTier, IRStatus) + 11 Pydantic models |
| scanner.py | 164 | File classification by extension/name pattern |
| chunker.py | 324 | AST-based Python, regex JS, heading markdown, PHASE-IR JSON |
| embedder.py | 181 | TF-IDF embedder (fit/transform/L2 normalize) |
| storage.py | 463 | SQLite persistence (3 tables: records, chunks, embeddings) |
| indexer_service.py | 301 | Two-pass orchestrator (scan → fit → index) |
| reliability.py | 296 | Four-factor reliability model |
| metrics_updater.py | 355 | Async event processor (5 event types) |
| markdown_exporter.py | 195 | Dual-storage markdown export |
| cloud_sync.py | 319 | SQLite → Postgres + pgvector sync |
| sync_daemon.py | 267 | Background sync orchestrator (IMMEDIATE/BATCHED/MANUAL) |

### Module 2: Entity Embeddings (1,234 lines)
`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\`

| File | Lines | Role |
|---|---|---|
| vectors.py | 686 | 5-vector system (alpha, sigma, rho, pi_bot, pi_human), cold-start cascade |
| embeddings.py | 281 | Bot embedding cache, drift detection, pi computation |
| voyage_embedding.py | 142 | Voyage AI client with fallback |
| embedding_routes.py | 129 | FastAPI routes (/api/bots/) |

### Module 3: BOK Services (142 lines)
`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\bok\`

| File | Lines | Role |
|---|---|---|
| embedding_service.py | 79 | Voyage AI embedding generation |
| rag_service.py | 65 | Keyword search + prompt enrichment |

### Module 4: Synthesizer (122 lines)
`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\rag\synthesizer.py`

## Target Locations

| Module | Target |
|---|---|
| Indexer | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\` |
| Entities | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\` |
| BOK | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\` |
| Synthesizer | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\synthesizer.py` |

## Existing ShiftCenter RAG Files to Read

Before decomposing, Q33N must read these to understand what exists and how to integrate:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\engine.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\embedder.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\schemas.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (router registration)

## Task Decomposition Guidance

Suggest 4 waves matching the 4 modules:

**Wave 1 — Indexer Data Model + Scanner + Chunker + Embedder (models.py, scanner.py, chunker.py, embedder.py = 848 lines)**
These are the foundation. No external dependencies beyond stdlib + pydantic. Can be one task.

**Wave 2 — Indexer Storage + Service (storage.py, indexer_service.py = 764 lines)**
Depends on Wave 1 models. storage.py is 463 lines (close to limit), keep it as one file.

**Wave 3 — Indexer Reliability + Metrics + Sync (reliability.py, metrics_updater.py, markdown_exporter.py, cloud_sync.py, sync_daemon.py = 1,432 lines)**
These depend on storage and models. Can be split into two tasks:
- 3a: reliability.py + metrics_updater.py (651 lines)
- 3b: markdown_exporter.py + cloud_sync.py + sync_daemon.py (781 lines)

**Wave 4 — Entity Embeddings (vectors.py, embeddings.py, voyage_embedding.py, embedding_routes.py = 1,238 lines)**
Independent of indexer. Can run in parallel with Wave 2/3.
- 4a: voyage_embedding.py + embeddings.py (423 lines)
- 4b: vectors.py (686 lines — large, complex, one bee)
- 4c: embedding_routes.py (129 lines — depends on 4a/4b)

**Wave 5 — BOK + Synthesizer (142 + 122 = 264 lines)**
Small. One task.

**Wave 6 — Integration + Routes**
Wire indexer into hivenode/main.py. Register all new routes. Connect to existing engine.py.

## Model Assignment

- Wave 1: Sonnet (AST chunker is algorithmic)
- Wave 2: Sonnet (storage is 463 lines, complex schema)
- Wave 3a: Haiku (reliability formulas are straightforward port)
- Wave 3b: Sonnet (cloud_sync involves psycopg2 + pgvector)
- Wave 4a: Haiku (Voyage client is simple HTTP)
- Wave 4b: Sonnet (vectors.py is 686 lines of entity math)
- Wave 4c: Haiku (thin FastAPI routes)
- Wave 5: Haiku (small, simple)
- Wave 6: Sonnet (integration wiring)

## Constraints

- PORT, not rewrite. Read the old file, adapt imports, preserve behavior.
- TDD: tests first for each module
- No file over 500 lines (vectors.py at 686 MUST be split into two files)
- No stubs
- Algorithms must be identical — same formulas, same decay windows, same confidence calculations
- If existing hivenode/rag/ files conflict with ported data models, the ported model wins (it's more complete)

## Deliverable

Write task files to `.deia/hive/tasks/`. Return to me for review before dispatching bees.

**Do Shell first. Start RAG after Shell bees are dispatched.**
