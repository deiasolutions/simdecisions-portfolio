"""
analyzer
========

Frontier Analyzer — Quality and Coverage Metrics

Ported from platform/efemera/src/efemera/optimization/pareto.py
Split: analyzer.py handles metric computations.

Metrics:
    spread()         -- range of each objective across frontier
    hypervolume()    -- hypervolume indicator (area/volume dominated)
    spacing()        -- average Euclidean distance between adjacent solutions
    trade_off_ratio() -- marginal rate of substitution between objectives

Module size: ~185 lines (under 500 limit)

Dependencies:
- from __future__ import annotations
- import math
- from typing import TYPE_CHECKING

Classes:
- FrontierAnalyzer: Metrics for evaluating a Pareto frontier's quality and coverage.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
