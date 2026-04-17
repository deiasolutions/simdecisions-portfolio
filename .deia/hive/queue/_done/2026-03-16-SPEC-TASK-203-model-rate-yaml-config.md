# TASK-203: Model Rate YAML Config + Loader Module

## Objective
Create centralized YAML config for model pricing rates and Python loader module with rate lookup and cost computation functions.

## Context
Currently model rates are hardcoded in two places:
- `hivenode/adapters/cli/claude_cli_subprocess.py` lines 49-56 (PRICING dict)
- `hivenode/llm/cost.py` lines 10-14 (COST_PER_TOKEN dict)

This creates duplication and drift risk. Need single source of truth in YAML config.

The new config will be loaded by a rate_loader module that provides:
1. Rate lookup by model ID
2. USD cost computation from tokens
3. Carbon (kg CO2e) estimation from tokens

This module will be used by:
- CLI adapter (to compute cost in ProcessResult.usage)
- LLM cost module (to replace hardcoded COST_PER_TOKEN)
- Event Ledger auto-attach (to compute cost_usd, cost_carbon)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (lines 49-56, PRICING dict)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` (lines 10-14, COST_PER_TOKEN dict)

## Deliverables

### 1. YAML Config File
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\model_rates.yml`

```yaml
# Model rates per million tokens (USD)
rates:
  claude-opus-4-6:
    input_per_million: 15.00
    output_per_million: 75.00
  claude-sonnet-4-5-20250929:
    input_per_million: 3.00
    output_per_million: 15.00
  claude-haiku-4-5-20251001:
    input_per_million: 0.80
    output_per_million: 4.00
  gpt-4o:
    input_per_million: 2.50
    output_per_million: 10.00
  default:  # Fallback for unknown models
    input_per_million: 3.00
    output_per_million: 15.00

# Carbon estimate per million tokens (kg CO2e)
carbon_per_million_tokens: 100.0  # ~0.0001 kg per token
```

### 2. Rate Loader Module
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\rate_loader.py`

**Functions:**
1. `load_model_rates() -> dict` — loads YAML, returns rates dict, caches in memory
2. `get_rate(model: str) -> dict` — returns `{"input_per_million": float, "output_per_million": float}` or default
3. `compute_coin(model: str, input_tokens: int, output_tokens: int) -> float` — USD cost
4. `compute_carbon(input_tokens: int, output_tokens: int) -> float` — kg CO2e

**Implementation notes:**
- Cache loaded YAML in module-level variable to avoid re-reading on every call
- `get_rate()` should try exact match first, then prefix match (e.g., "claude-sonnet-4-5-xxx" matches "claude-sonnet-4-5-20250929")
- If no match, return "default" rates
- `compute_coin()` formula: `(input_tokens * input_rate / 1_000_000) + (output_tokens * output_rate / 1_000_000)`
- `compute_carbon()` formula: `(input_tokens + output_tokens) * carbon_rate / 1_000_000`

### 3. Create hivenode/config/ Directory
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\`

Create directory with `__init__.py` exporting rate_loader functions:
```python
"""Hivenode configuration module."""
from .rate_loader import load_model_rates, get_rate, compute_coin, compute_carbon

__all__ = ["load_model_rates", "get_rate", "compute_coin", "compute_carbon"]
```

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\config\test_rate_loader.py`

Minimum 8 tests (TDD — write tests first):

1. `test_load_model_rates()` — loads YAML, returns dict with "rates" and "carbon_per_million_tokens" keys
2. `test_get_rate_opus()` — returns {"input_per_million": 15.0, "output_per_million": 75.0}
3. `test_get_rate_sonnet()` — returns {"input_per_million": 3.0, "output_per_million": 15.0}
4. `test_get_rate_haiku()` — returns {"input_per_million": 0.8, "output_per_million": 4.0}
5. `test_get_rate_unknown_fallback()` — returns default for "unknown-model-xyz"
6. `test_compute_coin_opus()` — with 1M input + 1M output, returns (15 + 75) = 90.0
7. `test_compute_coin_sonnet()` — with 500K input + 200K output, returns (0.5 * 3) + (0.2 * 15) = 4.5
8. `test_compute_carbon()` — with 1M total tokens, returns 100.0

## Constraints
- No file over 500 lines
- No hardcoded rates in Python after YAML is created (except in tests)
- No stubs — all functions fully implemented
- YAML must be in `hivenode/config/`, not `_tools/` or `docs/`
- Use `pathlib.Path` for file access
- Cache loaded YAML in module-level variable (thread-safe)

## Acceptance Criteria
- [ ] YAML config created with 5 model rates + default + carbon rate
- [ ] rate_loader.py implements all 4 functions (no stubs)
- [ ] hivenode/config/__init__.py exports all 4 functions
- [ ] 8+ tests pass
- [ ] No hardcoded rates in rate_loader.py (only in YAML)
- [ ] Prefix matching works (e.g., "claude-sonnet-4-5-xxx" matches "claude-sonnet-4-5-20250929")

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-203-RESPONSE.md`

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
