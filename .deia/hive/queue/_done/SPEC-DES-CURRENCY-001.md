# SPEC-DES-CURRENCY-001: Implement COIN (USD) currency computation

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Implement COIN (USD) currency computation in the DES engine. Currently `cost_usd` is hardcoded to 0.0 in ledger emission. This spec adds cost computation based on operator type (LLM, HTTP, human, script) so that every node execution emits a real USD cost to the ledger and statistics. Test cases T2/T5 use resources but test cost arithmetic only — do not assert on resource utilization (that requires SPEC-DES-RESOURCE-BINDING-001).

## Files to Read First

- simdecisions/des/core.py
- simdecisions/des/statistics.py
- simdecisions/des/ledger_adapter.py
- simdecisions/des/loader_v2.py
- simdecisions/phase_ir/primitives.py
- simdecisions/des/distributions.py
- tests/simdecisions/des/test_des_engine.py

## Acceptance Criteria

- [ ] Operator field `o` (with `op` key: llm/human/http/script) added to Node handling in core.py — this is NEW schema, not existing
- [ ] LLM nodes compute cost from token estimates and model rates via `node.cost` and flow-level `llm_costs`
- [ ] HTTP nodes compute cost from `node.cost.per_call` config (default 0.0)
- [ ] Human nodes compute cost from sampled duration and `resource.cost.hourly_rate` (new field alongside existing `cost_per_use`)
- [ ] Script nodes compute cost from `node.cost.per_call` config (default 0.0)
- [ ] Costs accumulate at token level (`token.cost_usd`) and flow level (`stats.total_cost_usd`)
- [ ] `cost_usd` emitted in ledger events (non-zero for costed nodes) via ledger_adapter.py
- [ ] `StatisticsCollector` provides: `total_cost_usd`, `mean_cost_per_token()`, `cost_by_node()`, `cost_by_operator_type()`
- [ ] `llm_costs` loaded from flow config in loader_v2.py with model-level and default rates
- [ ] Node-level `cost` block overrides flow-level `llm_costs` rates
- [ ] Existing 888 DES tests still pass (`python -m pytest tests/simdecisions/des/ -v`)
- [ ] New tests cover: LLM node cost arithmetic, HTTP node cost, human node cost from duration, script node cost, cost accumulation across multi-node flow, cost_by_node breakdown

## Smoke Test

- [ ] `python -m pytest tests/simdecisions/des/ -v` — all pass, 0 failures
- [ ] A flow with an LLM node (est_tokens_in=1000, est_tokens_out=500, default rates 0.001/0.002) produces cost_usd=0.002

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Cost computation goes in `handle_node_end()` in core.py
- Operator type detection reads `node.get("o", {}).get("op")` — if absent, node has no operator cost (default 0.0)
- Resource `cost.hourly_rate` is NEW — add alongside existing `cost_per_use` on Resource primitive
- T2/T5 test cost arithmetic from sampled duration only — do NOT assert on resource acquire/release behavior

## Files to Modify

- simdecisions/phase_ir/primitives.py
- simdecisions/des/core.py
- simdecisions/des/statistics.py
- simdecisions/des/ledger_adapter.py
- simdecisions/des/loader_v2.py
- tests/simdecisions/des/test_des_currency.py
