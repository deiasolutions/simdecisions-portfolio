"""
statistics
==========

Statistics Collector for DES Engine — ADR-008, TASK-085.

Running statistics collection using Welford's algorithm for numerically
stable online mean/variance, time-weighted metrics for utilization tracking,
and comprehensive metric categories for simulation analysis.

Components:
    RunningStats          — Welford's online algorithm for mean/variance/std_dev
    TimeWeightedStat      — Time-weighted average (e.g., resource utilization)
    Counter               — Simple integer counter
    StatisticsCollector   — Main collector aggregating all metric categories

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field

Classes:
- RunningStats: Numerically stable online statistics using Welford's algorithm.
- TimeWeightedStat: Time-weighted average (e.g., resource utilization).
- Counter: Simple integer counter with increment and serialization.
- EdgeStats: Statistics for a single edge (source->target).
- PathStats: Statistics for a unique path (sequence of nodes).
- StatisticsCollector: Central statistics collector for a DES simulation run.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
