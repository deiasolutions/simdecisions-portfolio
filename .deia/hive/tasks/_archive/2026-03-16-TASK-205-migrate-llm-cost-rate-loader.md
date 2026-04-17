# TASK-205: Migrate hivenode/llm/cost.py to Use rate_loader

## Objective
Replace hardcoded COST_PER_TOKEN dict in `hivenode/llm/cost.py` with centralized rate_loader module to eliminate duplication and ensure consistency.

## Context
Currently `hivenode/llm/cost.py` has hardcoded rates at lines 10-14:
```python
COST_PER_TOKEN = {
    "claude-haiku-4-5": {"input": 0.25e-6, "output": 1.25e-6},
    "claude-sonnet-4-5": {"input": 3e-6, "output": 15e-6},
    "claude-opus-4-6": {"input": 15e-6, "output": 75e-6},
}
```

These are **per-token** rates (USD), while the new YAML config uses **per-million-token** rates.

**Migration required:**
1. Remove COST_PER_TOKEN constant
2. Update `calculate_cost()` to use `rate_loader.compute_coin()`
3. Update `calculate_carbon()` to use `rate_loader.compute_carbon()`
4. Preserve existing `emit_llm_event()` interface (no signature changes)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` (lines 1-117)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\rate_loader.py` (after TASK-203 completes)

## Deliverables

### 1. Remove Hardcoded Constants
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py`

**Delete:**
- Lines 10-14 (COST_PER_TOKEN dict)
- Lines 16-17 (DEFAULT_COST)
- Lines 19-20 (CARBON_PER_TOKEN)

**Reason:** Now using centralized YAML config via rate_loader

### 2. Update calculate_cost()
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py`

**Current implementation:** Lines 23-44
```python
def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    # Find matching cost tier by model prefix
    cost_rates = DEFAULT_COST
    for model_prefix, rates in COST_PER_TOKEN.items():
        if model.startswith(model_prefix):
            cost_rates = rates
            break

    input_cost = input_tokens * cost_rates["input"]
    output_cost = output_tokens * cost_rates["output"]
    return input_cost + output_cost
```

**Replace with:**
```python
from hivenode.config import compute_coin

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate USD cost for LLM call using centralized rate loader.

    Args:
        model: Model ID (e.g., "claude-sonnet-4-5-20250929")
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        float: Total cost in USD
    """
    return compute_coin(model, input_tokens, output_tokens)
```

### 3. Update calculate_carbon()
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py`

**Current implementation:** Lines 47-57
```python
def calculate_carbon(total_tokens: int) -> float:
    return total_tokens * CARBON_PER_TOKEN
```

**Replace with:**
```python
from hivenode.config import compute_carbon as compute_carbon_internal

def calculate_carbon(total_tokens: int) -> float:
    """
    Calculate carbon footprint in kg CO2e using centralized rate loader.

    Args:
        total_tokens: Total tokens (input + output)

    Returns:
        float: Carbon footprint in kg CO2e
    """
    return compute_carbon_internal(total_tokens, 0)  # Pass total as input_tokens, 0 as output
```

**Note:** rate_loader.compute_carbon() takes (input_tokens, output_tokens), but this function takes total_tokens. Pass total as input, 0 as output to get same result.

### 4. Preserve emit_llm_event() Interface
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py`

**No changes required** to `emit_llm_event()` function (lines 60-116). It calls `calculate_cost()` and `calculate_carbon()`, which now use rate_loader internally.

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\llm\test_cost_migration.py`

Minimum 5 tests (TDD — write tests first):

1. `test_calculate_cost_opus()` — Verify calculate_cost("claude-opus-4-6", 1_000_000, 1_000_000) returns 90.0
2. `test_calculate_cost_sonnet()` — Verify calculate_cost("claude-sonnet-4-5-20250929", 500_000, 200_000) returns 4.5
3. `test_calculate_cost_haiku()` — Verify calculate_cost("claude-haiku-4-5-20251001", 1_000_000, 500_000) returns 2.8
4. `test_calculate_carbon()` — Verify calculate_carbon(1_000_000) returns 100.0
5. `test_emit_llm_event_cost_consistency()` — Verify emit_llm_event() writes Event Ledger entry with cost_usd matching calculate_cost() output

**Also run existing tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\llm\test_cost.py` (if it exists)
- All tests in `tests/hivenode/llm/` must pass after migration

## Constraints
- No file over 500 lines
- No stubs — all functions fully implemented
- No hardcoded rates after migration (except in tests)
- Preserve existing function signatures (no breaking changes)
- emit_llm_event() must still write to Event Ledger with cost_usd, cost_carbon

## Acceptance Criteria
- [ ] COST_PER_TOKEN constant removed
- [ ] DEFAULT_COST constant removed
- [ ] CARBON_PER_TOKEN constant removed
- [ ] calculate_cost() uses rate_loader.compute_coin()
- [ ] calculate_carbon() uses rate_loader.compute_carbon()
- [ ] emit_llm_event() still works (no signature changes)
- [ ] 5+ tests pass
- [ ] All existing tests in tests/hivenode/llm/ pass

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-205-RESPONSE.md`

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
