"""
test_factory_routes
===================

Tests for factory routes (SPEC-FACTORY-006).

Tests MCP-with-fallback pattern for all factory endpoints:
- GET /factory/health
- GET /factory/responses
- GET /factory/responses/{id}/content
- POST /factory/archive
- POST /factory/spec-submit
- GET /factory/git-summary

Dependencies:
- from unittest.mock import AsyncMock, MagicMock, patch
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- temp_factory_dirs(tmp_path): Create temporary factory directories for testing.
- mock_mcp_client(): Mock MCP client for testing.
- test_health_check_healthy(mock_mcp_client): Test /factory/health when MCP is up and filesystem is OK.
- test_health_check_mcp_down(mock_mcp_client): Test /factory/health when MCP is down.
- test_list_responses_file_fallback(temp_factory_dirs, mock_mcp_client): Test /factory/responses with file fallback when MCP is down.
- test_list_responses_filter_by_status(temp_factory_dirs, mock_mcp_client): Test /factory/responses with status filter.
- test_list_responses_pagination(temp_factory_dirs, mock_mcp_client): Test /factory/responses pagination.
- test_list_responses_mcp_success(mock_mcp_client): Test /factory/responses when MCP is available.
- test_get_response_content_file_fallback(temp_factory_dirs, mock_mcp_client): Test /factory/responses/{id}/content with file fallback.
- test_get_response_content_not_found(temp_factory_dirs, mock_mcp_client): Test /factory/responses/{id}/content when response doesn't exist.
- test_get_response_content_mcp_success(mock_mcp_client): Test /factory/responses/{id}/content when MCP is available.
- test_archive_task_file_fallback(temp_factory_dirs, mock_mcp_client): Test /factory/archive with file fallback.
- test_archive_task_response_not_found(temp_factory_dirs, mock_mcp_client): Test /factory/archive when response doesn't exist.
- test_archive_task_mcp_success(mock_mcp_client): Test /factory/archive when MCP is available.
- test_spec_submit_creates_file(temp_factory_dirs, mock_mcp_client): Test /factory/spec-submit creates spec file.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
