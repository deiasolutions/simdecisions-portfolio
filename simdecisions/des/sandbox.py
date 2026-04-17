"""
sandbox
=======

DES Production Sandbox — SPEC-EXEC-01

Sandboxing for Python execution in production and sim modes.

Components:
    ALLOWED_FUNCTIONS  — allowlist of callable functions (production)
    SAFE_BUILTINS      — restricted builtins (sim mode)
    register_function  — add to allowlist
    execute_sandboxed  — call allowlisted function safely

Dependencies:
- from __future__ import annotations
- from typing import Any, Callable
- import math

Functions:
- register_function(name: str, func: Callable): Register a function in the allowlist.
- execute_sandboxed(func_name: str,
    args: list,
    kwargs: dict,
    ctx: dict): Execute an allowlisted function with given arguments.
- list_sum(items): Safe sum function for lists.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
