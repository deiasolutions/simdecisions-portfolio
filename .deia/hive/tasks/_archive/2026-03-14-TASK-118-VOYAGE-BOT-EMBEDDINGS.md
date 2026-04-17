# TASK-118: Voyage AI Client + Bot Embeddings

**Wave:** 4
**Model:** haiku
**Role:** bee
**Depends on:** None (independent of indexer)

---

## Objective

Build Voyage AI embedding client for production embeddings and bot profile embedding system with drift detection.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

None (this is Wave 4, independent of indexer Wave 1-3)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\voyage_embedding.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\embeddings.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_voyage_embedding.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_embeddings.py`

## Files to Modify

None

## Deliverables

### voyage_embedding.py (142 lines)

**Function:** `get_embedding(text: str, model: Optional[str] = None) -> list[float]`

**Implementation:**
- URL: `https://api.voyageai.com/v1/embeddings`
- Model: default `voyage-2` (can override via parameter)
- API key: from `os.getenv("VOYAGE_API_KEY")`
- If API key not set:
  - Log WARNING: "VOYAGE_API_KEY not set, using fallback hash-based embedding"
  - Return `hash_embedding(text)` (dummy vector)
- POST request with:
  ```json
  {
    "input": [text],
    "model": model
  }
  ```
- Headers: `{"Authorization": "Bearer {api_key}", "Content-Type": "application/json"}`
- Extract embedding from response: `response.json()["data"][0]["embedding"]`
- Return list[float]

**In-memory cache:**
- Use `functools.lru_cache` with maxsize=1000
- Cache key: SHA256(text + model)
- Cache hit avoids API call

**Error handling:**
- Timeout: 30 seconds
- ConnectionError: log error, return `hash_embedding(text)` fallback
- HTTPError (4xx/5xx): log error, return fallback
- Unexpected response format: log error, return fallback

**Helper function:** `hash_embedding(text: str, dimension: int = 1024) -> list[float]`
- Hash text with SHA256
- Convert hash bytes to list of floats (normalize to range [-1, 1])
- Pad or truncate to dimension
- Return list[float]

**Utility function:** `clear_cache() -> None`
- Clear LRU cache (for tests)

### test_voyage_embedding.py (6+ tests)

**Test cases (use mock HTTP requests):**
- Test `get_embedding()` with mocked Voyage API response
- Test cache hit (second call with same text returns cached result, no API call)
- Test cache miss (different text triggers new API call)
- Test fallback when VOYAGE_API_KEY not set
- Test fallback on ConnectionError
- Test `hash_embedding()` produces consistent vector for same input
- Test `clear_cache()` clears LRU cache

---

### embeddings.py (281 lines)

**ORM Model:** `BotEmbeddingStore`

```python
class BotEmbeddingStore(Base):
    __tablename__ = "bot_embeddings"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, unique=True, nullable=False)  # bot ID
    system_prompt_hash = Column(String, nullable=False)      # SHA256 of prompt
    embedding = Column(LargeBinary, nullable=False)          # pickled list[float]
    model_version = Column(String, nullable=False)           # e.g. "voyage-2"
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Function:** `get_or_compute_bot_embedding(entity_id: str, system_prompt: str, db: Session) -> list[float]`

**Implementation:**
- Compute prompt_hash = SHA256(system_prompt)
- Query DB for BotEmbeddingStore WHERE entity_id = ? AND system_prompt_hash = ?
- If found: unpickle and return embedding
- Else:
  - Call `get_embedding(system_prompt, model="voyage-2")`
  - Pickle embedding
  - Insert or update BotEmbeddingStore
  - Return embedding

**Function:** `compute_pi_bot_full(entity_id: str, domain: str, system_prompt: str, task_text: Optional[str] = None, db: Optional[Session] = None) -> tuple[float, dict]`

**Implementation:**
- Get bot embedding: `get_or_compute_bot_embedding(entity_id, system_prompt, db)`
- Get domain archetype embedding (hardcoded for now, or from DB)
- Compute domain_sim = cosine_similarity(bot_embedding, domain_archetype_embedding)
- If task_text provided:
  - Get task embedding: `get_embedding(task_text)`
  - Compute task_sim = cosine_similarity(bot_embedding, task_embedding)
  - pi = (domain_sim + task_sim) / 2
- Else:
  - pi = domain_sim
- Return (pi, {"domain_sim": domain_sim, "task_sim": task_sim if task_text else None})

**Function:** `check_bot_drift(entity_id: str, new_system_prompt: str, threshold: float = 0.3, db: Optional[Session] = None) -> dict`

**Implementation:**
- Get current cached embedding for entity_id (latest in DB)
- If not found: return `{"drifted": False, "reason": "no_baseline"}`
- Compute new embedding: `get_embedding(new_system_prompt)`
- Compute similarity = cosine_similarity(current_embedding, new_embedding)
- drifted = similarity < (1 - threshold)  # e.g. threshold=0.3 → drifted if sim < 0.7
- Return:
  ```python
  {
    "drifted": drifted,
    "similarity": similarity,
    "threshold": threshold,
    "current_hash": current_prompt_hash,
    "new_hash": SHA256(new_system_prompt)
  }
  ```

**Function:** `register_bot_profile(entity_id: str, system_prompt: str, model_id: Optional[str] = None, db: Optional[Session] = None) -> dict`

**Implementation:**
- Call `get_or_compute_bot_embedding(entity_id, system_prompt, db)` to cache embedding
- Return:
  ```python
  {
    "entity_id": entity_id,
    "prompt_hash": SHA256(system_prompt),
    "model_version": model_id or "voyage-2",
    "cached": True
  }
  ```

**Helper function:** `cosine_similarity(vec1: list[float], vec2: list[float]) -> float`
- Compute dot product: sum(a * b for a, b in zip(vec1, vec2))
- Compute norms: ||vec1||, ||vec2||
- Return dot / (norm1 * norm2)

### test_embeddings.py (8+ tests)

**Test cases (use mock DB session):**
- Test `get_or_compute_bot_embedding()` caches embedding in DB
- Test `get_or_compute_bot_embedding()` returns cached embedding on second call
- Test `compute_pi_bot_full()` with domain only (no task_text)
- Test `compute_pi_bot_full()` with domain + task_text (average of both sims)
- Test `check_bot_drift()` returns drifted=True when similarity < 0.7
- Test `check_bot_drift()` returns drifted=False when similarity >= 0.7
- Test `check_bot_drift()` returns no_baseline when entity_id not found
- Test `register_bot_profile()` creates DB entry
- Test `cosine_similarity()` returns correct value for known vectors

### __init__.py

Export all functions:
```python
__all__ = [
    "get_embedding",
    "hash_embedding",
    "clear_cache",
    "get_or_compute_bot_embedding",
    "compute_pi_bot_full",
    "check_bot_drift",
    "register_bot_profile",
    "BotEmbeddingStore"
]
```

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/entities/ -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same Voyage API client, same drift detection (cosine sim < 0.7), same pi formula as platform/efemera
- [ ] TDD: tests written first
- [ ] 14+ tests total (6 voyage + 8 embeddings)
- [ ] Environment variable: `VOYAGE_API_KEY` (fallback to hash_embedding if not set)
- [ ] Cache: LRU maxsize=1000 for Voyage API calls

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-118-RESPONSE.md`

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
