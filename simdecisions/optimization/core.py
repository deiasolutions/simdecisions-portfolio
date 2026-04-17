"""
core
====

Pareto Core — Solution, Frontier, and Dominance Checking

Ported from platform/efemera/src/efemera/optimization/pareto.py
Split: core.py handles data structures and dominance logic.

Module size: ~430 lines (under 500 limit)

Dependencies:
- from __future__ import annotations
- import time
- from dataclasses import dataclass, field

Classes:
- ParetoSolution: A single evaluated point in objective space.
- ParetoFrontier: A set of ranked Pareto solutions with selection helpers.
- DominanceChecker: Static methods for Pareto dominance testing and ranking.

Functions:
- _parse_constraint(expr: str): Parse a constraint expression like '< 100' into (operator, value).
- _passes_constraints(sol: ParetoSolution, constraints: dict[str, str]): Check if a solution passes all the given constraints.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
