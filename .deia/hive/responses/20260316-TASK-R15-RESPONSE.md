# TASK-R15: Fix RAG Routes Returning 404 -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

## Files Modified

1. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py**
   - Line 5: Changed import from `from hivenode.rag import routes as rag_routes` to `from hivenode.routes import rag_routes`
   - Line 29: Removed prefix override (already has `/api/rag` in router definition)

2. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py**
   - Lines 145-172: Updated IndexRecord class to add missing optional fields:
     - Added `content_preview: str = ""` (preview of artifact content)
     - Added `char_count: int = 0` (number of characters)
     - Added `token_estimate: int = 0` (estimated token count)
     - Added `content_hash: str = ""` (SHA256 hash of content)
     - Added `engines: list[str] = Field(default_factory=list)` (embedding engines)

3. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py**
   - Lines 36-42: Fixed CCCMetadata instantiation - changed field names from `coin_usd`, `carbon_kg` to `coin_usd_per_load`, `carbon_kg_per_load`
   - Lines 264-295: Fixed metadata object creation with correct field names:
     - ReliabilityMetrics: changed from `reliability_score`, `latency_ms`, `last_updated` to actual model fields
     - RelevanceMetrics: changed from `helpful_feedback`, `not_helpful_feedback` to `user_feedback_helpful`, `user_feedback_not_helpful`
     - StalenessInfo: changed from `indexed_at`, `modified_at`, `days_stale` to `content_hash`, `last_modified`, `last_indexed`, etc.
     - ProvenanceInfo: changed from `source`, `actor_id`, `node_id`, `indexed_by` to `created_by` only
   - Lines 297-321: Fixed IndexRecord instantiation with correct field names and values:
     - Added `content_preview=content[:500]`
     - Added `char_count=len(content)`
     - Added `token_estimate=len(content) // 4`
     - Added `content_hash=content_hash`
     - Added `engines=["tfidf"]`

4. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py**
   - Lines 545-549: Updated _row_to_record to include default values for `content_preview`, `char_count`, `token_estimate` (not stored in DB)

5. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py**
   - Lines 209-252: Modified rag_query function to:
     - Load chunks for each record from storage
     - Reconstruct `content_preview` from chunk contents
     - Populate `char_count` and `token_estimate` by summing chunks
     - Pass complete records to search_similar_chunks
   - Lines 133-143: Modified search_similar_chunks to generate pseudo-unique chunk IDs using artifact_id + chunk index

## What Was Done

1. **Identified Root Cause:** Two RAG routes modules existed:
   - `hivenode/rag/routes.py` (old, at `/rag/...` paths)
   - `hivenode/routes/rag_routes.py` (new, intended for `/api/rag/...` paths)
   - The __init__.py was importing the old module instead of the new one

2. **Fixed Route Registration:** Changed __init__.py to import the new `rag_routes.py` module which provides the expected `/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, `/api/rag/stats` endpoints

3. **Fixed Model Mismatches:** The indexer_service.py was creating records with field names that didn't match the model definitions:
   - CCCMetadata required `coin_usd_per_load` not `coin_usd`
   - ReliabilityMetrics/RelevanceMetrics had different field names
   - StalenessMetadata required `content_hash` and `last_modified`
   - ProvenanceMetadata only required `created_by`

4. **Added Missing Fields to Model:** IndexRecord was missing `content_preview`, `char_count`, `token_estimate`, `content_hash`, and `engines` fields used by storage layer

5. **Fixed Query Pipeline:**
   - Modified rag_query to load chunks and reconstruct content_preview from them
   - This is necessary because the database schema doesn't store content_preview (only stores chunk-level content)
   - The TFIDFEmbedder is fitted on the reconstructed full content previews

6. **Fixed Chunk ID Generation:** search_similar_chunks was expecting chunk.chunk_id but CodeChunk doesn't have this field. Generated pseudo-unique IDs using artifact_id + chunk index

## Test Results

**Before:** 13 failures in test_rag_routes.py (all endpoints returning 404)
**After:** 16/16 tests PASSING ✓

All tests passing:
- test_index_valid_folder ✓
- test_index_nonexistent_folder ✓
- test_index_empty_folder ✓
- test_query_returns_matching_chunks ✓
- test_query_empty_query ✓
- test_query_top_k_limit ✓
- test_query_empty_index ✓
- test_query_unicode ✓
- test_query_very_large_top_k ✓
- test_get_chunks_for_artifact ✓
- test_get_chunks_invalid_artifact_id ✓
- test_get_chunks_missing_artifact_id ✓
- test_stats_empty_index ✓
- test_stats_after_indexing ✓
- test_cosine_similarity ✓
- test_cosine_similarity_different_lengths ✓

## Acceptance Criteria

- [x] All RAG route tests pass (13+ tests) — **16/16 passing**
- [x] Routes accessible at correct API paths — `/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, `/api/rag/stats`
- [x] No import errors on hivenode startup
- [x] No regressions in other route tests

---

## Summary

The task was to fix RAG API routes returning 404 errors. The root cause was that the wrong RAG routes module was being imported in hivenode/routes/__init__.py. Additionally, there were model/field mismatches between the indexer_service.py code and the actual Pydantic model definitions that needed to be corrected.

All 16 RAG route tests now pass successfully. The API is fully functional with endpoints at `/api/rag/index`, `/api/rag/query`, `/api/rag/chunks`, and `/api/rag/stats`.
