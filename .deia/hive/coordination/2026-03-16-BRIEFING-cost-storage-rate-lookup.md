# BRIEFING: Cost Storage Format + Model Rate Lookup Table

**Date:** 2026-03-16
**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-3004-SPE)
**To:** Q33N (Queen Coordinator)
**Model Assignment:** Sonnet
**Priority:** P1

---

## Objective

Define and implement:
1. **Three-currency cost storage** (CLOCK, COIN, CARBON) for every Event Ledger entry and heartbeat
2. **Model rate lookup table** in YAML config for computing COIN from token counts
3. **Token capture fixes** so CLI adapter actually extracts tokens from Claude Code JSON (currently returns 0)
4. **Heartbeat metadata** includes model + tokens so build monitor can display real costs

---

## Context

### Current State — BROKEN Token Tracking

**Problem 1: CLI adapter returns 0 tokens**
File: `hivenode/adapters/cli/claude_cli_subprocess.py`
Lines 366-421 contain JSON parsing logic that extracts `input_tokens` and `output_tokens` from Claude Code's `--output-format json` response. However:
- The extraction logic exists but is currently **not working correctly** — all heartbeats show 0 tokens
- Build monitor shows $0.00 for all dispatches because tokens are missing
- CCCMetadata.model_for_cost is often empty or hardcoded instead of coming from actual dispatch

**Problem 2: Event Ledger already has cost columns, but they're unused**
File: `hivenode/ledger/schema.py` (lines 40-45)
The schema has:
```sql
cost_tokens         INTEGER,
cost_usd            REAL,
cost_carbon         REAL,
cost_tokens_up      INTEGER,
cost_tokens_down    INTEGER
```

But only `hivenode/llm/cost.py` uses these columns (for terminal chat LLM calls). The CLI dispatch adapter does NOT write to Event Ledger.

**Problem 3: No centralized model rate lookup**
Two places define rates:
- `hivenode/adapters/cli/claude_cli_subprocess.py` lines 49-56 (PRICING dict)
- `hivenode/llm/cost.py` lines 10-14 (COST_PER_TOKEN dict)

Both are hardcoded in Python. No single source of truth. No YAML config.

---

## Files to Read First

**Cost/token tracking:**
- `hivenode/ledger/writer.py` (Event Ledger write interface)
- `hivenode/ledger/schema.py` (cost columns already exist)
- `hivenode/llm/cost.py` (calculate_cost, calculate_carbon, emit_llm_event)
- `hivenode/adapters/cli/claude_cli_subprocess.py` (lines 366-421: JSON parsing, usage extraction)

**Heartbeat flow:**
- `hivenode/routes/build_monitor.py` (HeartbeatPayload, BuildState)
- `hivenode/schemas.py` (CCCMetadata)
- `hivenode/rag/indexer/models.py` (CCCMetadata Pydantic model)

**Config:**
- No existing `hivenode/config/` directory — create it
- YAML config will go in `hivenode/config/model_rates.yml`

---

## Acceptance Criteria

### 1. Model Rate Lookup YAML (MANDATORY)

**Deliverable:** `hivenode/config/model_rates.yml`
Format:
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

**Deliverable:** `hivenode/config/rate_loader.py`
Functions:
- `load_model_rates() -> dict` — loads YAML, returns rates dict
- `get_rate(model: str) -> dict` — returns {"input_per_million": float, "output_per_million": float} or default
- `compute_coin(model: str, input_tokens: int, output_tokens: int) -> float` — USD
- `compute_carbon(input_tokens: int, output_tokens: int) -> float` — kg CO2e

### 2. Fix CLI Token Capture (MANDATORY)

**File:** `hivenode/adapters/cli/claude_cli_subprocess.py`

**Current bug:** Lines 366-421 parse JSON, but extracted tokens are NOT being propagated correctly. Heartbeats show 0 for all tokens.

**Fix required:**
1. Verify JSON parsing at lines 373-377 actually gets `input_tokens`, `output_tokens` from Claude Code response
2. Verify `usage` dict at lines 388-398 correctly computes total_input_tokens (input + cache_creation + cache_read)
3. **Add debug logging** to confirm parsed values before they're returned
4. Ensure `ProcessResult.usage` dict is populated with non-zero values when JSON output contains token data

**Expected result:** After fix, `ProcessResult.usage` contains:
```python
{
    "input_tokens": 12450,      # Non-zero
    "output_tokens": 3200,      # Non-zero
    "cost_usd": 0.085,          # Computed via rate_loader
    "carbon_kg": 0.0015,        # Computed via rate_loader
    "model": "claude-sonnet-4-5-20250929",  # Actual model from dispatch
    ...
}
```

### 3. Heartbeat Metadata Expansion

**File:** `hivenode/routes/build_monitor.py`

**Current HeartbeatPayload** (line 37-47):
```python
class HeartbeatPayload(BaseModel):
    task_id: str
    status: str
    model: Optional[str] = None
    message: Optional[str] = None
    tests_passed: Optional[int] = None
    tests_total: Optional[int] = None
    cost_usd: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    role: Optional[str] = None
```

**Already has the fields!** But they're not being populated correctly because CLI adapter returns 0 tokens.

**Fix:** Once CLI adapter token capture is fixed, verify heartbeats include:
- `model`: actual model string (not None, not empty)
- `input_tokens`: non-zero count
- `output_tokens`: non-zero count
- `cost_usd`: computed from rate_loader (not hardcoded)

### 4. CCCMetadata Consistency

**Files:** `hivenode/rag/indexer/models.py` (lines 46-54), `hivenode/schemas.py`

**Current CCCMetadata:**
```python
class CCCMetadata(BaseModel):
    clock_ms: int
    coin_usd: float
    carbon_kg: float
    token_estimate: int = 0
    model_for_cost: str = ""
```

**Required fix:**
- `model_for_cost` MUST come from actual dispatch (from ProcessResult.usage["model"])
- NEVER hardcoded as empty string or default
- Use `rate_loader.get_rate(model)` to compute coin_usd from token_estimate

### 5. Event Ledger Auto-Attach Cost

**File:** `hivenode/llm/router.py` (or new dispatcher integration)

**Requirement:** Every LLM call via CLI adapter MUST auto-attach cost to Event Ledger after completion.

**Flow:**
1. CLI adapter completes → returns ProcessResult with usage dict
2. Dispatcher extracts: model, input_tokens, output_tokens, cost_usd, carbon_kg
3. Dispatcher calls `ledger_writer.write_event(event_type="CLI_DISPATCH", cost_tokens_up=input_tokens, cost_tokens_down=output_tokens, cost_usd=cost_usd, cost_carbon=carbon_kg)`

**Note:** `hivenode/llm/cost.py:emit_llm_event()` already does this for terminal chat. Replicate the pattern for CLI dispatches.

### 6. Build Monitor Display

**File:** `hivenode/routes/build_monitor.py`

**Requirement:** Build monitor header shows real cumulative cost.

**Current logic** (lines 88-90):
```python
self.total_cost = data.get("total_cost", 0.0)
self.total_input_tokens = data.get("total_input_tokens", 0)
self.total_output_tokens = data.get("total_output_tokens", 0)
```

**Already implemented!** Just needs CLI adapter to send non-zero tokens in heartbeats.

**Expected display after fix:**
```
Total Cost: $1.23 | Tokens: 45,600 in / 12,300 out | Tasks: 8
```

---

## Test Requirements

**Minimum 10 tests:**

1. `test_load_model_rates()` — loads YAML, returns dict
2. `test_get_rate_opus()` — returns correct Opus rates
3. `test_get_rate_sonnet()` — returns correct Sonnet rates
4. `test_get_rate_haiku()` — returns correct Haiku rates
5. `test_get_rate_unknown_fallback()` — returns default for unknown model
6. `test_compute_coin_opus()` — USD calculation with Opus rates
7. `test_compute_coin_sonnet()` — USD calculation with Sonnet rates
8. `test_compute_carbon()` — kg CO2e from token count
9. `test_cli_token_capture_json_output()` — ProcessResult.usage contains non-zero tokens from real JSON response
10. `test_heartbeat_metadata_tokens()` — HeartbeatPayload includes model + tokens after dispatch

**Additional integration test:**
11. `test_event_ledger_cost_auto_attach()` — CLI dispatch writes Event Ledger entry with cost_usd, cost_carbon, cost_tokens_up, cost_tokens_down

---

## Constraints

- **TDD:** Tests first, then implementation
- **No hardcoded rates** in Python after YAML is added (migrate PRICING and COST_PER_TOKEN to use rate_loader)
- **No stubs:** Every function fully implemented
- **File size:** No file over 500 lines
- **YAML location:** `hivenode/config/model_rates.yml` (create hivenode/config/ if missing)

---

## Smoke Test

After implementation:

1. **Start hivenode:** `python -m hivenode.main`
2. **Dispatch a bee via CLI:** Queue runner dispatches TASK-XXX
3. **Check heartbeat in build monitor:** Should show model="claude-sonnet-4-5-20250929", input_tokens=12450, output_tokens=3200, cost_usd=0.085
4. **Check Event Ledger:** SQLite query shows cost_usd, cost_carbon, cost_tokens_up, cost_tokens_down populated
5. **Build monitor header:** Shows "Total Cost: $0.09" (not $0.00)

---

## Critical Note: Token Capture is PRIORITY ZERO

The entire system depends on CLI adapter correctly extracting tokens from Claude Code JSON output. If this remains broken (returning 0), all downstream cost tracking fails.

**Debug steps for Q33N to verify:**
1. Add logging in `claude_cli_subprocess.py` at line 370 to print raw `json_data` dict
2. Add logging at line 383 to print `total_input_tokens` and `total_output_tokens` before creating usage dict
3. Run a test dispatch, check logs — if tokens are 0, JSON parsing is broken
4. If JSON parsing is correct but tokens still 0, check if `--output-format json` flag is actually being passed to Claude CLI (line 219)

---

## Response Requirements

When bees complete, response files MUST include:
1. **Files Modified** — every file created/modified
2. **Test Results** — 10+ tests passing
3. **Smoke Test Confirmation** — build monitor shows non-zero cost after test dispatch
4. **Clock / Cost / Carbon** — all three currencies tracked

---

## Final Checklist for Q33N

Before dispatching bees, verify task files include:
- [ ] YAML config schema defined
- [ ] rate_loader.py interface specified (4 functions)
- [ ] CLI adapter token capture fix (debug logging added)
- [ ] Event Ledger auto-attach pattern (replicate emit_llm_event)
- [ ] 10+ test cases listed with specific assertions
- [ ] Smoke test steps concrete and testable
- [ ] No hardcoded rates after migration
- [ ] CCCMetadata.model_for_cost never empty after fix

---

**Q33N: Break this into bee-sized tasks. Each task MUST include absolute file paths, TDD requirements, and specific acceptance criteria. Return task files for Q33NR review before dispatch.**
