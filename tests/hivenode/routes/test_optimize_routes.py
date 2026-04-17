"""
test_optimize_routes
====================

Test suite for optimize API routes — TASK-CANVAS-005C-3

Tests for /api/des/sweep, /api/des/pareto, and /api/des/optimize endpoints.
TDD: tests written first, then implementation.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- simple_flow(): Minimal valid flow for testing.
- sweep_config(): Basic sweep configuration.
- pareto_points(): Sample points for Pareto frontier computation.
- execution_ledger(): Sample execution ledger for optimize endpoint.
- test_sweep_valid_config(simple_flow, sweep_config): POST /api/des/sweep with valid config returns 200 with results.
- test_sweep_empty_params(simple_flow): POST /api/des/sweep with empty parameters returns 400.
- test_sweep_returns_sweep_results(simple_flow, sweep_config): Verify SweepResults structure from sweep endpoint.
- test_pareto_two_objectives(pareto_points): POST /api/des/pareto with valid points returns 200.
- test_pareto_empty_points(): POST /api/des/pareto with empty points returns 400.
- test_pareto_frontier_non_dominated(pareto_points): Verify non-dominated flagging in Pareto response.
- test_pareto_single_objective(pareto_points): Edge case: Pareto with single objective degenerates to sorted list.
- test_optimize_suggestions(simple_flow, execution_ledger): POST /api/des/optimize with valid flow + ledger returns 200.
- test_optimize_empty_ledger(simple_flow): POST /api/des/optimize with empty ledger returns 400.
- test_optimize_returns_suggestions(simple_flow, execution_ledger): Verify suggestion structure from optimize endpoint.
- test_sweep_sensitivity(simple_flow): Sensitivity analysis endpoint (if added) works.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
