"""
benchmark_events
================

Benchmark-specific event types for Event Ledger.

TASK-BENCH-005 - Defines event types for benchmark task lifecycle:
benchmark_task_start, benchmark_task_complete, benchmark_task_failed.

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, asdict
- from datetime import datetime
- from typing import Any

Classes:
- BenchmarkTaskStartEvent: Event emitted when a benchmark task starts execution.
- BenchmarkTaskCompleteEvent: Event emitted when a benchmark task completes successfully.
- BenchmarkTaskFailedEvent: Event emitted when a benchmark task fails.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
