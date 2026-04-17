"""
checkpoints
===========

Checkpoint Manager for DES Engine — ADR-008 / TASK-086

State snapshot/restore for Alterverse branching. Saves complete simulation
state, restores from checkpoints, forks with modifications.

Components:
    Checkpoint          — immutable snapshot of all simulation state
    CheckpointManager   — save, restore, fork, branch management
    BranchComparison    — comparison of two branch outcomes
    compare_branches    — produce a BranchComparison from two branches

Dependencies:
- from __future__ import annotations
- import copy
- import time
- import uuid
- from dataclasses import dataclass, field
- from simdecisions.des.core import (
- from simdecisions.des.tokens import TokenRegistry
- from simdecisions.des.resources import ResourceManager
- from simdecisions.des.distributions import RNGManager
- from simdecisions.des.statistics import StatisticsCollector

Classes:
- Checkpoint: Immutable snapshot of complete simulation state at a point in time.
- CheckpointManager: Manages simulation checkpoints for save, restore, and branching.
- BranchComparison: Comparison of statistics and variables between two branches.

Functions:
- compare_branches(stats_a: StatisticsCollector,
    stats_b: StatisticsCollector,
    vars_a: dict,
    vars_b: dict,
    branch_a: str,
    branch_b: str,
    fork_point: str,): Compare statistics from two branches.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
