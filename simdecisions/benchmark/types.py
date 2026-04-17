"""
types
=====

Benchmark types and dataclasses.

TASK-BENCH-001 - Core types for benchmark infrastructure: BenchmarkTask,
BaselineResult, SimResult, EvalResult, BenchmarkResult.

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, asdict
- from datetime import datetime
- from typing import Any

Classes:
- BenchmarkTask: A single benchmark task to be executed.
- BaselineResult: Result from running a baseline track (no SimDecisions).
- SimResult: Result from running a SimDecisions-augmented track.
- EvalResult: Evaluation result for a benchmark task output.
- BenchmarkResult: Complete benchmark result combining task, execution, and evaluation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
