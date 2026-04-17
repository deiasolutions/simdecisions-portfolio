# TASK-157: Port RAG API Routes

## Objective
Port the FastAPI routes that expose RAG indexing and search functionality via REST API.

## Context
The RAG routes provide 4 endpoints:
- POST /api/rag/index — index a folder
- POST /api/rag/query — similarity search (returns matching chunks)
- GET /api/rag/chunks — list chunks for artifact
- GET /api/rag/stats — index statistics

The platform version includes LLM-synthesized answers via `RAGEngine.query()`, but for Sprint 1 we're implementing search-only (no LLM synthesis yet).

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\rag\routes.py` (154 lines, uses RAGEngine)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py`

**Key difference from platform:** Platform uses `RAGEngine` class. We're porting indexer service only, so routes will directly use IndexerService + similarity search.

**Dependencies:**
- TASK-151 through TASK-156 (all indexer modules)
- Similarity search function (may need to implement cosine_similarity helper)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\rag\routes.py` (reference only — will need adaptation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (from TASK-156)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (from TASK-155)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (reference for route patterns in shiftcenter)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py`
- [ ] Implement 4 endpoints:
  - POST /api/rag/index (IndexRequest → IndexResponse)
  - POST /api/rag/query (QueryRequest → QueryResponse with chunks, no LLM synthesis yet)
  - GET /api/rag/chunks?artifact_id=... (return chunks for artifact)
  - GET /api/rag/stats (return total indexed artifacts, counts by type)
- [ ] Define Pydantic request/response models in routes file:
  - IndexRequest (folder_path)
  - QueryRequest (query, top_k)
  - IndexResponse (files, chunks, duration_ms)
  - QueryResponse (chunks: list[ChunkMatch], query_vector)
  - ChunkMatch (chunk_id, content, score, artifact_id, artifact_type, path)
  - StatsResponse (total_artifacts, by_type: dict)
- [ ] Implement cosine similarity search helper (if not in storage.py):
  - `cosine_similarity(vec_a, vec_b)` → float
  - `search_similar_chunks(query_text, storage, embedder, top_k)` → list[ChunkMatch]
- [ ] Register routes in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rag_routes.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test POST /api/rag/index with valid folder path
- [ ] Test POST /api/rag/index with non-existent folder (400 error)
- [ ] Test POST /api/rag/query returns matching chunks
- [ ] Test POST /api/rag/query with empty query (400 error)
- [ ] Test POST /api/rag/query returns top_k results sorted by score
- [ ] Test GET /api/rag/chunks?artifact_id=... returns chunks
- [ ] Test GET /api/rag/chunks with invalid artifact_id (404 error)
- [ ] Test GET /api/rag/stats returns correct counts
- [ ] Test cosine_similarity() computes correct similarity score
- [ ] Test search_similar_chunks() returns correct top_k matches
- [ ] Edge cases:
  - Empty index (no artifacts)
  - Query with no matches (empty result)
  - Very large top_k (> total chunks)
  - Unicode queries
  - Special characters in folder paths

**Target test count:** 15+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/test_rag_routes.py -v
```

## Cosine Similarity Helper Template

```python
import math

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec_a: First vector
        vec_b: Second vector

    Returns:
        Similarity score in [0, 1] (1 = identical, 0 = orthogonal)
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have same length")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot_product / (mag_a * mag_b)
```

## Constraints
- No file over 500 lines
- No stubs — all endpoints fully implemented
- TDD: tests first
- POST /api/rag/query returns chunks only (no LLM synthesis) — that's for Sprint 2
- Use TestClient with mock SQLite db (see test_des_routes.py for reference)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-157-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks (note LLM synthesis pending)

DO NOT skip any section.

---

**Priority:** P0.50
**Model:** sonnet (API design, search logic)
**Estimated time:** 35 minutes
**Dependencies:** TASK-151, TASK-152, TASK-153, TASK-154, TASK-155, TASK-156
