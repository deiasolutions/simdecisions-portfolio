"""
distributions
=============

Statistical Distribution Library for DES Engine (ADR-008, TASK-084).

Pure Python implementation using only `random.Random` and `math` stdlib.
No numpy/scipy dependencies. All distributions are deterministic given
the same Random instance.

14 distribution types + factory functions + RNG stream manager.

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass
- from random import Random
- from typing import Any
- import math

Classes:
- DistributionResult: Container for a single sample result with provenance metadata.
- BaseDistribution: Base class for all distributions.
- ConstantDistribution: Always returns the same value (degenerate distribution).
- UniformDistribution: Continuous uniform distribution on [min_val, max_val].
- TriangularDistribution: Triangular distribution on [min_val, max_val] with mode.
- ExponentialDistribution: Exponential distribution with given rate (lambda).
- PoissonDistribution: Poisson distribution using inverse transform (Knuth's algorithm).
- NormalDistribution: Normal (Gaussian) distribution.
- LogNormalDistribution: Log-normal distribution with parameters mu and sigma of the
- GammaDistribution: Gamma distribution with shape (alpha) and scale (beta).
- ErlangDistribution: Erlang distribution — sum of `shape` i.i.d. exponential(rate) variates.
- WeibullDistribution: Weibull distribution with shape (k) and scale (lambda).
- BetaDistribution: Beta distribution on [0, 1] with parameters alpha and beta.
- DiscreteDistribution: Discrete distribution — weighted random choice from a finite set.
- EmpiricalDistribution: Empirical distribution — random choice (with replacement) from

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
