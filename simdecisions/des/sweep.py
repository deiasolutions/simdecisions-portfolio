"""
sweep
=====

Parameter Sweep & Sensitivity Analysis — ADR-008, TASK-090.

Tools for systematically exploring parameter spaces and measuring
sensitivity of simulation outputs to input changes.

Components:
    SweepParameter       — one parameter to sweep (name, path, values)
    SweepConfig          — sweep experiment configuration
    SweepPoint           — results for a single parameter combination
    SweepResults         — aggregate sweep results with best_point / to_table
    parameter_sweep      — full factorial sweep over parameter combinations
    SensitivityResult    — one-at-a-time sensitivity measurement
    sensitivity_analysis — OAT sensitivity with elasticity and correlation

Pure Python — no external dependencies beyond the DES engine.

Dependencies:
- from __future__ import annotations
- import itertools
- import math
- from copy import deepcopy
- from dataclasses import dataclass, field
- from typing import Any
- from simdecisions.des.replication import (
- from simdecisions.phase_ir.primitives import Flow

Classes:
- SweepParameter: One parameter to vary during a sweep.
- SweepConfig: Configuration for a parameter sweep experiment.
- SweepPoint: Results for a single parameter combination.
- SweepResults: Aggregate results from a parameter sweep.
- SensitivityResult: Result of a one-at-a-time sensitivity analysis for one parameter.

Functions:
- _apply_parameter(flow: Flow, param: SweepParameter, value: Any): Apply a parameter value to a flow (in-place).
- _extract_metrics(rep_results: ReplicationResults, metric_names: list[str]): Extract named metrics from replication results.
- parameter_sweep(flow: Flow, config: SweepConfig): Run a parameter sweep over one or more parameters.
- _compute_elasticity(inputs: list[float], outputs: list[float], base_input: float): Compute point elasticity: (dY/Y) / (dX/X).
- _compute_correlation(x: list[float], y: list[float]): Pearson correlation coefficient between two lists.
- sensitivity_analysis(flow: Flow,
    parameters: list[SweepParameter],
    metric: str = "cycle_time",
    perturbation: float = 0.1,
    replications: int = 5,): One-at-a-time (OAT) sensitivity analysis.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
