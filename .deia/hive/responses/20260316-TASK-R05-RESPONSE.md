# TASK-R05: Add TFIDFEmbedder and IndexStorage exports -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

## What Was Done

- Added import of `TFIDFEmbedder` from `hivenode.rag.indexer.embedder` (line 8)
- Added import of `compute_content_hash` and `IndexStorage` from `hivenode.rag.indexer.storage` (line 25)
- Updated `__all__` list to include three new exports in alphabetical order:
  - `IndexStorage` (line 34)
  - `TFIDFEmbedder` (line 44)
  - `compute_content_hash` (line 45)
- Verified all three classes can be imported directly from `hivenode.rag.indexer` package

## Test Results

**test_embedder.py:** 30 passed, 4 failed (pre-existing failures in `create_embedding_record` method, unrelated to exports)
**test_storage.py:** 18 passed, 0 failed
**All indexer tests:** 135 passed, 4 failed, 6 skipped

Import verification: SUCCESS - All three exports importable from `hivenode.rag.indexer`

## Build Verification

All storage tests pass (18/18). The 4 embedder test failures are pre-existing issues in the `TFIDFEmbedder.create_embedding_record()` method (missing required EmbeddingRecord fields: artifact_id, dimension, created_at), not caused by the export changes. The classes themselves are correctly exported and available via the public API.

## Acceptance Criteria

- [x] TFIDFEmbedder imported and exported from `hivenode/rag/indexer/__init__.py`
- [x] IndexStorage imported and exported from `hivenode/rag/indexer/__init__.py`
- [x] compute_content_hash imported and exported from `hivenode/rag/indexer/__init__.py`
- [x] `__all__` list updated with three new exports in alphabetical order
- [x] All storage tests pass (18/18)
- [x] Build verification complete
- [x] No regressions caused by this change

## Clock / Cost / Carbon

**Clock:** ~5 minutes
**Cost:** Minimal - simple import/export addition, no code generation
**Carbon:** Negligible - quick file edits, minimal test runs

## Issues / Follow-ups

None. Task complete. The 4 pre-existing embedder test failures (in `create_embedding_record`) should be addressed separately - they require adding missing fields to EmbeddingRecord creation, but are outside scope of this export task.
