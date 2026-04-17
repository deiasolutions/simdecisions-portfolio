"""
executors
=========

DES Production Executors — SPEC-EXEC-01

Executor functions for running nodes in production mode.
Each executor takes (node, state, ctx) and returns a dict of outputs.

Components:
    ExecutorRegistry       — maps node types to executor functions
    execute_python_node    — runs Python code/functions
    execute_llm_node       — calls LLM adapters
    execute_decision_node  — creates decision requests
    execute_validate_node  — runs validation rules
    default_registry       — pre-populated registry

Dependencies:
- from __future__ import annotations
- import time
- from typing import Any, Callable, Optional

Classes:
- ExecutorRegistry: Registry mapping node type strings to executor callables.

Functions:
- execute_python_node(node: dict, state: Any, ctx: dict): Execute a Python node.
- execute_llm_node(node: dict, state: Any, ctx: dict): Execute an LLM node by calling the injected LLMAdapter.
- execute_decision_node(node: dict, state: Any, ctx: dict): Execute a decision node by creating a DecisionRequest.
- execute_validate_node(node: dict, state: Any, ctx: dict): Execute a validate node by checking rules against context.
- default_registry(): Create a registry pre-populated with core executors.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
