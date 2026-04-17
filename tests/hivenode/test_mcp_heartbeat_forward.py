"""
test_mcp_heartbeat_forward
==========================

Tests for MCP heartbeat forwarding to hivenode BuildState.

Tests verify that MCP heartbeats are dual-written:
1. To MCP StateManager (existing behavior)
2. To hivenode BuildState via HTTP /build/heartbeat (new forwarding)

Dependencies:
- import json
- import pytest
- from unittest.mock import patch, MagicMock
- from hivenode.hive_mcp.tools.telemetry import heartbeat
- from hivenode.hive_mcp.state import StateManager

Functions:
- test_heartbeat_forwards_to_hivenode_success(): Test that heartbeat successfully forwards to hivenode /build/heartbeat.
- test_heartbeat_forwards_with_connection_failure(): Test that heartbeat continues when hivenode is unavailable.
- test_heartbeat_forwards_with_timeout(): Test that heartbeat continues when hivenode times out.
- test_heartbeat_payload_mapping(): Test that MCP heartbeat payload correctly maps to BuildState schema.
- test_heartbeat_dual_write_state_manager(): Test that heartbeat writes to both StateManager and hivenode.
- test_mcp_heartbeat_appears_in_build_status(): Integration test: verify MCP heartbeat appears in /build/status response.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
