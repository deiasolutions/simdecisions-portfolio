"""
edges
=====

DES Edge Evaluation Engine — ADR-008 / TASK-083

Edge evaluation logic for routing tokens through a flow graph.
Handles guard evaluation, fork/join/switch/any/repeat edge types.

Edge Types:
    then   — Sequential: single token proceeds to target
    fork   — Parallel split: token cloned to all outgoing fork edges
    join   — Parallel sync: wait for all incoming tokens before proceeding
    switch — Exclusive choice: first matching guard wins
    any    — Inclusive choice: all matching guards fire
    repeat — Loop: return if guard condition is true

Components:
    build_guard_context  — assemble evaluation context for guard expressions
    evaluate_guard       — evaluate a single guard expression (fail-closed)
    evaluate_edges       — evaluate a list of outgoing edges, return which fire
    select_weighted      — probabilistic edge selection by weight
    JoinState            — tracks arrival state at a single join node
    JoinTracker          — manages all join synchronization points

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from random import Random
- from simdecisions.phase_ir.expressions import parse_expression, evaluate

Classes:
- JoinState: Tracks tokens arriving at a single join synchronization point.
- JoinTracker: Tracks tokens arriving at join nodes for synchronization.

Functions:
- build_guard_context(token_properties: dict,
    variables: dict,
    sim_time: float,
    mode: str = "sim",): Build the evaluation context for guard expressions.
- evaluate_guard(guard: str | None, context: dict): Evaluate a guard expression. Returns True if guard passes.
- evaluate_edges(edges: list[dict],
    token_properties: dict,
    variables: dict,
    sim_time: float,
    mode: str = "sim",
    default_edge_type: str = "then",): Evaluate a list of outgoing edges and return which ones should fire.
- _evaluate_switch(switch_edges: list[dict], context: dict): Evaluate switch edges: first matching guard wins.
- select_weighted(edges: list[dict], rng: Random): Select one edge based on weights (for probabilistic routing).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
