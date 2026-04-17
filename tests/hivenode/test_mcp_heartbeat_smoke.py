"""
test_mcp_heartbeat_smoke
========================

Smoke test for MCP heartbeat forwarding.

This test verifies that MCP heartbeats are forwarded to hivenode's
BuildState and appear in /build/status responses.

Run this test with a live hivenode instance:
    python -m pytest tests/hivenode/test_mcp_heartbeat_smoke.py -v

Dependencies:
- import json
- import time
- import pytest
- import httpx
- from hivenode.hive_mcp.tools.telemetry import heartbeat
- from hivenode.hive_mcp.state import StateManager

Functions:
- test_smoke_mcp_heartbeat_to_build_status(): Smoke test: Send MCP heartbeat and verify it appears in /build/status.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
