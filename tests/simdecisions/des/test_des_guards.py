"""
test_des_guards
===============

TDD tests for DES Engine Guard Evaluation — ADR-008

Tests verify that handle_node_end uses evaluate_edges to apply guard
conditions when routing tokens through the flow graph.

Covers:
  - Token follows unconditional edge (then/fork — existing behaviour)
  - Token follows edge when guard condition passes
  - Token does NOT follow edge when guard condition fails
  - Exclusive gateway (switch): first matching guard wins
  - Parallel gateway (fork): all edges fire, tokens sent to all targets

Dependencies:
- from __future__ import annotations
- from simdecisions.phase_ir.primitives import Edge, Flow, Node, Variable
- from simdecisions.des.core import (

Classes:
- TestUnconditionalEdge: Token follows a 'then' edge that has no guard.
- TestGuardPassesTokenFollows: Token follows a 'switch' edge whose guard evaluates to True.
- TestGuardFailsTokenBlocked: Token does NOT follow a 'switch' edge whose guard evaluates to False.
- TestExclusiveGateway: Switch: token follows first edge whose guard passes.
- TestParallelGateway: Fork: all outgoing fork edges fire (parallel split).
- TestMixedEdgeTypes: Node can have both 'then' and 'switch' edges; each evaluated independently.
- TestEndToEndWithGuards: Full simulation run: token routes via switch guard to correct sink.

Functions:
- _make_state(flow: Flow, sim_time: float = 0.0, mode: str = "sim"): Build a minimal EngineState for a given flow.
- _node_end_event(node_id: str,
    token_id: str = "tok-1",
    properties: dict | None = None,): Build a node_end event for a given node.
- _flow_with_edges(edges: list[Edge], variables: list[Variable] | None = None): Build a minimal Flow with the given edges (nodes inferred from edges).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
