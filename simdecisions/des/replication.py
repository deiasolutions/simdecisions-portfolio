"""
replication
===========

Replication Manager for DES Engine — ADR-008, TASK-087.

Multiple independent simulation replications with confidence intervals,
warm-up detection (MSER-5), and variance reduction techniques (CRN,
antithetic variates).

Pure Python — uses only math, statistics, and random from stdlib.
NO scipy dependency; t-distribution critical values are computed via
Cornish-Fisher expansion and a rational approximation of the inverse
normal CDF (Abramowitz & Stegun 26.2.23).

Components:
    ReplicationConfig     — settings for multi-run experiments
    ConfidenceInterval    — CI result with relative precision
    confidence_interval   — compute CI from a list of sample means
    _t_critical           — t-critical value without scipy
    _norm_ppf             — inverse normal CDF approximation
    detect_warmup_mser    — MSER-5 warm-up truncation detection
    ReplicationResult     — single-run output
    ReplicationResults    — aggregate output with CIs
    run_replications      — orchestrate multiple independent runs
    PairedComparison      — CRN comparison result
    compare_configs_paired — compare two configs using CRN

Dependencies:
- from __future__ import annotations
- import math
- import statistics as stats_module
- from dataclasses import dataclass, field
- from random import Random
- from typing import Any
- from simdecisions.des.core import SimConfig, load_flow, run
- from simdecisions.phase_ir.primitives import Flow

Classes:
- ConfidenceInterval: Result of a confidence interval calculation.
- ReplicationConfig: Configuration for a multi-replication experiment.
- ReplicationResult: Output from a single simulation replication.
- ReplicationResults: Aggregate results across multiple replications, with CIs.
- PairedComparison: Result of a paired comparison between two configurations.

Functions:
- _norm_ppf(p: float): Approximate inverse normal CDF (rational approximation).
- _t_critical(confidence: float, df: int): Approximate t-critical value for a two-tailed confidence interval.
- confidence_interval(values: list[float], confidence: float = 0.95): Compute a confidence interval using the t-distribution.
- detect_warmup_mser(observations: list[float],
    batch_size: int = 5,
    max_truncate: float = 0.5,): MSER-5 warm-up detection.
- run_replications(flow: Flow, config: ReplicationConfig | None = None): Run multiple independent replications of a flow.
- compare_configs_paired(flow: Flow,
    config_a: dict,
    config_b: dict,
    n_replications: int = 10,
    seed: int = 42,
    metric: str = "cycle_time",
    confidence: float = 0.95,): Compare two configurations using Common Random Numbers.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
