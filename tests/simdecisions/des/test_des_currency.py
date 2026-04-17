"""
test_des_currency
=================

Tests for DES Currency (COIN/USD) Computation — SPEC-DES-CURRENCY-001

Test cost computation for LLM, HTTP, human, and script nodes.
Verify cost accumulation at token and flow level.

Dependencies:
- from __future__ import annotations
- from simdecisions.des.core import load_flow, run, SimConfig
- from simdecisions.des.statistics import StatisticsCollector
- from simdecisions.phase_ir.primitives import Flow, Node, Edge, Resource

Functions:
- test_llm_node_cost_default_rates(): T1: LLM node computes cost from token estimates and default rates.
- test_llm_node_cost_model_specific_rates(): T2: LLM node uses model-specific rates when available.
- test_llm_node_cost_node_override(): T3: Node-level cost config overrides flow-level rates.
- test_http_node_cost(): T4: HTTP node computes cost from per_call config.
- test_human_node_cost_from_duration(): T5: Human node computes cost from sampled duration and resource hourly_rate.
- test_script_node_cost(): T6: Script node computes cost from per_call config.
- test_multi_node_cost_accumulation(): T7: Costs accumulate across multiple nodes in a flow.
- test_token_cost_tracking(): T8: Token-level cost tracking accumulates across nodes.
- test_no_cost_when_no_operator(): T9: Nodes without operator field have zero cost.
- test_cost_breakdown_by_operator_type(): T10: cost_by_operator_type() provides correct breakdown.
- test_cost_in_statistics_summary(): T11: Cost data is included in statistics summary.
- test_existing_888_des_tests_still_pass(): T12: Verify existing DES tests are not broken by currency changes.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
