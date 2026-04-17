"""
test_adapters
=============

Tests for DES Production Executor Adapters — SPEC-EXEC-01

Tests LLMAdapter protocol, DecisionRequest/Response, FileChannel, and DeciderRouter.

Dependencies:
- from __future__ import annotations
- import json
- import tempfile
- from datetime import datetime
- from pathlib import Path
- from simdecisions.des.adapters import (

Classes:
- MockLLMAdapter: Mock implementation of LLMAdapter for testing.
- MockChannel: Mock implementation of Channel protocol for testing.

Functions:
- test_llm_adapter_protocol_compliance(): Test that MockLLMAdapter satisfies the LLMAdapter protocol.
- test_llm_response_dataclass(): Test LLMResponse dataclass structure.
- test_decision_request_serialization(): Test DecisionRequest can be serialized to JSON.
- test_decision_response_dataclass(): Test DecisionResponse structure.
- test_file_channel_writes_prompt_file(): Test FileChannel writes decision request to file.
- test_file_channel_reads_yaml_frontmatter_response(): Test FileChannel reads response from YAML frontmatter.
- test_file_channel_receive_timeout(): Test FileChannel returns None on timeout.
- test_decider_router_picks_file_channel_by_default(): Test DeciderRouter defaults to FileChannel.
- test_decider_router_respects_preferred_channel(): Test DeciderRouter uses preferred_channel when specified.
- test_decider_router_respects_allowed_deciders(): Test DeciderRouter filters recipients by allowed_deciders.
- test_channel_protocol_compliance(): Test that MockChannel satisfies the Channel protocol.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
