"""
test_factory_report_ops
=======================

Tests for factory_report.py ops manager metrics.

Tests cover:
1. Load profile calculation
2. Queue wait time calculation
3. Time analysis (estimated vs actual)
4. Concurrency factor
5. Enhanced currencies
6. Productivity metrics

Dependencies:
- import sys
- from datetime import datetime, timedelta
- from pathlib import Path
- import tempfile
- from factory_report import (

Functions:
- test_compute_load_timeline(): Test load timeline reconstruction from task timestamps.
- test_load_profile_peak_trough(): Test peak and trough load calculation.
- test_load_profile_zero_windows(): Test detection of zero-load windows.
- test_queue_wait_no_backlog(tmp_path): Test queue wait when backlog is empty.
- test_queue_wait_with_waiting(tmp_path): Test queue wait with specs waiting in backlog.
- test_time_analysis_no_estimates(): Test time analysis when no estimates available.
- test_time_analysis_with_estimates(): Test time analysis with schedule estimates.
- test_concurrency_sequential(): Test concurrency factor for sequential tasks.
- test_concurrency_parallel(): Test concurrency factor for parallel tasks.
- test_concurrency_bottleneck(): Test bottleneck identification.
- test_productivity_rework_detection(): Test detection of fix/rework tasks.
- test_productivity_throughput(): Test throughput calculation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
