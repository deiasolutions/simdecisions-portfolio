# TASK-151: Port RAG Indexer Models

## Objective
Port Pydantic models for the RAG indexer from platform repo to shiftcenter, providing the foundational schema for all indexed artifacts.

## Context
This is the first task in porting the RAG indexer service. The models define the complete schema for indexed artifacts including artifact types, chunks, IR pairs, embeddings, and metadata (CCC, reliability, relevance, staleness, provenance).

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\models.py` (179 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`

All models must be ported verbatim from platform — no rewriting, no modifications. This is a direct port.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\models.py`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (minimal exports)
- [ ] Port all 17 Pydantic models:
  - ArtifactType (enum)
  - StorageTier (enum)
  - IRStatus (enum)
  - IRPair
  - Chunk
  - EmbeddingRecord
  - CCCMetadata
  - ReliabilityMetadata
  - RelevanceMetadata
  - StalenessMetadata
  - ProvenanceMetadata
  - IRSummary
  - IndexRecord
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_models.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test all enums have expected values
- [ ] Test Chunk creation with default UUIDs
- [ ] Test IRPair status defaults to UNTESTED
- [ ] Test IndexRecord with all required fields
- [ ] Test IndexRecord with optional fields omitted (defaults work)
- [ ] Test IndexRecord serialization (model_dump, model_dump_json)
- [ ] Edge cases:
  - Empty ir_pairs list
  - Empty chunks list
  - Empty embeddings dict
  - Large token_estimate values
  - Missing optional fields

**Target test count:** 15+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_models.py -v
```

## Constraints
- No file over 500 lines (models.py is 179 lines, well under limit)
- No stubs — all models fully implemented
- TDD: tests first
- Port verbatim — do NOT modify model definitions from platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-151-RESPONSE.md`

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
**Estimated time:** 20 minutes
