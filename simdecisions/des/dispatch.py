"""
dispatch
========

DES Resource Dispatch Algorithms — TASK-039

Implements dispatch strategies for selecting resources from pools:
- longest_idle: Select resource idle the longest
- scored: Weighted multi-factor scoring with expression evaluation
- matrix: Lookup table dispatch (entity_attr x resource_attr -> score)
- decision_tree: Rule-based dispatch with condition evaluation

Components:
    DispatchResult      — result of a dispatch decision with score breakdown
    DispatchAlgorithm   — base class for all dispatch algorithms
    LongestIdleDispatch — select resource idle the longest
    ScoredDispatch      — weighted multi-factor scoring
    MatrixDispatch      — lookup table dispatch
    DecisionTreeDispatch — rule-based dispatch tree
    create_dispatch     — factory function to create dispatch from config

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from typing import TYPE_CHECKING
- from simdecisions.phase_ir.expressions import parse_expression, evaluate

Classes:
- DispatchResult: Result of a dispatch decision.
- DispatchAlgorithm: Base class for dispatch algorithms.
- LongestIdleDispatch: Select the resource that has been idle the longest.
- ScoredDispatch: Weighted multi-factor scoring with expression evaluation.
- MatrixDispatch: Lookup table dispatch: entity_attr x resource_attr -> score.
- DecisionTreeDispatch: Rule-based dispatch: if/then/else tree.

Functions:
- create_dispatch(config: dict): Create a dispatch algorithm from IR config.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
