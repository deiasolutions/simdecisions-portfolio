"""
collector
=========

Results collector and aggregator for benchmark suite.

TASK-BENCH-003 - Polls completed benchmark tasks, aggregates by benchmark
and track, computes statistics using Welford's algorithm, and prepares
data for publishing.

Dependencies:
- from __future__ import annotations
- import json
- import yaml
- from pathlib import Path
- from simdecisions.benchmark.types import BenchmarkResult
- from simdecisions.benchmark.metrics import extract_metric, recovery_rate
- from simdecisions.benchmark.significance import mann_whitney_u
- from simdecisions.des.statistics import RunningStats

Classes:
- ResultsCollector: Collects and aggregates benchmark results from results directory.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
