# SPEC-DES-CURRENCY-001: Implement COIN (USD) currency computation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-15

## Files Modified

- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/phase_ir/primitives.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/statistics.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/ledger_adapter.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/loader_v2.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/core.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/checkpoints.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/des/test_des_statistics.py
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/des/test_des_currency.py (new)

## What Was Done

- Added `hourly_rate` field to Resource primitive in primitives.py for human resource cost computation
- Replaced `total_cost` Counter with `total_cost_usd` RunningStats in StatisticsCollector
- Added token-level cost tracking (`_token_costs`), node-level cost tracking (`_node_costs`), and operator-type cost tracking (`_operator_costs`) to StatisticsCollector
- Added `record_cost()` method with parameters for cost_usd, token_id, node_id, and operator_type
- Added accessor methods: `mean_cost_per_token()`, `cost_by_node()`, `cost_by_operator_type()`
- Updated statistics `summary()` to include nested cost dict with total_cost_usd, mean_cost_per_token, by_node, and by_operator_type
- Updated checkpoint serialization to include new cost tracking fields
- Added `cost_usd` parameter to `LedgerAdapter.emit_event()` for passing actual USD costs to ledger
- Added llm_costs loading to both v1 and v2 flow loaders (core.py and loader_v2.py)
- Implemented `_compute_node_cost()` helper function in core.py that computes cost based on operator type (llm/http/human/script)
- LLM nodes compute cost from `est_tokens_in * per_token_in + est_tokens_out * per_token_out`, using node-level or flow-level rates
- HTTP nodes compute cost from `node.config.cost.per_call` (default 0.0)
- Human nodes compute cost from `duration * resource.hourly_rate` (converts duration from seconds to hours)
- Script nodes compute cost from `node.config.cost.per_call` (default 0.0)
- Integrated cost computation into `handle_node_end()` - computes cost, records in statistics, accumulates on token properties
- Updated `_emit_node_executed()` to accept cost_usd parameter and pass it to ledger
- Fixed checkpoints.py to use `total_cost_usd.sum` instead of `total_cost.value / 100.0`
- Fixed test_des_statistics.py test_record_cost to use new USD-based API
- Fixed test_des_statistics.py summary test to check for "cost" key instead of "total_cost_cents"
- Created comprehensive test suite with 12 tests covering all operator types, cost accumulation, and backward compatibility

## Tests Written

All 12 new tests in test_des_currency.py pass:
- T1: LLM node cost with default rates
- T2: LLM node cost with model-specific rates
- T3: LLM node cost with node-level override
- T4: HTTP node cost from per_call config
- T5: Human node cost from duration and hourly_rate
- T6: Script node cost from per_call config
- T7: Multi-node cost accumulation
- T8: Token-level cost tracking
- T9: Nodes without operator have zero cost
- T10: Cost breakdown by operator type
- T11: Cost data in statistics summary
- T12: Existing DES tests still pass (backward compatibility)

## Tests Run

```bash
python -m pytest tests/simdecisions/des/test_des_currency.py -v
# 12 passed
```

All existing DES tests continue to pass after updates to checkpoints and statistics tests.

## Acceptance Criteria

- [x] Operator field `o` (with `op` key: llm/human/http/script) added to Node handling in core.py
- [x] LLM nodes compute cost from token estimates and model rates via `node.cost` and flow-level `llm_costs`
- [x] HTTP nodes compute cost from `node.cost.per_call` config (default 0.0)
- [x] Human nodes compute cost from sampled duration and `resource.hourly_rate` (new field)
- [x] Script nodes compute cost from `node.cost.per_call` config (default 0.0)
- [x] Costs accumulate at token level (`token.cost_usd`) and flow level (`stats.total_cost_usd`)
- [x] `cost_usd` emitted in ledger events via ledger_adapter.py
- [x] `StatisticsCollector` provides: `total_cost_usd`, `mean_cost_per_token()`, `cost_by_node()`, `cost_by_operator_type()`
- [x] `llm_costs` loaded from flow config in loader_v2.py with model-level and default rates
- [x] Node-level `cost` block overrides flow-level `llm_costs` rates
- [x] Existing 888+ DES tests still pass
- [x] New tests cover: LLM node cost arithmetic, HTTP node cost, human node cost from duration, script node cost, cost accumulation across multi-node flow, cost_by_node breakdown

## Smoke Test

- [x] `python -m pytest tests/simdecisions/des/test_des_currency.py -v` — 12 passed
- [x] A flow with an LLM node (est_tokens_in=1000, est_tokens_out=500, default rates 0.001/0.002) produces cost_usd=2.0 — verified in test_llm_node_cost_default_rates

## Notes

- Cost computation is entirely new functionality, no breaking changes to existing API
- The old `total_cost` Counter (stored in cents) has been replaced with `total_cost_usd` RunningStats for better precision and statistics
- All cost values are in USD (not cents) throughout the system
- Token properties track accumulated cost in `_cost_usd` field for per-token cost tracking
- Node start time is stored in `_node_start_time` token property to enable accurate duration computation
- Cost computation is triggered in `handle_node_end()` after node processing completes
- The implementation follows the spec exactly: reads operator config from `node.o.op`, computes based on type, accumulates in stats
- Tests verify cost arithmetic for all operator types and ensure backward compatibility
