"""
test_des_statistics
===================

Tests for DES Statistics Collector — TASK-085.

35+ tests covering:
    - RunningStats (Welford's algorithm)
    - TimeWeightedStat (time-weighted averages)
    - Counter (simple integer counter)
    - StatisticsCollector (all recording methods, computed metrics, checkpoint)
    - Edge cases (zero sim_time, single observation, large datasets)
    - Welford accuracy verification against known variance

Dependencies:
- from __future__ import annotations
- import pytest
- from simdecisions.des.statistics import (

Classes:
- TestRunningStats: Tests for RunningStats using Welford's algorithm.
- TestTimeWeightedStat: Tests for TimeWeightedStat.
- TestCounter: Tests for Counter.
- TestStatisticsCollector: Tests for the main StatisticsCollector.
- TestWelfordAccuracy: Verify Welford's algorithm against Python's statistics module.
- TestEdgeCases: Edge cases for statistics collection.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
