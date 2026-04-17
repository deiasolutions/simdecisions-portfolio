"""
test_mcp_tools
==============

Integration tests for Hive MCP Phase 0 tools.

Tests verify tool interfaces match documented specs and return correct data structures.

Dependencies:
- import pytest
- from hivenode.hive_mcp.tools import queue, coordination, responses, telemetry
- from hivenode.hive_mcp.state import StateManager

Classes:
- TestHeartbeat: Test heartbeat tool interface.
- TestQueueList: Test queue_list tool interface.
- TestMcpQueueState: Test mcp_queue_state (queue_state) tool interface.
- TestBriefingRead: Test briefing_read tool interface.
- TestResponseSubmit: Test response_submit tool interface.
- TestToolInterfaceCompliance: Verify all Phase 0 tools match documented interfaces.

Functions:
- temp_repo_root(tmp_path): Create temporary repo structure for testing.
- patch_repo_root(temp_repo_root, monkeypatch): Patch _find_repo_root to use temp directory.
- state_manager(): Create in-memory state manager for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
