"""
test_des_currency_aggregation
=============================

Tests for DES Currency Aggregation — SPEC-DES-CURRENCY-002

Per-edge, per-path, and per-run cost aggregation.
Tests token cost accumulation, edge traversal tracking, path signature deduplication,
and statistics API for edge/path queries.

Dependencies:
- from __future__ import annotations
- import hashlib
- from simdecisions.des.core import load_flow, run, SimConfig
- from simdecisions.des.statistics import StatisticsCollector

Functions:
- _path_signature(node_ids: list[str]): Compute deterministic hash of ordered node ID list.
- test_token_carries_cost_fields(): Token dataclass carries cost_clock, cost_coin, cost_carbon fields.
- test_token_cost_accumulates_across_nodes(): Token cost accumulates as it traverses multiple nodes.
- test_token_tracks_path_history(): Token tracks visited nodes in path_history.
- test_edge_stats_track_traversal_count(): EdgeStats tracks traversal_count per edge.
- test_edge_stats_accumulate_costs(): EdgeStats accumulates total_clock, total_coin, total_carbon.
- test_branching_flow_produces_distinct_path_stats(): Branching flow with different costs produces correct per-path aggregation.
- test_path_signature_deduplication(): Multiple tokens following same path share the same path signature.
- test_statistics_api_edge_cost(): Statistics API provides edge_cost(edge_id).
- test_statistics_api_hottest_edges(): Statistics API provides hottest_edges(n) returning top n by traversal count.
- test_statistics_api_most_expensive_edges(): Statistics API provides most_expensive_edges(n) returning top n by total cost.
- test_statistics_api_path_cost(): Statistics API provides path_cost(sig) returning total cost for a path.
- test_statistics_api_most_common_paths(): Statistics API provides most_common_paths(n) returning top n by count.
- test_statistics_api_most_expensive_paths(): Statistics API provides most_expensive_paths(n) returning top n by total cost.
- test_statistics_api_compare_paths(): Statistics API provides compare_paths(sig_a, sig_b) returning cost deltas.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
