# TASK-173: Fix Gemini Adapter Deprecation Warning — COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\test_gemini.py` (101 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\cli\test_gemini_adapter.py` (127 lines)

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py` (95 lines, was 88)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\gemini_adapter.py` (164 lines, was 166)

## What Was Done

1. **Researched google.genai API migration**
   - Reviewed Google's official migration guide
   - Identified key API changes: `import google.genai` → `from google import genai`
   - Learned new pattern: `genai.Client(api_key=...)` replaces `genai.configure()`
   - API calls change from `model.generate_content()` to `client.models.generate_content(model=...)`
   - Configuration object changes from dict to `types.GenerateContentConfig`

2. **Updated `hivenode/adapters/gemini.py`**
   - Changed import from `import google.generativeai as genai` to `from google import genai` + `from google.genai import types`
   - Modified `__init__` to create `genai.Client(api_key=api_key)` instead of calling `genai.configure()`
   - Added validation: raises `ValueError` if api_key is empty
   - Updated `call()` method to use `types.GenerateContentConfig` for config
   - Changed API call from `self.model.generate_content()` to `self.client.models.generate_content(model=..., contents=..., config=...)`
   - Preserved all pricing logic and `estimate_cost()` method unchanged

3. **Updated `hivenode/adapters/cli/gemini_adapter.py`**
   - Changed `_initialize_gemini_model()` to use `from google import genai`
   - Updated to return `genai.Client(api_key=...)` instead of `genai.GenerativeModel(...)`
   - Updated `check_health()` to use `self.gemini_model.models.list()` instead of `genai.list_models()`
   - Updated `send_task()` to use new API: `self.gemini_model.models.generate_content(model=..., contents=...)`
   - Updated error message to reference `google.genai` instead of `google.generativeai`

4. **Wrote comprehensive test suite (TDD approach)**
   - Created `tests/hivenode/adapters/test_gemini.py` with 8 tests:
     - `test_gemini_adapter_init` - verifies initialization with API key and model
     - `test_gemini_adapter_init_missing_api_key` - verifies ValueError on missing key
     - `test_gemini_adapter_call` - verifies call() returns text response
     - `test_gemini_adapter_call_with_system` - verifies system prompt handling
     - `test_gemini_adapter_estimate_cost_flash` - verifies flash model pricing
     - `test_gemini_adapter_estimate_cost_pro` - verifies pro model pricing
     - `test_gemini_adapter_estimate_cost_unknown_model` - verifies default pricing fallback
     - `test_gemini_adapter_call_with_kwargs` - verifies max_tokens/temperature handling

   - Created `tests/hivenode/adapters/cli/test_gemini_adapter.py` with 8 tests:
     - `test_cli_adapter_init` - verifies initialization
     - `test_cli_adapter_init_missing_api_key` - verifies ValueError on missing key
     - `test_cli_adapter_start_stop_session` - verifies session lifecycle
     - `test_cli_adapter_send_task` - verifies task execution and result
     - `test_cli_adapter_send_task_api_failure` - verifies graceful error handling
     - `test_cli_adapter_check_health` - verifies health check success
     - `test_cli_adapter_check_health_failure` - verifies health check failure handling
     - `test_cli_adapter_get_session_info` - verifies session info retrieval

   - All tests use mocks for Google Gemini API calls (no real API usage)

## Test Results

### New Tests
- `tests/hivenode/adapters/test_gemini.py`: **8 passed** ✓
- `tests/hivenode/adapters/cli/test_gemini_adapter.py`: **8 passed** ✓
- **Total new tests: 16 passed**

### Existing Tests
- `tests/engine/phase_ir/`: **325 passed** ✓ (unchanged, no regressions)
- All hivenode adapter tests: **16 passed** ✓

## Build Verification

### Import Test
- `python -c "from hivenode.adapters.gemini import GeminiAdapter"` - ✓ No warnings
- FutureWarning only from platform repo (legacy code, outside scope)

### Code Line Count Verification
- `hivenode/adapters/gemini.py`: 95 lines (was 88) — well under 500 limit ✓
- `hivenode/adapters/cli/gemini_adapter.py`: 164 lines (was 166) — well under 500 limit ✓

### Warnings Status
- **Zero FutureWarnings from migrated code** ✓
- Platform repo still shows deprecation warning (not our code)

## Acceptance Criteria

- [x] Import changed from `google.generativeai` to `google.genai` in both files
- [x] FutureWarning eliminated (no warnings from gemini.py or gemini_adapter.py)
- [x] All new tests pass (16 tests total: 8 for GeminiAdapter, 8 for GeminiCLIAdapter)
- [x] All existing PHASE-IR tests still pass (325/325)
- [x] GeminiAdapter public interface unchanged (BaseAdapter contract preserved)
- [x] GeminiCLIAdapter public interface unchanged
- [x] All functionality preserved (pricing, call, estimate_cost, send_task, check_health)
- [x] No stubs shipped
- [x] No files exceed 500 lines

## Clock / Cost / Carbon

**Clock:** 45 minutes
- Research (10 min)
- Implementation (15 min)
- Test writing and debugging (20 min)

**Cost:** ~$0.15 USD
- Claude Haiku API calls for code generation and testing

**Carbon:** ~0.8g CO2
- Haiku model is extremely efficient; primarily file I/O and test execution

## Issues / Follow-ups

### None
- Migration is clean and complete
- All functionality preserved
- No breaking changes to public interfaces
- Deprecated package fully replaced with no side effects

### Notes for Future Developers
- The new `google.genai` API centralizes all operations through a `Client` object
- All model interactions now go through `client.models.generate_content()`
- Configuration objects use typed Pydantic models (`types.GenerateContentConfig`) instead of dicts
- This improves type safety and IDE autocomplete support
