"""
test_sandbox
============

Tests for DES Production Sandbox — SPEC-EXEC-01

Tests function allowlist, execute_sandboxed, and SAFE_BUILTINS.

Dependencies:
- from __future__ import annotations
- import pytest
- from simdecisions.des.sandbox import (

Functions:
- test_register_function_adds_to_allowlist(): Test register_function adds function to allowlist.
- test_register_function_overwrites_existing(): Test register_function can overwrite existing entry.
- test_execute_sandboxed_calls_allowlisted_function(): Test execute_sandboxed successfully calls allowlisted function.
- test_execute_sandboxed_with_kwargs(): Test execute_sandboxed passes kwargs correctly.
- test_execute_sandboxed_raises_for_non_allowlisted(): Test execute_sandboxed raises for non-allowlisted function.
- test_execute_sandboxed_with_context(): Test execute_sandboxed can access context variables.
- test_execute_sandboxed_handles_exceptions(): Test execute_sandboxed propagates exceptions from function.
- test_safe_builtins_includes_basics(): Test SAFE_BUILTINS includes basic safe functions.
- test_safe_builtins_excludes_dangerous(): Test SAFE_BUILTINS excludes dangerous functions.
- test_safe_builtins_can_execute_simple_code(): Test SAFE_BUILTINS is sufficient for simple computations.
- test_safe_builtins_blocks_import(): Test SAFE_BUILTINS blocks import statements.
- test_safe_builtins_blocks_eval(): Test SAFE_BUILTINS blocks eval().
- test_safe_builtins_blocks_file_operations(): Test SAFE_BUILTINS blocks file operations.
- test_allowlist_production_workflow(): Integration test: register function, call via execute_sandboxed.
- test_safe_builtins_sim_workflow(): Integration test: run simple code with SAFE_BUILTINS.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
