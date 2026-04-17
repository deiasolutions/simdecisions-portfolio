"""
test_des_edges
==============

TDD tests for DES Edge Evaluation Engine — ADR-008 / TASK-083

Tests cover:
  - build_guard_context: context assembly from token props, variables, sim_time
  - evaluate_guard: true/false guards, None guard, invalid expression
  - evaluate_edges: then, fork, switch, any, repeat edge types
  - select_weighted: probabilistic edge selection
  - JoinTracker: register, arrival, merge, pending, get/set state

Dependencies:
- from __future__ import annotations
- from random import Random
- from simdecisions.des.edges import (

Classes:
- TestBuildGuardContext: Token properties appear in the context.
- TestEvaluateGuard: None guard is unconditional — returns True.
- TestEvaluateEdgesThen: All 'then' edges fire unconditionally.
- TestEvaluateEdgesFork: All 'fork' edges fire (parallel split).
- TestEvaluateEdgesSwitch: Switch returns only the first matching guard.
- TestEvaluateEdgesAny: 'any' fires all edges whose guard matches.
- TestEvaluateEdgesRepeat: 'repeat' fires when guard evaluates to True.
- TestEvaluateEdgesMixed: 'then' and 'switch' edges in the same list both evaluate.
- TestSelectWeighted: Empty edge list returns None.
- TestJoinTracker: register_join creates a tracking entry.
- TestEdgeEvaluationIntegration: Switch guard using 'now' special variable.

Functions:
- _edge(id: str = "e1",
    from_node: str = "A",
    to_node: str = "B",
    type: str = "then",
    guard: str | None = None,
    weight: int = 1,): Shortcut to create an edge dict with minimal boilerplate.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
