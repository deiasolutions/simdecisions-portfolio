"""
test_des_checkpoints
====================

Tests for DES Checkpoint Manager — ADR-008 / TASK-086

State snapshot/restore for Alterverse branching: save complete simulation
state, restore from checkpoints, fork with modifications.

30+ tests covering save, restore, fork, branch comparison, queue
serialization, and edge cases.

Dependencies:
- from __future__ import annotations
- import time
- import uuid
- import pytest
- from simdecisions.des.core import (
- from simdecisions.des.tokens import TokenRegistry
- from simdecisions.des.resources import ResourceManager
- from simdecisions.des.distributions import RNGManager
- from simdecisions.des.statistics import StatisticsCollector
- from simdecisions.des.edges import JoinTracker

Classes:
- TestSave: Tests for CheckpointManager.save.
- TestRestore: Tests for CheckpointManager.restore.
- TestFork: Tests for CheckpointManager.fork.
- TestInventory: Tests for checkpoint inventory operations.
- TestQueueSerialization: Tests for event queue serialization/deserialization.
- TestRoundTrip: Round-trip save -> restore -> state matches.
- TestBranchComparison: Tests for BranchComparison and compare_branches.
- TestEdgeCases: Edge case and error handling tests.

Functions:
- _tid(): Build a linear flow: N0 -> N1 -> ... -> N(n-1).
- _single_node_flow(): A flow with one node and no edges.
- _make_state(flow: Flow | None = None, config: SimConfig | None = None): Build an EngineState from a flow.
- _make_full_components(): Create a set of all manager components for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
