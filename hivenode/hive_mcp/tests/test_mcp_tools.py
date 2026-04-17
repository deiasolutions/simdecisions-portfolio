"""
test_mcp_tools
==============

Tests for MCP telemetry tools with advisory support — SPEC-MCP-008.

Dependencies:
- import pytest
- import tempfile
- from pathlib import Path
- from unittest.mock import patch
- from hivenode.hive_mcp.tools import telemetry
- from hivenode.hive_mcp.state import StateManager

Functions:
- temp_state_dir(): Create a temporary directory for state files.
- state_manager(temp_state_dir): Create a StateManager instance for testing.
- test_heartbeat_no_advisory_by_default(state_manager): Test heartbeat returns no advisory when no warnings exist.
- test_heartbeat_with_budget_warning_advisory(state_manager): Test heartbeat includes advisory when budget warning detected.
- test_heartbeat_with_stall_detected_advisory(state_manager): Test heartbeat includes advisory when stall pattern detected.
- test_heartbeat_with_yield_suggested_advisory(state_manager): Test heartbeat includes advisory when yield is suggested.
- test_heartbeat_advisory_non_blocking(state_manager): Test advisory does not block heartbeat on error.
- test_heartbeat_advisory_performance(state_manager): Test advisory check completes within 50ms performance constraint.
- test_heartbeat_advisory_only_when_exists(state_manager): Test advisory field only included when recommendation exists.
- test_heartbeat_advisory_types_valid(state_manager): Test all valid advisory types are supported.
- test_heartbeat_advisory_with_all_params(state_manager): Test heartbeat with advisory and all optional params.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
