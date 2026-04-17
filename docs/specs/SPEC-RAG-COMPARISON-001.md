# SPEC-RAG-COMPARISON-001: RAG System Comparison (ShiftCenter vs FamilyBondBot)

**Date:** 2026-03-12
**Status:** Reference
**Purpose:** Document differences between the two RAG implementations to inform future decisions (BL-074)

## Summary

Two RAG systems exist across DEIA projects. They serve completely different purposes and do not overlap. This doc captures the architectural differences so we can evaluate whether FBB patterns should be ported to ShiftCenter.

## Side-by-Side Comparison

| Dimension | ShiftCenter (`hivenode/rag/`) | FamilyBondBot (`fbb/backend-v2/`) |
|---|---|---|
| **Purpose** | Code + chat search for developer tooling | Curated KB retrieval for coaching bot |
| **What gets indexed** | Raw code files (.py, .ts, .tsx, .md, .css) + chat messages | Curated ContentEntity records (personas, rules, topics, handlers) |
| **Embedding model** | sentence-transformers `all-MiniLM-L6-v2` (local, 384-dim, free) | Voyage AI `voyage-3.5-lite` (API, 1024-dim, $0.02/1M tokens) |
| **Storage** | SQLite (`rag-index.db`, two tables: `code_chunks`, `chat_chunks`) | PostgreSQL (`content_entities` table, embedding as JSONB column) |
| **Chunking** | Python AST, TS regex, MD headings, CSS whole-file, chat messages | No chunking — each ContentEntity is a pre-curated unit |
| **Retrieval strategy** | Flat cosine similarity, top-k | 3-tier: ALWAYS (no filter) + STATE (condition match) + SITUATION (semantic) |
| **Threshold** | Single `min_score` parameter | Priority-weighted: high-priority items get lower thresholds (0.3), low-priority get higher (0.7) |
| **Reranking** | None | Optional Haiku-based reranker on top 15 candidates |
| **Recency penalty** | None | `kb_exposure_history` table, skip content shown within last 3 turns |
| **Keyword matching** | None | Fast-path: keyword match = similarity 1.0, skip embedding |
| **Long input handling** | None | Theme extraction for messages > 500 words (embed themes separately) |
| **Token budgeting** | `maxChars` in context builder (char-based) | `situation_token_budget` tracked but not enforced (count-based: top 6 items) |
| **Content types** | 2 (code, chat) | 6 (PERSONA, RULE, HANDLER, TOPIC, CHAT_CONTEXT, RERANKER) |
| **Prompt injection** | System prompt append (try/catch, non-blocking) | Structured prompt assembly (personas → rules → handlers → topics → context → history) |

## FBB Patterns Worth Evaluating for ShiftCenter

### 1. Voyage AI as Alternative Embedder
- **Pro:** Higher quality embeddings (1024-dim vs 384-dim), Anthropic-recommended
- **Pro:** No local model download (~400MB for sentence-transformers)
- **Con:** Requires API key and network, costs money
- **Decision:** Could offer as alternative backend in `embedder.py` (config switch)

### 2. Priority-Weighted Thresholds
- **Pro:** Important code (e.g., core modules) could have lower thresholds
- **Con:** ShiftCenter chunks don't have priority metadata (would need heuristic: file path depth? test coverage?)
- **Decision:** Low value for code search, but useful if we add curated knowledge

### 3. Keyword Fast-Path
- **Pro:** Exact filename/function name matches skip embedding entirely — faster, more precise
- **Con:** Simple to implement
- **Decision:** Strong candidate. Could add keyword index to `code_chunks` table

### 4. Reranker (Haiku-based)
- **Pro:** Better precision by filtering false positives
- **Con:** Extra API call per search, adds latency and cost
- **Decision:** Overkill for v1. Revisit when search quality becomes a complaint

### 5. Recency Penalty / Exposure Tracking
- **Pro:** Avoid showing same context repeatedly in chat
- **Con:** Only matters for long conversations
- **Decision:** Low priority. Chat context builder already has char budget that naturally limits repetition

### 6. Theme Extraction for Long Inputs
- **Pro:** Better matching for verbose queries
- **Con:** Extra LLM call
- **Decision:** Interesting for when users paste large code blocks as queries. Revisit later

## Files Reference

### ShiftCenter RAG
- `hivenode/rag/chunkers.py` — Code + chat chunking
- `hivenode/rag/embedder.py` — Local sentence-transformers singleton
- `hivenode/rag/engine.py` — RagEngine (index, ingest, search, status, reset)
- `hivenode/rag/routes.py` — 5 FastAPI endpoints
- `hivenode/rag/schemas.py` — Pydantic models
- `browser/src/services/rag/ragApi.ts` — Browser HTTP client
- `browser/src/services/rag/ragContextBuilder.ts` — Format results for prompts
- Tests: `tests/hivenode/rag/` (59 tests), `browser/src/services/rag/` (21 tests)

### FamilyBondBot RAG
- `fbb/backend-v2/src/services/embedding_service.py` — Voyage AI client + cosine similarity
- `fbb/backend-v2/src/services/content_retrieval_service.py` — 3-tier retrieval pipeline
- `fbb/backend-v2/src/services/reranker_service.py` — Haiku reranker
- `fbb/backend-v2/src/services/prompt_prep_service.py` — Unified prompt prep
- `fbb/backend-v2/src/models/content_entity.py` — 6-type entity model
- `fbb/backend-v2/scripts/backfill_content_embeddings.py` — Batch embedding generator

## Conclusion

No duplicate work. The systems serve different domains. The most portable patterns from FBB are **keyword fast-path** (easy win) and **Voyage AI as alternative embedder** (config switch). The sophisticated retrieval tiers and reranker are overkill for code search but worth revisiting if ShiftCenter adds curated knowledge bases.
