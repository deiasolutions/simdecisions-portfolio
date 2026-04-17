"""
test_des_sweep
==============

Tests for DES Parameter Sweep & Sensitivity Analysis — ADR-008, TASK-090.

30+ tests covering:
  - SweepParameter: fields, defaults, custom param_type
  - SweepConfig: defaults, custom metrics, empty parameters
  - SweepPoint: construction, metrics dict
  - SweepResults: best_point minimize/maximize, to_table, summary, empty
  - parameter_sweep: single parameter, multiple values, full factorial
  - _apply_parameter: resource_capacity, variable, distribution_param
  - _extract_metrics: cycle_time, throughput, completions, empty
  - sensitivity_analysis: single parameter, empty values
  - SensitivityResult: elasticity, correlation fields
  - _compute_elasticity: positive, negative, zero input, zero output, single point
  - _compute_correlation: perfect positive, perfect negative, uncorrelated, constant, single
  - Edge cases: empty values, single value parameter, no parameters

Dependencies:
- from __future__ import annotations
- import uuid
- import pytest
- from simdecisions.des.replication import (
- from simdecisions.des.sweep import (
- from simdecisions.phase_ir.primitives import (

Functions:
- _tid(): Build a linear flow: N0 -> N1 -> ... -> N(n-1).
- _single_node_flow(): Build a single-node flow (source = sink).
- _flow_with_resources(): Build a flow with resources attached.
- _flow_with_variables(): Build a flow with variables.
- _flow_with_distributions(): Build a flow with distributions.
- _make_rep_results(stats_list: list[dict],
    tokens_list: list[int] | None = None,
    sim_times: list[float] | None = None,): Construct a ReplicationResults from raw stats dicts.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
