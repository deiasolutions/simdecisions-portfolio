"""
test_des_core
=============

Tests for DES Core Engine — ADR-008

TASK-080 — Discrete Event Simulation core: EventQueue, Clock, EngineState,
event handlers, stop conditions, and the main event loop.

30+ tests covering all core components.

Dependencies:
- from __future__ import annotations
- import uuid
- import pytest
- from simdecisions.des.core import (

Classes:
- TestEventQueue: Events at the same time are ordered by priority (lower first).
- TestSimulationClock: Linear flow A->B->C: only A is a source node.
- TestStopCondition: Single node flow: no outgoing edges, token should complete.
- TestProcessEvent: A->B->C: one token flows through 3 nodes in ~3.0 sim-time units.
- TestEventPriorities: Checkpoint restore is highest priority (0), statistics_collect is lowest (100).
- TestEdgeCases: sim_time exactly at warmup_time should NOT be past warmup.

Functions:
- _tid(): Build a linear flow: N0 -> N1 -> ... -> N(n-1).
- _fork_flow(): Build a forking flow: A -> B, A -> C.
- _single_node_flow(): A flow with one node and no edges (source + sink).
- _make_state(flow: dict, config: SimConfig | None = None): Quick helper to build a state from a flow.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
