# SPEC-DES-CURRENCY-002: Per-transition cost aggregation

## Priority
P1

## Depends On
SPEC-DES-CURRENCY-001

## Model Assignment
sonnet

## Objective

Add per-edge, per-path, and per-run cost aggregation to the DES engine. CURRENCY-001 computes cost per node; this spec aggregates those costs so you can answer "What does path A cost vs. path B?" Tokens accumulate CLOCK/COIN/CARBON as they traverse, edges track traversal counts and cost totals, and paths aggregate by unique node sequence. Statistics API provides edge/path queries and path comparison.

## Files to Read First

- simdecisions/des/core.py
- simdecisions/des/tokens.py
- simdecisions/des/statistics.py
- simdecisions/des/trace_writer.py
- simdecisions/des/edges.py
- simdecisions/des/ledger_adapter.py
- tests/simdecisions/des/test_des_engine.py

## Acceptance Criteria

- [ ] Token dataclass carries `cost_clock`, `cost_coin`, `cost_carbon` (cumulative) and `path_history` (list of node IDs visited)
- [ ] On `node_end`, token costs are incremented by node duration (clock), node cost_usd (coin), and node cost_carbon (carbon)
- [ ] EdgeStats dataclass tracks `traversal_count`, `total_clock`, `total_coin`, `total_carbon` per edge (keyed by "source->target")
- [ ] PathStats dataclass tracks `path_signature` (hash of node sequence), `count`, `total_clock/coin/carbon` per unique path
- [ ] On edge traversal, edge stats are incremented with token cost delta since last edge
- [ ] On token completion, path stats are updated and `run_completed` trace event emitted with full cost summary
- [ ] `edge_traversed` trace events emitted with cost snapshot payload
- [ ] Statistics API: `edge_stats()`, `edge_cost(edge_id)`, `hottest_edges(n)`, `most_expensive_edges(n)`
- [ ] Statistics API: `path_stats()`, `path_cost(sig)`, `most_common_paths(n)`, `most_expensive_paths(n)`
- [ ] Statistics API: `compare_paths(sig_a, sig_b)` returns cost deltas between two paths
- [ ] Branching flow test: two paths with different costs produce correct per-path aggregation and compare_paths shows delta
- [ ] Existing 888+ DES tests still pass (`python -m pytest tests/simdecisions/des/ -v`)
- [ ] New tests cover: single-path cost accumulation, branching path separation, edge traversal counts, path signature deduplication

## Smoke Test

- [ ] `python -m pytest tests/simdecisions/des/ -v` — all pass, 0 failures
- [ ] A branching flow (start→decision→[path_a|path_b]→end) with different node costs produces two distinct PathStats entries with correct mean costs

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Token cost fields are floats, not integers
- Path signature = deterministic hash of ordered node ID list (e.g. sha256 of joined string)
- Edge key format: "source_id->target_id"
- This spec depends on CURRENCY-001 for node-level cost_usd computation — if CURRENCY-001 has not landed, token.cost_coin will always be 0 but the aggregation machinery must still work correctly

## Files to Modify

- simdecisions/des/tokens.py
- simdecisions/des/statistics.py
- simdecisions/des/core.py
- simdecisions/des/trace_writer.py
- tests/simdecisions/des/test_des_currency_aggregation.py
