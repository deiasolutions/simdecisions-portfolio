"""
test_integration
================

Integration tests for Hive MCP Streamable HTTP transport.

Dependencies:
- import pytest
- import json
- from starlette.testclient import TestClient

Functions:
- test_repo_dir(tmp_path): Create temporary repository structure for testing.
- mcp_client(test_repo_dir, monkeypatch): Create TestClient for MCP server.
- test_health_check_responds(mcp_client): Test health check endpoint is reachable.
- test_mcp_endpoint_exists(mcp_client): Test /mcp endpoint exists (MCP endpoint for Streamable HTTP).
- test_mcp_tool_listing(mcp_client): Test MCP server has correct tools registered.
- test_call_task_list_via_mcp(mcp_client): Test calling task_list tool via MCP handler.
- test_call_queue_list_via_mcp(mcp_client): Test calling queue_list tool via MCP handler.
- test_multiple_concurrent_clients(mcp_client): Test multiple tool calls can execute (simulating concurrent clients).
- test_invalid_tool_call_returns_error(mcp_client): Test calling nonexistent tool returns error.
- test_server_startup_and_shutdown(mcp_client): Test MCP server app is properly initialized.
- test_task_read_with_frontmatter(mcp_client): Test task_read returns parsed frontmatter via MCP handler.
- test_queue_peek_returns_content(mcp_client): Test queue_peek returns full spec content via MCP handler.
- test_streamable_http_post_initialize(mcp_client): Test Streamable HTTP transport is configured.
- test_streamable_http_notification_returns_202(mcp_client): Test Streamable HTTP transport configuration.
- test_streamable_http_graceful_shutdown(mcp_client): Test server handles graceful shutdown.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
