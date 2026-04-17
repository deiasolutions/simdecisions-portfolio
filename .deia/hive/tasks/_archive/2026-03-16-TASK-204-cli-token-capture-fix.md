# TASK-204: Fix CLI Token Capture from JSON Output

## Objective
Fix token extraction bug in claude_cli_subprocess.py that causes ProcessResult.usage to contain 0 tokens despite Claude Code JSON containing valid token counts.

## Context
**Current state:**
- Lines 366-421 in `claude_cli_subprocess.py` parse JSON output from `--output-format json`
- Code extracts `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`
- Code computes `total_input_tokens` and `total_output_tokens`
- Code creates `usage` dict with tokens, cost_usd, carbon_kg, model
- BUT: heartbeats show 0 for all tokens, build monitor shows $0.00

**Problem:** Token extraction logic exists but is NOT working correctly. Either:
1. JSON parsing fails silently
2. Extracted tokens are 0 because JSON structure is wrong
3. usage dict is created but not returned in ProcessResult

**Fix required:**
1. Add debug logging to verify JSON parsing extracts non-zero tokens
2. Verify usage dict is actually returned in ProcessResult (line 458+)
3. Test with real Claude Code JSON response to confirm extraction works

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (lines 366-421, JSON parsing)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (lines 76-89, ProcessResult dataclass)

## Deliverables

### 1. Add Debug Logging
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Changes:**
- Line ~370 (after `json_data = json.loads(output)`): Log `logger.debug(f"Claude Code JSON keys: {json_data.keys()}")`
- Line ~373 (after `usage_data = json_data.get("usage", {})`): Log `logger.debug(f"Usage data: {usage_data}")`
- Line ~380 (after computing total_input_tokens): Log `logger.debug(f"Extracted tokens: input={total_input_tokens}, output={total_output_tokens}")`
- Line ~393 (after creating usage dict): Log `logger.debug(f"ProcessResult.usage: {usage}")`

### 2. Verify ProcessResult Construction
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Check:** Line 458+ where `ProcessResult(...)` is created
- Ensure `usage=usage` is passed (not `usage=None`)
- If usage is only set when `total_input_tokens > 0 or total_output_tokens > 0`, this may cause 0-token responses to have `usage=None` — FIX: Always set usage if JSON parsing succeeds

### 3. Update _estimate_cost to Use rate_loader
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Current code:** Lines ~150-165 have hardcoded PRICING lookup
**Replace with:**
```python
from hivenode.config import compute_coin

def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
    """Estimate USD cost using centralized rate loader."""
    return compute_coin(self._get_model_id(), input_tokens, output_tokens)
```

### 4. Update _estimate_carbon to Use rate_loader
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Current code:** Lines ~167-175 have hardcoded carbon calculation
**Replace with:**
```python
from hivenode.config import compute_carbon

def _estimate_carbon(self, input_tokens: int, output_tokens: int) -> float:
    """Estimate carbon footprint using centralized rate loader."""
    return compute_carbon(input_tokens, output_tokens)
```

### 5. Remove Hardcoded PRICING Constant
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Delete:** Lines 49-56 (PRICING dict)
**Reason:** Now using centralized YAML config via rate_loader

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\cli\test_token_capture.py`

Minimum 5 tests (TDD — write tests first):

1. `test_json_parsing_extracts_tokens()` — Mock JSON response with valid token counts, verify ProcessResult.usage contains non-zero tokens
2. `test_json_parsing_zero_tokens()` — Mock JSON response with 0 tokens, verify ProcessResult.usage is still created (not None)
3. `test_json_parsing_with_cache()` — Mock JSON with cache_creation_input_tokens and cache_read_input_tokens, verify total_input_tokens = input + cache_creation + cache_read
4. `test_usage_dict_includes_model()` — Verify ProcessResult.usage["model"] matches model ID from _get_model_id()
5. `test_estimate_cost_uses_rate_loader()` — Verify _estimate_cost() returns correct USD based on rate_loader (not hardcoded PRICING)

**Example JSON response to test against:**
```json
{
  "result": "Task completed successfully.",
  "usage": {
    "input_tokens": 12450,
    "cache_creation_input_tokens": 2000,
    "cache_read_input_tokens": 500,
    "output_tokens": 3200
  },
  "duration_ms": 45000,
  "duration_api_ms": 42000,
  "num_turns": 3,
  "session_id": "test-session-123"
}
```

Expected extraction:
- total_input_tokens = 12450 + 2000 + 500 = 14950
- total_output_tokens = 3200
- cost_usd = compute_coin(model, 14950, 3200)
- carbon_kg = compute_carbon(14950, 3200)

## Constraints
- No file over 500 lines
- No stubs — all functions fully implemented
- Debug logging uses logger.debug() (not print)
- Must preserve existing JSON parsing structure (lines 366-421)
- PRICING constant removed after migration to rate_loader

## Acceptance Criteria
- [ ] Debug logging added at 4 locations (JSON keys, usage_data, extracted tokens, final usage dict)
- [ ] ProcessResult construction verified to pass `usage=usage` (not None)
- [ ] _estimate_cost() migrated to use rate_loader.compute_coin()
- [ ] _estimate_carbon() migrated to use rate_loader.compute_carbon()
- [ ] PRICING constant removed (lines 49-56)
- [ ] 5+ tests pass
- [ ] Test with real JSON response confirms non-zero token extraction

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-204-RESPONSE.md`

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
