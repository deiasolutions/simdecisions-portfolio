"""
test_mcp_dispatch
=================

Tests for MCP dispatch integration (SPEC-MCP-WAVE-2-DISPATCH-INTEGRATION).

Tests that dispatch.py creates temp directories, writes .mcp.json config,
and includes MCP telemetry instructions in bee prompts.

Dependencies:
- import json
- from unittest import mock
- import pytest

Functions:
- repo_root(tmp_path): Create a temporary repo structure.
- test_temp_directory_created_per_dispatch(repo_root): Test AC-13: Temp directory is isolated per bee.
- test_mcp_config_structure(tmp_path): Test AC-14: .mcp.json points to correct endpoint.
- test_mcp_prompt_injection_contains_tools(tmp_path): Test AC-05: Bee prompt includes MCP notice.
- test_mcp_health_check_returns_bool(): Test AC-08: Queue runner logs MCP status (non-blocking).
- test_dispatch_proceeds_when_mcp_down(repo_root): Test AC-09: Dispatch proceeds if MCP down.
- test_temp_dir_cleanup_on_completion(tmp_path): Verify temp directory is cleaned up after dispatch (success case).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
