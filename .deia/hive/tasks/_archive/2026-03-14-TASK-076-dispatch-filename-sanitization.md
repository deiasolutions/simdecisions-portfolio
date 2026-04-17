# TASK-076: Fix Dispatch Filename Sanitization for Model Names with Colons

## Objective

Fix the dispatch.py bug where model names containing colons (e.g., `ollama:llama3.1:8b`) produce invalid filenames on Windows, causing OSError when trying to write response files. Sanitize model names before embedding them in response filenames.

## Context

**Error observed:**
```
OSError: [Errno 22] Invalid argument: '...\20260313-1654-BEE-OLLAMA:LLAMA3.1:8B-QUEUE-TEMP-...-RAW.txt'
```

**Root cause:**
Line 314 in `dispatch.py` generates response filenames using:
```python
response_file = response_dir / f"{timestamp}-BEE-{model.upper()}-{task_id.upper()}-RAW.txt"
```

When `model = "ollama:llama3.1:8b"`, the `.upper()` call produces `OLLAMA:LLAMA3.1:8B`, embedding colons into the filename. Windows rejects colons in filenames (except for drive letters).

**Solution:**
Sanitize the model name before embedding it in the filename by replacing `:` with `-`.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (line ~314)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\test_dispatch_validation.py` (for test structure reference)

## Deliverables

- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\test_dispatch_filename_sanitization.py`
- [ ] Write 5+ tests covering:
  - Model name with colons (e.g., `ollama:llama3.1:8b`) → filename contains `OLLAMA-LLAMA3.1-8B`
  - Model name without colons (e.g., `haiku`) → filename contains `HAIKU`
  - Model name with multiple colons (e.g., `anthropic:claude:sonnet`) → filename contains `ANTHROPIC-CLAUDE-SONNET`
  - Edge case: model name with leading colon (e.g., `:model`) → sanitized correctly
  - Edge case: model name with trailing colon (e.g., `model:`) → sanitized correctly
- [ ] Fix `dispatch.py` line ~314 to sanitize model name before embedding in filename
- [ ] Ensure existing dispatch tests still pass
- [ ] Ensure no regressions in response file generation

## Test Requirements

- [ ] **Tests written FIRST (TDD)** — write all test cases before fixing dispatch.py
- [ ] All new tests pass after fix is applied
- [ ] All existing dispatch tests still pass
- [ ] Edge cases covered:
  - Single colon in model name
  - Multiple colons in model name
  - Leading/trailing colons
  - Model names without colons (regression test)
  - Empty model name (should not crash, even if unlikely)

**Test command:**
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch
python -m pytest tests/test_dispatch_filename_sanitization.py -v
python -m pytest tests/test_dispatch_validation.py -v
```

## Constraints

- **Only fix the filename sanitization** — do NOT refactor dispatch.py
- **Do not change the response file format** — only sanitize the model name portion
- No file over 500 lines
- No stubs — every test must be fully implemented
- Use unittest framework (consistent with existing dispatch tests)

## Acceptance Criteria

- [ ] Model name `ollama:llama3.1:8b` produces filename containing `OLLAMA-LLAMA3.1-8B` (not `OLLAMA:LLAMA3.1:8B`)
- [ ] Model name `haiku` produces filename containing `HAIKU` (no regression)
- [ ] Model name `anthropic:claude:sonnet` produces filename containing `ANTHROPIC-CLAUDE-SONNET`
- [ ] Leading/trailing colons are handled correctly (e.g., `:model` → `-MODEL`, `model:` → `MODEL-`)
- [ ] Empty model name does not crash (handled gracefully)
- [ ] All 5+ tests pass
- [ ] All existing dispatch tests still pass (`test_dispatch_validation.py`)
- [ ] No changes to response file format except model name sanitization

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-076-RESPONSE.md`

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

## Implementation Notes

**Recommended approach:**

1. **Write tests first** in `test_dispatch_filename_sanitization.py`:
   - Test the sanitization function directly (if extracted)
   - OR test that response filenames are generated correctly for various model names
   - Use `unittest.TestCase` and follow the pattern from `test_dispatch_validation.py`

2. **Fix dispatch.py**:
   - Line ~314: Replace `:` with `-` in the model name before embedding in filename
   - Example: `model_sanitized = model.replace(":", "-").upper()`
   - Use `model_sanitized` instead of `model.upper()` in the filename
   - Also update line ~321 where `bot_id` is generated (if it uses model name)

3. **Run tests** to verify:
   - New tests pass
   - Existing tests pass
   - No regressions

**Do NOT:**
- Extract a separate sanitization function (keep it inline for now)
- Refactor unrelated parts of dispatch.py
- Change the response file format beyond model name sanitization
- Skip writing tests first
