"""
test_routes_weighted
====================

Tests for context-weighted suggestion endpoint.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from unittest.mock import patch
- from hivenode.terminal.routes import router

Functions:
- client(): Create test client.
- mock_auth(): Mock authentication dependency.
- test_suggest_weighted_empty_suggestions(client, mock_auth): Test weighted suggestions with empty input.
- test_suggest_weighted_no_context_boost(client, mock_auth): Test weighted suggestions when no context rules apply.
- test_suggest_weighted_file_command_boost(client, mock_auth): Test file command boost in text-pane.
- test_suggest_weighted_git_command_boost(client, mock_auth): Test git command boost in git repository.
- test_suggest_weighted_recent_command_boost(client, mock_auth): Test recent command boost.
- test_suggest_weighted_combined_boosts(client, mock_auth): Test multiple boosts applied cumulatively.
- test_suggest_weighted_reranking(client, mock_auth): Test that suggestions are re-ranked by weighted score.
- test_suggest_weighted_edge_cases(client, mock_auth): Test edge cases with zero scores and empty context.
- test_suggest_weighted_validation_error(client, mock_auth): Test validation error for invalid request.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
