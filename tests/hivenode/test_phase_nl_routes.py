"""
test_phase_nl_routes
====================

Tests for /api/phase/nl-to-ir endpoint (NL → PHASE-IR conversion).

Dependencies:
- import json
- import pytest
- from unittest.mock import patch, AsyncMock
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- mock_anthropic_response(): Mock successful Anthropic API response with PHASE-IR JSON.
- mock_openai_response(): Mock successful OpenAI API response with PHASE-IR JSON.
- test_nl_to_ir_valid_request_anthropic(mock_anthropic_response): Test valid NL request with Anthropic model returns PHASE-IR flow.
- test_nl_to_ir_valid_request_openai(mock_openai_response): Test valid NL request with OpenAI model returns PHASE-IR flow.
- test_nl_to_ir_empty_text(): Test empty text returns 422 error.
- test_nl_to_ir_whitespace_only_text(): Test whitespace-only text returns 422 error.
- test_nl_to_ir_llm_api_error(): Test LLM API error returns 500 with details.
- test_nl_to_ir_missing_api_key(): Test missing API key returns 401 error.
- test_nl_to_ir_llm_timeout(): Test LLM timeout returns 504 error.
- test_nl_to_ir_malformed_json(): Test malformed JSON from LLM returns validation error.
- test_nl_to_ir_invalid_flow_structure(): Test invalid PHASE-IR structure returns validation error.
- test_nl_to_ir_complex_flow(): Test complex flow with multiple nodes and edges.
- test_nl_to_ir_bpmn_gateway(): Test BPMN gateway flow generation.
- test_nl_to_ir_with_api_key_override(): Test request with custom API key override.
- test_nl_to_ir_with_intent(): Test request with intent field.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
