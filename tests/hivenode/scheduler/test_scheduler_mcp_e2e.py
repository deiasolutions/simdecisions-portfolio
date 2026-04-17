"""
test_scheduler_mcp_e2e
======================

E2E tests for scheduler MCP event-driven operation.

Tests cover:
- Start scheduler daemon with MCP enabled
- Move spec to _done/
- Send MCP event via POST
- Verify schedule recalculated within 2s
- Verify fallback polling works if no events (60s timeout)
- Edge cases: MCP server down on startup, malformed events, daemon stopped while waiting

Dependencies:
- import socket
- import tempfile
- import time
- from pathlib import Path
- import httpx
- import pytest

Classes:
- TestMCPServerIntegration: Test MCP server integration.
- TestEventDrivenScheduleRecalculation: Test that schedule is recalculated on MCP events.
- TestEdgeCases: Test edge cases.

Functions:
- get_free_port(): Get a free port for testing.
- temp_dirs(): Create temporary directories for testing.
- sample_tasks(): Sample tasks for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
