# TASK-112: TF-IDF Embedder

**Wave:** 1
**Model:** haiku
**Role:** bee
**Depends on:** None

---

## Objective

Add a TF-IDF embedder class to `hivenode/rag/embedder.py` for lightweight local embeddings without LLM API calls.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\embedder.py` (existing embedder — ADD TFIDFEmbedder class)
- Source file in `platform/efemera/src/efemera/indexer/embedder.py` (reference for TF-IDF formulas)

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\embedder.py` (ADD TFIDFEmbedder class)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_tfidf_embedder.py`

## Deliverables

### embedder.py — Add TFIDFEmbedder class (181 lines)

**Class:** `TFIDFEmbedder`

**Attributes:**
- `vocabulary: dict[str, int]` — word → index mapping (top N by document frequency)
- `idf: dict[str, float]` — word → IDF score
- `vocab_size: int` — default 500 (configurable)
- `stopwords: set[str]` — 25 common words to filter

**Stopwords list:**
```python
STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "should", "could", "may", "might", "must", "can", "of", "in", "on", "at", "to", "for", "with", "by", "from"}
```

**Methods:**

1. **`__init__(vocab_size: int = 500)`**
   - Initialize empty vocabulary and IDF dicts
   - Set vocab_size
   - Set stopwords

2. **`fit(documents: list[str]) -> None`**
   - Tokenize all documents (lowercase, split on whitespace, filter stopwords)
   - Count document frequency for each word
   - Select top `vocab_size` words by document frequency
   - Build vocabulary dict: `{word: index}`
   - Compute IDF for each word: `idf[word] = log(corpus_size / document_frequency)`
   - Use `math.log()` for natural logarithm

3. **`transform(documents: list[str]) -> list[list[float]]`**
   - For each document:
     - Tokenize (same as fit)
     - Count term frequency: `tf[word] = count / total_terms_in_doc`
     - Build vector: `vector[vocab[word]] = tf[word] * idf[word]`
     - L2 normalize vector: `v_normalized = v / ||v||`
   - Return list of vectors (one per document)

4. **`fit_transform(documents: list[str]) -> list[list[float]]`**
   - Call `fit(documents)`
   - Call `transform(documents)`
   - Return vectors

5. **`create_embedding_record(artifact_id: str, vector: list[float]) -> EmbeddingRecord`**
   - Import `EmbeddingRecord` from `hivenode.rag.indexer.models` (after TASK-110 completes)
   - Create EmbeddingRecord with engine="tfidf", dimension=len(vector), created_at=now
   - Return record

**Helper functions:**

6. **`_tokenize(text: str) -> list[str]`**
   - Lowercase
   - Regex split: `re.split(r'\W+', text)`
   - Filter stopwords
   - Filter empty strings
   - Return word list

7. **`_l2_normalize(vector: list[float]) -> list[float]`**
   - Compute norm: `||v|| = sqrt(sum(x^2 for x in vector))`
   - If norm == 0, return vector as-is
   - Else: return `[x / norm for x in vector]`

### test_tfidf_embedder.py (8+ tests)

**Test cases:**
- Test `fit()` builds vocabulary from 5 documents
- Test `transform()` produces vectors of correct dimension
- Test `fit_transform()` combines fit + transform
- Test L2 normalization (verify norm ≈ 1.0 for non-zero vectors)
- Test empty corpus handling (fit with empty list → raises ValueError or returns empty vocab)
- Test single document corpus (edge case)
- Test stopwords are filtered (verify "the", "a", "is" not in vocabulary)
- Test IDF formula: `log(corpus_size / doc_freq)` for known input
- Test `create_embedding_record()` returns valid EmbeddingRecord with engine="tfidf"

## Acceptance Criteria

- [ ] All listed files modified/created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/test_tfidf_embedder.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same TF-IDF formulas (TF = term_freq / total_terms, IDF = log(N / df), L2 norm) as platform/efemera
- [ ] TDD: tests written first
- [ ] 8+ tests covering fit, transform, L2 norm, empty corpus, single doc, stopwords, IDF formula

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-112-RESPONSE.md`

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
