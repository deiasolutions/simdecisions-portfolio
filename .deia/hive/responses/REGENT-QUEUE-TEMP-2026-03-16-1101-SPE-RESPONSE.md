# Q33NR REGENT REPORT: SPEC-fix-R15-rag-routes-404

**Status:** ✅ COMPLETE
**Priority:** P0.91
**Model:** Haiku 4.5
**Date:** 2026-03-16

---

## Spec Summary

Fix RAG routes returning 404 (13 test failures). Debug and fix route registration in `__init__.py` so `/api/rag/` endpoints respond correctly.

---

## Task Files Reviewed

✅ **TASK-R15:** `.deia/hive/tasks/2026-03-16-TASK-R15-fix-rag-routes-registration.md`

**Mechanical Review:**
- [x] Deliverables match spec
- [x] File paths absolute
- [x] Test requirements present (13+ tests)
- [N/A] CSS var(--sd-*)
- [x] No file over 500 lines
- [x] No stubs
- [x] Response template present

**APPROVED** — dispatched to BEE-HAIKU.

---

## What Was Delivered

**Root Cause:** Two RAG routes modules existed:
- `hivenode/rag/routes.py` (old, at `/rag/...` paths)
- `hivenode/routes/rag_routes.py` (new, at `/api/rag/...` paths)

The `__init__.py` was importing the old module instead of the new one.

**Fixes Applied:**

1. **Fixed route registration** (`hivenode/routes/__init__.py`)
   - Changed import from `hivenode.rag.routes` to `hivenode.routes.rag_routes`
   - Removed duplicate prefix override

2. **Fixed model mismatches** (`hivenode/rag/indexer/models.py`)
   - Added missing optional fields to `IndexRecord`: `content_preview`, `char_count`, `token_estimate`, `content_hash`, `engines`

3. **Fixed field naming** (`hivenode/rag/indexer/indexer_service.py`)
   - `CCCMetadata`: `coin_usd` → `coin_usd_per_load`
   - `ReliabilityMetrics`, `RelevanceMetrics`, `StalenessInfo`, `ProvenanceInfo`: corrected field names to match actual models

4. **Fixed query pipeline** (`hivenode/routes/rag_routes.py`)
   - Load chunks and reconstruct `content_preview` from database
   - Generate pseudo-unique chunk IDs using `artifact_id + chunk index`

5. **Updated storage layer** (`hivenode/rag/indexer/storage.py`)
   - Populate default values for `content_preview`, `char_count`, `token_estimate`

---

## Test Results

✅ **16/16 tests PASSING** (exceeded spec requirement of 13+)

```
test_index_valid_folder ✓
test_index_nonexistent_folder ✓
test_index_empty_folder ✓
test_query_returns_matching_chunks ✓
test_query_empty_query ✓
test_query_top_k_limit ✓
test_query_empty_index ✓
test_query_unicode ✓
test_query_very_large_top_k ✓
test_get_chunks_for_artifact ✓
test_get_chunks_invalid_artifact_id ✓
test_get_chunks_missing_artifact_id ✓
test_stats_empty_index ✓
test_stats_after_indexing ✓
test_cosine_similarity ✓
test_cosine_similarity_different_lengths ✓
```

**Regression Check:**
- ✅ DES routes: 22/22 passing
- ✅ Phase NL routes: 15/15 passing
- ✅ No import errors on startup

---

## Acceptance Criteria

- [x] All 13+ RAG route tests pass — **16/16 passing**
- [x] Routes accessible at `/api/rag/index`, `/query`, `/chunks`, `/stats`
- [x] No import errors on startup

---

## Files Modified (5 files)

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py`

---

## Issues / Notes

⚠️ **BEE response file incomplete** — missing sections:
- Section 4: Build Verification
- Section 7: Clock / Cost / Carbon
- Section 8: Issues / Follow-ups

However, all acceptance criteria met and tests pass. Approved under correction cycle rule (functional completion).

⚠️ **Gemini deprecation warning** — `google.generativeai` package deprecated, should migrate to `google.genai`. Not blocking. (See BL-173 or TASK-173 for fix.)

---

## Next Steps

1. Spec complete — TASK-R15 can be archived
2. Queue proceeds to next P0 fix spec
3. RAG routes now fully functional at `/api/rag/*`

---

**READY FOR Q88N REVIEW**
