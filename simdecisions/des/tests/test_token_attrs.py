"""
test_token_attrs
================

Tests for token attribute read/write access in production engine.

SPEC-ENG-TOKEN-ATTRS-001: Add token attribute read/write access to production
engine node execution so that PRISM-IR task nodes can read attributes like
`treatment`, `run_number`, and `branch` from the current token, and write new
attributes back.

Dependencies:
- from simdecisions.des.tokens import SimToken, TokenState, TokenRegistry
- from simdecisions.phase_ir.expressions.evaluator import evaluate
- from simdecisions.phase_ir.expressions.parser import parse_expression

Functions:
- test_token_initializes_with_empty_attrs(): Tokens should initialize with empty attributes dict.
- test_set_attr_stores_value(): set_attr should store a value in the token.
- test_get_attr_returns_value(): get_attr should retrieve a stored value.
- test_get_attr_returns_default_when_missing(): get_attr should return default when key doesn't exist.
- test_attrs_returns_full_dict(): attrs() should return the complete attributes dictionary.
- test_attrs_snapshot_is_copy_not_reference(): attrs() should return a copy, not a reference to internal storage.
- test_multiple_attrs_set_and_read(): Multiple attributes can be set and read independently.
- test_executor_context_includes_token(): Executor context should include live token reference.
- test_executor_context_includes_token_attrs_snapshot(): token_attrs in context should be a snapshot, not live reference.
- test_set_attr_in_executor_persists_to_next_node(): set_attr on token in one node should be readable by the next node.
- test_token_attrs_snapshot_does_not_mutate_token(): Mutating token_attrs snapshot should not affect the token.
- test_token_attrs_accessible_in_expression_evaluator(): Expression evaluator should have token in scope for guard expressions.
- test_treatment_attr_routes_decision_node_correctly(): Guard `token.treatment == 'opus_solo'` should evaluate correctly.
- test_run_number_attr_accessible_in_guard(): Guard `token.run_number <= 3` should evaluate correctly.
- test_attrs_survives_engine_checkpoint_restore(): Token attributes should survive checkpoint/restore cycle.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
