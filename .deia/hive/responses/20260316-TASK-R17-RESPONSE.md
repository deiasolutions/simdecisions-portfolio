# TASK-R17: Register Phase NL routes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-16

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (added import and registration)

## What Was Done
- Discovered that `hivenode/routes/phase_nl_routes.py` already exists (13,500 bytes, created 2026-03-15)
- The route module is fully implemented with all required functionality:
  - POST `/api/phase/nl-to-ir` endpoint
  - Support for Anthropic (Claude) and OpenAI (GPT) models
  - API key resolution from request or environment variables
  - JSON extraction with markdown fence handling
  - PHASE-IR validation and error reporting
  - Cost calculation and metadata tracking
- The issue was simply that the route was not registered in `hivenode/routes/__init__.py`
- Added `phase_nl_routes` to the import statement on line 3
- Added `router.include_router(phase_nl_routes.router, tags=['phase-nl'])` on line 41
- All 15 tests now pass

## Test Results

**Command:** `python -m pytest tests/hivenode/test_phase_nl_routes.py -v`
**Duration:** 0.89 seconds
**Exit Code:** 0

**Summary:**
- ✅ 15 tests PASSED
- ❌ 0 tests FAILED
- ⏭️ 0 tests SKIPPED

**Tests passing:**
1. `test_nl_to_ir_valid_request_anthropic` — Valid Anthropic API call
2. `test_nl_to_ir_valid_request_openai` — Valid OpenAI API call
3. `test_nl_to_ir_empty_text` — 422 error for empty text
4. `test_nl_to_ir_whitespace_only_text` — 422 error for whitespace-only text
5. `test_nl_to_ir_llm_api_error` — 500 error on LLM API failure
6. `test_nl_to_ir_missing_api_key` — 401 error when API key missing
7. `test_nl_to_ir_llm_timeout` — 504 error on timeout
8. `test_nl_to_ir_malformed_json` — 422 error for invalid JSON
9. `test_nl_to_ir_invalid_flow_structure` — Validation errors for invalid PHASE-IR
10. `test_nl_to_ir_complex_flow` — Complex flows with multiple nodes/edges
11. `test_nl_to_ir_bpmn_gateway` — BPMN gateway flows with conditional edges
12. `test_nl_to_ir_with_api_key_override` — Custom API key override
13. `test_nl_to_ir_with_intent` — Intent field support
14. `test_nl_to_ir_json_in_markdown_fence` — JSON extraction from markdown fences
15. `test_nl_to_ir_cost_calculation` — Cost metadata calculation

## Acceptance Criteria

- [x] Route module exists: `hivenode/routes/phase_nl_routes.py` (13,500 bytes)
- [x] Route registered in `__init__.py` with `tags=['phase-nl']`
- [x] All 15 Phase NL route tests pass
- [x] No regressions: routes load successfully (`from hivenode.routes import create_router`)
- [x] `/api/phase/nl-to-ir` endpoint responds (not 404)

## Issues / Follow-ups

### Pre-existing Issue (not caused by this task)
When running broader phase_ir tests (`tests/engine/phase_ir/`), there are import errors related to RAG indexer service:
- `hivenode/rag/indexer/indexer_service.py:37` — CCCMetadata validation error
- Missing fields: `coin_usd_per_load`, `carbon_kg_per_load`, `token_estimate`
- This is tracked as **TASK-R14** (RAG models enum values fix)
- This error is NOT caused by registering phase_nl_routes
- Verified by successfully importing routes: `from hivenode.routes import create_router`

### No Follow-ups Required
The Phase NL routes are fully functional. All tests pass. No additional work needed for this task.

## Clock / Cost / Carbon

- **Session duration:** 8 minutes (from task start to response write)
- **Test execution time:** 0.89 seconds
- **Cost estimate:** $0.02 (read files, edit 1 file, run tests)
- **Carbon cost:** ~1g CO₂ (local test execution)

## Notes

The route module `phase_nl_routes.py` was created during the wave-2 rebuild and survived the git reset that deleted other files. It includes:
- Full LLM integration (Anthropic + OpenAI)
- Comprehensive error handling (401, 422, 500, 504 status codes)
- JSON extraction with markdown fence support
- PHASE-IR validation via `engine.phase_ir.schema.validate_flow_structure`
- Cost calculation via `hivenode.llm.cost.calculate_cost`
- API key resolution from request or environment variables

The fix was trivial: just adding two lines to `hivenode/routes/__init__.py` to register the existing router.
