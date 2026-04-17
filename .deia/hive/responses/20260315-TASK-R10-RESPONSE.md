# TASK-R10: Add 2 smoke tests to RAG routes test file -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_rag_routes.py` (modified: added TestQueryRoute class with 2 test methods)

## What Was Done

- Read existing test file to understand structure and patterns (uses TestClient fixture, consistent assertion styles)
- Reviewed TASK-163 response file to understand original test implementation details
- Added `TestQueryRoute` class to test file (after `TestResetRoute`, before `TestEmbedderUnavailable`)
- Added `test_query_endpoint_exists` method — verifies `/rag/query` endpoint responds with 200, 500, or 503 status codes
- Added `test_query_missing_query_param` method — validates that missing query parameter returns 422 or 400 validation error
- Corrected test payload format: `/query` endpoint expects query parameter in URL, not JSON body (per `hivenode/rag/routes.py` line 167-227)
- Ran full test suite: all 14 tests passed without failures

## Test Results

**Test File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_rag_routes.py`

**Test Run Output:**
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
collected 14 items

tests/hivenode/rag/test_rag_routes.py::TestStatusRoute::test_status_returns_200 PASSED
tests/hivenode/rag/test_rag_routes.py::TestIndexRoute::test_index_code PASSED
tests/hivenode/rag/test_rag_routes.py::TestIndexRoute::test_index_full_rebuild PASSED
tests/hivenode/rag/test_rag_routes.py::TestIngestChatRoute::test_ingest_messages PASSED
tests/hivenode/rag/test_rag_routes.py::TestIngestChatRoute::test_ingest_empty_messages PASSED
tests/hivenode/rag/test_rag_routes.py::TestSearchRoute::test_search_returns_results PASSED
tests/hivenode/rag/test_rag_routes.py::TestSearchRoute::test_search_with_source_filter PASSED
tests/hivenode/rag/test_rag_routes.py::TestSearchRoute::test_search_empty_query_rejected PASSED
tests/hivenode/rag/test_rag_routes.py::TestSearchRoute::test_search_missing_query_rejected PASSED
tests/hivenode/rag/test_rag_routes.py::TestResetRoute::test_reset_clears_index PASSED
tests/hivenode/rag/test_rag_routes.py::TestQueryRoute::test_query_endpoint_exists PASSED
tests/hivenode/rag/test_rag_routes.py::TestQueryRoute::test_query_missing_query_param PASSED
tests/hivenode/rag/test_rag_routes.py::TestEmbedderUnavailable::test_index_503_when_no_embedder PASSED
tests/hivenode/rag/test_rag_routes.py::TestEmbedderUnavailable::test_search_503_when_no_embedder PASSED

============================== 14 passed in 16.41s =============================
```

**Pass Count:** 14/14 (100%)
**Failures:** 0

## Build Verification

All tests passed with no failures or errors. Test file line count: 217 lines (well under 500 line limit).

Test breakdown:
- `TestStatusRoute` — 1 test ✓
- `TestIndexRoute` — 2 tests ✓
- `TestIngestChatRoute` — 2 tests ✓
- `TestSearchRoute` — 4 tests ✓
- `TestResetRoute` — 1 test ✓
- `TestQueryRoute` — 2 tests ✓ (NEW)
- `TestEmbedderUnavailable` — 2 tests ✓

## Acceptance Criteria

- [x] `TestQueryRoute` class added to test file
- [x] `test_query_endpoint_exists` method added (accepts 200, 500, or 503)
- [x] `test_query_missing_query_param` method added (expects 422 or 400)
- [x] All 14 tests pass (12 existing + 2 new)
- [x] No test file over 500 lines (217 lines)
- [x] Consistent style with existing tests
- [x] No modifications to existing tests

## Clock / Cost / Carbon

**Clock:** 10 minutes (file reading, test addition, payload format correction, test execution)
**Cost:** ~0.0003 USD (minimal API usage, local test execution)
**Carbon:** ~0.15g CO2e (10 min Haiku model execution at standard datacenter efficiency)

## Issues / Follow-ups

None. Both test methods added successfully and all 14 tests pass.

Key findings:
- The `/rag/query` endpoint expects query parameter in URL (`?query=...`), not JSON body
- Endpoint returns 500 when synthesizer is unavailable in test environment (acceptable for smoke test)
- Test file remains under 500 line limit with good separation of concerns across test classes
