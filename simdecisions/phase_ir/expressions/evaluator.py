"""
evaluator
=========

Raised during expression evaluation.

Dependencies:
- from __future__ import annotations
- import random
- import re
- from typing import Any
- from .types import (
- from .parser import ParseError

Classes:
- ExpressionError: Raised during expression evaluation.

Functions:
- _resolve_target_key(node: Any): Convert an Identifier or DotAccess AST node into a dotted string key.
- _get_from_context(key: str, context: dict): Resolve a dotted key against a context dict.
- _set_in_context(key: str, value: Any, context: dict): Set a value in the context using a dotted key.
- evaluate(ast: Any, context: dict): Evaluate an expression AST against a context dict.
- evaluate_mutation(ast: Any, context: dict): Evaluate a mutation AST against a context dict.
- validate_expression(source: str): Try to parse an expression and return success/failure.
- _collect_refs(ast: Any, refs: set[str]): Recursively collect all identifier/dot-access references from an AST.
- extract_references(source: str): Extract all variable/identifier references from an expression.
- eval_template(expr: str, context: dict): Evaluate expression, handling ${...} template wrapping.
- eval_guard(expr: str, entity: dict, context: dict | None = None): Evaluate edge guard expression. Returns bool.
- eval_action_value(expr: str, entity: dict, context: dict | None = None): Evaluate action value expression (handles ${...} templates).
- eval_score(expr: str, resource: dict, entity: dict, context: dict | None = None): Evaluate dispatch scoring expression.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
