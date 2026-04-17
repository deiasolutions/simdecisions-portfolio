# TASK-R06: Fix RAG indexer_service.py imports + storage.py methods

**Priority:** P0.30
**Original:** TASK-156 (RAG indexer service port)
**Rebuild Batch:** 02
**Date:** 2026-03-15

---

## Objective

Restore lost import fixes and model schema alignments in `indexer_service.py`, add missing public methods to `storage.py`, and fix test assertions to match actual model schema.

---

## Context

After `git reset --hard HEAD`, the RAG indexer service lost critical repairs from TASK-156:
- Import statements using non-existent modules (`hivenode.rag.chunkers`, `hivenode.rag.embedder`)
- Model field usage mismatches (wrong enum values, missing required fields, non-existent metadata fields)
- Missing storage API methods (`get_chunks()`, `get_embeddings()`, `limit` parameter)
- Test assertions expecting wrong field names

The indexer_service.py file currently has broken imports and will fail when tests run.

**Dependencies:**
- This task depends on TASK-R02, R03, R04, R05 from Batch 01 completing first (needs correct `__init__.py` exports)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (current broken state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (authoritative schema definitions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_indexer_service.py` (broken tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-156-RESPONSE.md` (what was done originally)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1418-BEE-HAIKU-2026-03-15-TASK-156-PORT-RAG-INDEXER-SERVICE-RAW.txt` (raw bee output)

---

## Deliverables

### 1. Fix `indexer_service.py` Imports (Lines 17-18, 31)

- [ ] Line 17: Change `from hivenode.rag.chunkers import CodeChunk, chunk_file` to `from hivenode.rag.indexer.chunker import Chunker`
- [ ] Line 18: Change `from hivenode.rag.embedder import TFIDFEmbedder` to `from hivenode.rag.indexer.embedder import TFIDFEmbedder`
- [ ] Line 31: Change `from hivenode.rag.indexer.scanner import scan` to use `Scanner` class instead
- [ ] Fix all type hints using `CodeChunk` to use `Chunk` model from models.py

### 2. Fix `indexer_service.py` Model Field Usage

- [ ] Fix `StorageTier.WARM` → `StorageTier.EDGE` (EDGE tier exists in models.py, not WARM)
- [ ] Add missing required fields to `IndexRecord` creation: `content_preview`, `char_count`, `token_estimate`
- [ ] Fix `StalenessInfo` to use correct fields: `content_hash`, `last_modified` (not `indexed_at`, `modified_at`, `days_stale`)
- [ ] Fix `ProvenanceInfo` to use only `created_by` field (not `actor_id`, `node_id`, `source`, `indexed_by`)
- [ ] Fix `ReliabilityMetrics` fields: use `availability`, `hit_rate`, `failure_count`, `consecutive_failures` (per actual schema)
- [ ] Fix `RelevanceMetrics` fields: use `user_feedback_helpful`, `user_feedback_not_helpful` (not `helpful_feedback`, `not_helpful_feedback`)

### 3. Add CodeChunk-to-Chunk Conversion Method

- [ ] Create `_convert_code_chunks_to_chunks()` method to convert dataclass `CodeChunk` objects from chunker into Pydantic `Chunk` model objects
- [ ] Handle conversion of IR pairs (dicts) to `IRPair` model instances with proper status enum mapping

### 4. Fix IR Summary Computation

- [ ] Update `_compute_ir_summary()` to work with `Chunk` model objects (not `CodeChunk` dataclasses)
- [ ] Fix status field access: use `ir_pair.status.value` instead of `ir_pair.get("status", "UNTESTED")`
- [ ] Add `verification_rate` calculation per spec

### 5. Fix Storage Interaction

- [ ] Remove invalid kwargs from `storage.insert()` call (insert handles chunks and embeddings automatically from record)
- [ ] Fix content hash check: use `existing.staleness.content_hash` instead of `existing.content_hash`
- [ ] Add embeddings to `IndexRecord` as dict before storing

### 6. Fix Scanner Usage

- [ ] Change `scan(repo_path)` function call to use `Scanner` class: `Scanner(str(self.repo_path)).scan()`

### 7. Add Storage API Methods (`storage.py`)

- [ ] Implement `get_chunks(artifact_id: str) -> list[Chunk]` — retrieves chunks for an artifact
- [ ] Implement `get_embeddings(artifact_id: str) -> dict` — retrieves embeddings for an artifact
- [ ] Add optional `limit: int | None = None` parameter to `list_all()` method for pagination

### 8. Fix Test Suite (`test_indexer_service.py`)

- [ ] Update IR summary assertions: `verified_count` (not `verified`), etc.
- [ ] Fix provenance field assertions: remove non-existent `actor_id`, `node_id` fields
- [ ] Fix CCC metadata assertions: `coin_usd_per_load` (not `coin_usd`), `carbon_kg_per_load` (not `carbon_kg`)
- [ ] Fix staleness field assertions: use `record.staleness.content_hash` instead of `record.content_hash`

---

## Test Requirements

### Tests Written FIRST (TDD)
- [ ] Read existing test file `tests/hivenode/rag/indexer/test_indexer_service.py` first
- [ ] Fix all test assertions to match actual model schema BEFORE running tests

### All Tests Pass
- [ ] Run: `python -m pytest tests/hivenode/rag/indexer/test_indexer_service.py -v`
- [ ] Expected: **13 tests PASSING, 0 failures**

### Edge Cases Covered (Already in Test Suite)
- [ ] Two-pass indexing (scan → fit → index)
- [ ] Single file indexing (cold-start embedder)
- [ ] IR summary computation rollup
- [ ] CCC metadata attachment
- [ ] Provenance tracking
- [ ] Content hash staleness checking
- [ ] Re-indexing on content change
- [ ] Error handling (missing files, syntax errors)

---

## Constraints

- No file over 500 lines (indexer_service.py is ~440 lines, storage.py is ~530 lines currently — both within limits)
- No stubs (event emission is already stubbed with TODO per spec — that's acceptable)
- Use models from `hivenode.rag.indexer.models` as authoritative schema
- Do NOT modify models.py — it's the source of truth
- Refer to TASK-156-RESPONSE.md for exact field names and conversions

---

## Acceptance Criteria

- [x] All imports fixed (chunker, embedder, scanner)
- [x] All model field mismatches corrected (StorageTier, StalenessInfo, ProvenanceInfo, ReliabilityMetrics, RelevanceMetrics)
- [x] CodeChunk-to-Chunk conversion method added
- [x] IR summary computation works with Chunk model objects
- [x] Storage interaction uses correct field paths
- [x] Scanner class usage (not module-level function)
- [x] Storage API methods added: `get_chunks()`, `get_embeddings()`, `list_all(limit=...)`
- [x] All 13 tests pass
- [x] No file over 500 lines
- [x] No stubs shipped (except event emission TODO — per spec)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R06-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Sonnet (complex multi-file repair with schema dependencies)
**Estimated Duration:** 20-30 minutes
**Depends On:** TASK-R02, R03, R04, R05 (Batch 01)
