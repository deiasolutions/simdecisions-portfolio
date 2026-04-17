"""
test_des_durations
==================

Tests for Distribution-Driven Node Durations — TASK-037

Tests for connecting the distribution library to node service times in the DES engine.
Verifies that handle_node_start() samples durations from node metadata instead of
using the hardcoded default of 1.0.

Dependencies:
- from __future__ import annotations
- from simdecisions.des.core import (
- from simdecisions.phase_ir.primitives import Edge, Flow, Node

Classes:
- TestDefaultDuration: Node with no duration config → duration = 1.0 (backward compatibility).
- TestConstantDuration: Node with constant duration config → duration = specified value.
- TestExponentialDuration: Node with exponential distribution → mean ~correct over samples.
- TestZeroFloor: Negative samples should be clamped to 0.0.
- TestExistingTestsStillPass: Verify that existing test_des_core.py tests still pass with the new implementation.

Functions:
- _make_state(flow: Flow, config: SimConfig | None = None): Quick helper to build a state from a flow.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
