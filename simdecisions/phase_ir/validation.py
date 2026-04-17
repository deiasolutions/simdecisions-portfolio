"""
validation
==========

PHASE-IR Validation Engine -- TASK-072

Multi-level validation for PHASE-IR flow graphs:
    1. Syntax   (V-1xx) -- structural correctness
    2. Semantic  (V-2xx) -- logical correctness
    3. Mode      (V-3xx) -- mode-specific rules (sim vs production)
    4. Governance (V-4xx) -- DEIA governance requirements

Dependencies:
- from __future__ import annotations
- from collections import deque
- from dataclasses import dataclass, field
- from .expressions import validate_expression
- from .node_types import get_node_type
- from .primitives import (

Classes:
- ValidationIssue: A single validation finding.
- ValidationResult: Aggregate result of a validation run.

Functions:
- validate_syntax(flow: Flow): Run structural / syntax checks on a Flow.
- _check_duration_non_negative(value: str | None,
    label: str,
    ref_id: str,
    issues: list[ValidationIssue],
    is_edge: bool = False,): Check that a duration string (e.g. '5m', '-3s') is non-negative.
- validate_semantics(flow: Flow): Run logical / semantic checks on a Flow.
- _find_node(flow: Flow, node_id: str): Run mode-specific checks (sim vs production).
- validate_governance(flow: Flow): Run DEIA governance checks on a Flow.
- validate_flow(flow: Flow,
    level: str = "semantic",
    mode: str = "sim",): Validate a Flow at the specified level.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
