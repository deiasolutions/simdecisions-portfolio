"""
test_claude_cli_token_tracking
==============================

test_claude_cli_token_tracking.py

Tests for Claude Code CLI token tracking, cost calculation, and carbon estimation.

Dependencies:
- import json
- import pytest
- from unittest.mock import patch, MagicMock
- from hivenode.adapters.cli.claude_cli_subprocess import (

Classes:
- TestModelMapping: Test model ID mapping and retrieval.
- TestCostCalculation: Test cost calculation using rate cards.
- TestCarbonCalculation: Test carbon emissions estimation.
- TestTokenExtraction: Test token extraction from Claude Code JSON responses.
- TestEndToEndIntegration: Integration tests for full token tracking flow.

Functions:
- temp_work_dir(tmp_path): Create a temporary working directory for tests.
- mock_claude_process(temp_work_dir): Create a ClaudeCodeProcess instance for testing.
- create_mock_json_response(input_tokens=100,
    cache_creation=0,
    cache_read=0,
    output_tokens=50,
    result_text="Task completed successfully",): Helper to create a mock Claude Code JSON response.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
