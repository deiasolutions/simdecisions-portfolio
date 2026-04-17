"""
test_mcp_lifecycle
==================

Tests for MCP server lifecycle and health endpoints.

Covers:
- MCP server starts with hivenode
- /mcp/health endpoint returns tool list + uptime
- /health endpoint returns bare liveness
- Graceful handling of port conflicts

Dependencies:
- import pytest
- import httpx
- from pathlib import Path

Functions:
- test_queue_yml_mcp_required_false(): AC-04: queue.yml contains mcp_required: false.
- test_mcp_startup_logging_code_review(): AC-05: Hivenode startup logs show MCP status.
- test_mcp_port_conflict_handling_code_review(): AC-06: If port 8421 is occupied, hivenode logs warning and continues.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
