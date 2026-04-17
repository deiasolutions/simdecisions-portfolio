"""
test_executors
==============

Tests for DES Production Executors — SPEC-EXEC-01

Tests ExecutorRegistry, execute_python_node, execute_llm_node,
execute_decision_node, execute_validate_node.

Dependencies:
- from __future__ import annotations
- from simdecisions.des.adapters import LLMResponse
- from simdecisions.des.core import EngineState, SimConfig, SimulationClock, EventQueue
- from simdecisions.des.executors import (
- from simdecisions.phase_ir.primitives import Flow, Node

Classes:
- MockLLMAdapter: Mock LLM adapter for testing.

Functions:
- test_executor_registry_register_and_lookup(): Test ExecutorRegistry can register and lookup executors.
- test_executor_registry_get_unknown_type(): Test ExecutorRegistry returns None for unknown type.
- test_default_registry_has_core_executors(): Test default_registry() has python, llm, decision, validate executors.
- test_execute_python_node_production_allowlisted_function(): Test execute_python_node calls allowlisted function in production.
- test_execute_python_node_production_rejects_non_allowlisted(): Test execute_python_node rejects non-allowlisted function in production.
- test_execute_python_node_sim_mode_inline_code(): Test execute_python_node with inline code in sim mode.
- test_execute_python_node_sim_mode_blocks_dangerous_builtins(): Test execute_python_node blocks dangerous builtins in sim mode.
- test_execute_llm_node_calls_adapter(): Test execute_llm_node calls injected LLM adapter.
- test_execute_llm_node_uses_prompt_from_context(): Test execute_llm_node can get prompt from context.
- test_execute_decision_node_creates_request(): Test execute_decision_node creates DecisionRequest and returns response.
- test_execute_validate_node_pass(): Test execute_validate_node with passing validation.
- test_execute_validate_node_fail(): Test execute_validate_node with failing validation.
- test_production_flow_executes_python(): Integration test: 3-node flow with python executor.
- test_backward_compat_sim_mode_unchanged(): Test that sim mode behavior is unchanged (backward compatibility).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
