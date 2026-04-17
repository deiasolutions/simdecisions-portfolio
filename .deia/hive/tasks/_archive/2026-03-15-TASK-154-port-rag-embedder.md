# TASK-154: Port RAG TF-IDF Embedder Module

## Objective
Port the TF-IDF embedding engine that generates baseline embeddings for all artifacts using term frequency–inverse document frequency vectorization.

## Context
The TFIDFEmbedder class provides the universal baseline embedding per harness spec §7.1. Every artifact gets TF-IDF embedded automatically. This is a local, deterministic embedding that requires no external API calls.

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\embedder.py` (181 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py`

**Dependencies:**
- TASK-151 (models.py) must be complete
- scikit-learn is already installed (verified)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\embedder.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (from TASK-151)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py`
- [ ] Port TFIDFEmbedder class with methods:
  - `__init__(max_features)` — initialize with vocabulary size limit
  - `fit(documents)` — build vocabulary and compute IDF scores from corpus
  - `transform(text)` → list[float] — transform text into TF-IDF vector
  - `fit_transform(documents, current_doc)` → list[float] — fit and transform in one call
  - `create_embedding_record(vector)` → EmbeddingRecord — wrap vector in EmbeddingRecord
  - `_tokenize(text)` → list[str] — tokenizer with stopword removal
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` to export TFIDFEmbedder
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_embedder.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test fit() builds vocabulary from corpus
- [ ] Test fit() computes IDF scores correctly
- [ ] Test fit() selects top N features by document frequency
- [ ] Test transform() generates vector of correct length
- [ ] Test transform() on text not in vocabulary (zeros for unknown terms)
- [ ] Test transform() normalizes vectors (L2 norm = 1)
- [ ] Test fit_transform() convenience method
- [ ] Test create_embedding_record() wraps vector correctly
- [ ] Test _tokenize() lowercases text
- [ ] Test _tokenize() removes stopwords
- [ ] Test _tokenize() filters single-char tokens
- [ ] Test _tokenize() handles punctuation and special chars
- [ ] Test transform() raises ValueError if not fitted
- [ ] Edge cases:
  - Empty document list for fit()
  - Empty string for transform()
  - Single document corpus
  - Very large corpus (1000+ documents)
  - Unicode text
  - Code tokens (underscores, camelCase)

**Target test count:** 18+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_embedder.py -v
```

## Constraints
- No file over 500 lines (embedder.py is 181 lines, well under limit)
- No stubs — all methods fully implemented
- TDD: tests first
- Port verbatim — do NOT modify logic from platform
- Do NOT use scikit-learn's TfidfVectorizer — port the custom implementation from platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-154-RESPONSE.md`

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

---

**Priority:** P0.50
**Model:** haiku
**Estimated time:** 25 minutes
**Dependency:** TASK-151
