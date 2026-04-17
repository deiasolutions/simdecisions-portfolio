# TASK-121: BOK Services + RAG Synthesizer

**Wave:** 5
**Model:** haiku
**Role:** bee
**Depends on:** None (independent, can run parallel with all other waves)

---

## Objective

Build Body of Knowledge (BOK) keyword search, prompt enrichment, and LLM synthesis service for RAG answer generation.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

None (independent Wave 5 task)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\embedding_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\rag_service.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\synthesizer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\bok\test_bok_services.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_synthesizer.py`

## Files to Modify

None

## Deliverables

### bok/embedding_service.py (50 lines)

**Function:** `generate_embedding(text: str) -> list[float]`

**Implementation:**
- URL: `https://api.voyageai.com/v1/embeddings`
- Model: `voyage-large-2` (BOK uses larger model than indexer)
- API key: `os.getenv("VOYAGE_API_KEY")` — REQUIRED (raise ValueError if not set)
- POST request with:
  ```json
  {
    "input": [text],
    "model": "voyage-large-2"
  }
  ```
- Headers: `{"Authorization": "Bearer {api_key}", "Content-Type": "application/json"}`
- Extract embedding: `response.json()["data"][0]["embedding"]`
- Return list[float]

**Error handling:**
- No API key: raise ValueError("VOYAGE_API_KEY required for BOK embeddings")
- Timeout: 30 seconds
- HTTPError: raise with error details

---

### bok/rag_service.py (92 lines)

**Function:** `search_bok(query: str, db: Session, limit: int = 5) -> list[BokEntry]`

**Implementation:**
- Keyword search (simple, no embeddings)
- Split query on whitespace: `keywords = query.lower().split()`
- Query BokEntry table (assume table exists with columns: id, title, content, keywords)
- WHERE clause: `title LIKE %keyword% OR content LIKE %keyword%` for each keyword
- ORDER BY relevance (count of matching keywords)
- LIMIT results
- Return list of BokEntry objects

**Function:** `format_bok_for_prompt(entries: list[BokEntry]) -> str`

**Implementation:**
- Format as markdown:
  ```markdown
  ## Relevant Knowledge (from BOK)

  ### {entry.title}
  {entry.content}

  ---

  ### {entry2.title}
  {entry2.content}

  ---
  ```
- Return formatted string

**Function:** `enrich_prompt(base_prompt: str, query: str, db: Session, max_entries: int = 3) -> tuple[str, list[BokEntry]]`

**Implementation:**
- Call `search_bok(query, db, limit=max_entries)`
- If no results: return (base_prompt, [])
- Format BOK entries: `bok_section = format_bok_for_prompt(entries)`
- Enrich prompt:
  ```python
  enriched = f"{base_prompt}\n\n{bok_section}\n\nUser Query: {query}"
  ```
- Return (enriched, entries)

---

### synthesizer.py (122 lines)

**Class:** `Synthesizer`

**Attributes:**
- `api_key: str` — from `os.getenv("ANTHROPIC_API_KEY")` or parameter
- `model: str` — from `os.getenv("RAG_MODEL", "claude-haiku-3-5-20241022")` or parameter
- `base_url: str` — `"https://api.anthropic.com/v1/messages"`

**Methods:**

1. **`__init__(api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None)`**
   - api_key: default from env `ANTHROPIC_API_KEY` (raise ValueError if not set)
   - model: default from env `RAG_MODEL` or "claude-haiku-3-5-20241022"
   - base_url: default "https://api.anthropic.com/v1/messages"

2. **`answer(query: str, chunks: list[CodeChunk]) -> dict`**
   - Build sources list from chunks: `sources = [chunk.path for chunk in chunks]`
   - Format context: `context = _format_context(chunks)`
   - Build prompt:
     ```python
     prompt = f"""You are a helpful assistant answering questions based on the provided context.

     Context:
     {context}

     Question: {query}

     Answer the question using ONLY the information from the context. If the context doesn't contain enough information, say so. Cite sources by referencing the file paths."""
     ```
   - POST to Claude API:
     ```json
     {
       "model": self.model,
       "max_tokens": 2048,
       "messages": [{"role": "user", "content": prompt}]
     }
     ```
   - Headers: `{"x-api-key": self.api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}`
   - Extract response:
     ```python
     answer_text = response.json()["content"][0]["text"]
     input_tokens = response.json()["usage"]["input_tokens"]
     output_tokens = response.json()["usage"]["output_tokens"]
     ```
   - Calculate cost:
     ```python
     cost_usd = (input_tokens * 0.001 + output_tokens * 0.005) / 1000
     ```
   - Return:
     ```python
     {
       "answer": answer_text,
       "sources": sources,
       "model_used": self.model,
       "cost_tokens": {"input": input_tokens, "output": output_tokens},
       "cost_usd": cost_usd,
       "duration_ms": duration_ms  # measure with time.time()
     }
     ```

3. **`_format_context(chunks: list[CodeChunk]) -> str`**
   - Format each chunk:
     ```
     --- Chunk 1: {chunk.path} (L{chunk.start_line}-L{chunk.end_line}, score={chunk.score if hasattr(chunk, 'score') else 'N/A'}) ---
     {chunk.content}

     --- Chunk 2: ... ---
     {chunk.content}
     ```
   - Return concatenated string

---

### test_bok_services.py (6 tests)

**Test cases (mock Voyage API and DB):**
- Test `generate_embedding()` with mocked API response
- Test `generate_embedding()` raises ValueError when VOYAGE_API_KEY not set
- Test `search_bok()` returns matching entries (mock DB with 3 BOK entries)
- Test `search_bok()` returns empty list when no matches
- Test `format_bok_for_prompt()` produces correct markdown format
- Test `enrich_prompt()` appends BOK section to base prompt

---

### test_synthesizer.py (6 tests)

**Test cases (mock Claude API):**
- Test `answer()` with mocked Claude API response
- Test `_format_context()` produces correct format for 3 chunks
- Test cost calculation (input=1000, output=500 → cost_usd ≈ $0.0035)
- Test `answer()` raises ValueError when ANTHROPIC_API_KEY not set
- Test `answer()` handles API error gracefully
- Test duration_ms is measured correctly

---

### bok/__init__.py

Export all functions:
```python
__all__ = ["generate_embedding", "search_bok", "format_bok_for_prompt", "enrich_prompt"]
```

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/bok/ tests/hivenode/rag/test_synthesizer.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same keyword search, same Claude API client, same cost formula as platform/efemera
- [ ] TDD: tests written first
- [ ] 12+ tests total (6 BOK + 6 synthesizer)
- [ ] Environment variables: `VOYAGE_API_KEY` (required), `ANTHROPIC_API_KEY` (required), `RAG_MODEL` (default haiku)
- [ ] Token cost formula: `(input_tokens × 0.001 + output_tokens × 0.005) / 1000`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-121-RESPONSE.md`

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
