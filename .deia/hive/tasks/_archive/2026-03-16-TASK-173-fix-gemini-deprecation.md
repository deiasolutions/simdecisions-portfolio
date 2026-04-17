# TASK-173: Fix Gemini Adapter Deprecation Warning

## Objective
Update `hivenode/adapters/gemini.py` and `hivenode/adapters/cli/gemini_adapter.py` to use the new `google.genai` package instead of the deprecated `google.generativeai` package, eliminating the FutureWarning.

## Context
Google has deprecated the `google.generativeai` package in favor of the new `google.genai` package. During execution of w1-02-phase-ir-cli spec, a FutureWarning was emitted:

```
FutureWarning: All support for the `google.generativeai` package has ended.
It will no longer be receiving updates or bug fixes. Please switch to the
`google.genai` package as soon as possible.
```

The migration requires updating two files that use the deprecated package:
1. `hivenode/adapters/gemini.py` (88 lines) - BaseAdapter implementation
2. `hivenode/adapters/cli/gemini_adapter.py` (166 lines) - CLI adapter

Both files use the same API pattern:
- Import: `import google.generativeai as genai`
- Configure: `genai.configure(api_key=api_key)`
- Create model: `genai.GenerativeModel(model_name)`
- Generate: `model.generate_content(prompt, generation_config=...)`

You must research the new `google.genai` API to determine:
1. What is the new import statement?
2. Has the configuration method changed?
3. Has the model instantiation changed?
4. Has the content generation method changed?

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\gemini_adapter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\base.py` (to understand BaseAdapter contract)

## Deliverables
- [ ] Research new `google.genai` API (read docs/examples or use WebSearch if needed)
- [ ] Update import in `gemini.py` from `google.generativeai` to `google.genai`
- [ ] Update import in `gemini_adapter.py` from `google.generativeai` to `google.genai`
- [ ] Update all API calls to match new `google.genai` API (if API changed)
- [ ] Preserve all existing functionality (pricing, call(), estimate_cost() for gemini.py)
- [ ] Preserve all existing functionality (send_task(), check_health() for gemini_adapter.py)
- [ ] Write tests for GeminiAdapter (if none exist, create new test file)
- [ ] Write tests for GeminiCLIAdapter (if none exist, create new test file)
- [ ] Ensure FutureWarning is eliminated

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\test_gemini.py` if it doesn't exist
- [ ] Minimum 5 tests for GeminiAdapter:
  - `test_gemini_adapter_init` - verify initialization with API key and model
  - `test_gemini_adapter_call` - verify call() returns text response
  - `test_gemini_adapter_call_with_system` - verify system prompt handling
  - `test_gemini_adapter_estimate_cost_flash` - verify cost estimation for flash model
  - `test_gemini_adapter_estimate_cost_pro` - verify cost estimation for pro model
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\cli\test_gemini_adapter.py` if it doesn't exist
- [ ] Minimum 4 tests for GeminiCLIAdapter:
  - `test_cli_adapter_init` - verify initialization
  - `test_cli_adapter_start_stop_session` - verify session lifecycle
  - `test_cli_adapter_send_task` - verify task execution
  - `test_cli_adapter_check_health` - verify health check
- [ ] All tests use mocks/stubs for actual Gemini API calls (no real API calls in tests)
- [ ] All existing PHASE-IR tests still pass: 325/325
- [ ] No new warnings emitted

## Edge Cases
- API key missing (should raise ValueError)
- Model initialization failure (should raise RuntimeError)
- API call failure (should handle gracefully)
- Empty/None prompts
- System prompt with empty user prompt

## Constraints
- No file over 500 lines (gemini.py is 88, gemini_adapter.py is 166 — both safe)
- No refactoring beyond the deprecation fix
- No feature additions
- Preserve all public interfaces (BaseAdapter contract must remain unchanged)
- No stubs
- TDD: tests first, then implementation

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-173-RESPONSE.md`

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

## Verification Steps
After completing implementation:
1. Run `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode && python -m pytest tests/hivenode/adapters/test_gemini.py -v`
2. Run `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode && python -m pytest tests/hivenode/adapters/cli/test_gemini_adapter.py -v`
3. Run `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine && python -m pytest tests/engine/phase_ir/ -v` (verify PHASE-IR tests still pass: 325/325)
4. Verify no FutureWarning when importing GeminiAdapter
5. Run `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode && python -m pytest tests/ -v` to ensure no regressions

## Acceptance Criteria
- [ ] Import changed from `google.generativeai` to `google.genai` in both files
- [ ] FutureWarning eliminated (no warnings from gemini.py or gemini_adapter.py)
- [ ] All new tests pass (minimum 9 tests total: 5 for GeminiAdapter, 4 for GeminiCLIAdapter)
- [ ] All existing PHASE-IR tests still pass (325/325)
- [ ] GeminiAdapter public interface unchanged (BaseAdapter contract preserved)
- [ ] GeminiCLIAdapter public interface unchanged
- [ ] All functionality preserved (pricing, call, estimate_cost, send_task, check_health)
- [ ] No stubs shipped
- [ ] No files exceed 500 lines

## Notes
- This is a **library migration**, not a feature addition
- If the new `google.genai` API has significant breaking changes that would require extensive refactoring beyond simple import/call updates, **STOP and report to Q33N**
- The scope should remain narrow: update the import and minimal API changes only
- Use WebSearch or research to understand the new API if documentation is unclear
- Mock all Gemini API calls in tests (use `unittest.mock` or `pytest-mock`)
