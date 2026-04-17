"""
test_pipeline_sim
=================

Tests for pipeline simulation endpoint (TASK-228).

DES runner for build pipeline — loads PHASE-IR flow, runs through
DES engine with statistical service times, returns throughput and
bottleneck analysis.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- client(): Create a TestClient for the FastAPI app.
- test_simulate_endpoint_returns_valid_response(client: TestClient): Test that /api/pipeline/simulate returns expected fields.
- test_simulate_throughput_increases_with_pool_size(client: TestClient): Test that throughput increases with pool size (up to a point).
- test_simulate_identifies_bottleneck(client: TestClient): Test that bottleneck_stage is a valid stage name.
- test_simulate_with_different_failure_rates(client: TestClient): Test simulation with varying failure rates.
- test_simulate_wip_distribution_sums_to_total(client: TestClient): Test that WIP distribution accounts for all tokens.
- test_simulate_optimal_pool_size_is_reasonable(client: TestClient): Test that optimal_pool_size recommendation is within reasonable bounds.
- test_simulate_with_zero_failure_rate(client: TestClient): Test simulation with no failures.
- test_simulate_with_small_num_specs(client: TestClient): Test simulation with minimal number of specs.
- test_simulate_detects_pool_starvation(client: TestClient): Test that simulation detects when bee pool is undersized (bottleneck).
- test_simulate_handles_fix_cycles(client: TestClient): Test that simulation handles fix cycles (high failure rate scenario).
- test_simulate_budget_exhaustion(client: TestClient): Test that simulation handles budget exhaustion (max_tokens limit).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
