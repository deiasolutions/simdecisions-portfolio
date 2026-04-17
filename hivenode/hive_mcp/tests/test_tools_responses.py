"""
test_tools_responses
====================

Tests for response submission and task write/archive tools.

Dependencies:
- import pytest
- from hivenode.hive_mcp.tools.responses import (
- from hivenode.hive_mcp.tools.tasks import task_write, task_archive
- from hivenode.hive_mcp.state import StateManager

Functions:
- repo_root(tmp_path): Create temp repo structure.
- state_manager(tmp_path): Create state manager with temp directory.
- test_task_write_creates_file(repo_root, monkeypatch): Test task_write creates file with correct content.
- test_task_write_validates_naming_convention(repo_root, monkeypatch): Test task_write rejects malformed filenames.
- test_task_write_rejects_path_traversal(repo_root, monkeypatch): Test task_write rejects path traversal attempts.
- test_task_archive_requires_response(repo_root, monkeypatch): Test task_archive rejects archival without response file.
- test_task_archive_moves_to_archive(repo_root, monkeypatch): Test task_archive moves task to _archive/ when response exists.
- test_task_archive_rejects_path_traversal(repo_root, monkeypatch): Test task_archive rejects path traversal.
- test_response_submit_creates_file(repo_root, state_manager, monkeypatch): Test response_submit creates file with valid frontmatter.
- test_response_submit_validates_frontmatter(repo_root, state_manager, monkeypatch): Test response_submit rejects missing frontmatter fields.
- test_response_submit_structured_error_format(repo_root, state_manager, monkeypatch): Test response_submit returns structured errors per spec 8.1.
- test_response_submit_retry_tracking(repo_root, state_manager, monkeypatch): Test response_submit tracks retry count and emits TASK_BLOCKED after 3 failures.
- test_response_submit_invalid_yaml(repo_root, state_manager, monkeypatch): Test response_submit handles invalid YAML gracefully.
- test_response_submit_rejects_path_traversal(repo_root, state_manager, monkeypatch): Test response_submit rejects path traversal.
- test_response_submit_naming_convention(repo_root, state_manager, monkeypatch): Test response_submit validates naming convention.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
