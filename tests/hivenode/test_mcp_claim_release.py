"""
test_mcp_claim_release
======================

Tests for MCP claim/release tools (Phase 1 write tools).

Dependencies:
- import pytest
- from hivenode.hive_mcp.tools.claim import mcp_claim_task, mcp_release_task
- from hivenode.hive_mcp.state import StateManager

Functions:
- temp_repo(tmp_path): Create temporary repo structure.
- state_manager(tmp_path): Create test state manager.
- test_claim_task_success(temp_repo, state_manager, monkeypatch): Test successful task claim moves file to _active.
- test_claim_task_already_claimed(temp_repo, state_manager, monkeypatch): Test claiming already-claimed task returns existing owner.
- test_release_task_done(temp_repo, state_manager, monkeypatch): Test releasing task with reason='done' moves to _done.
- test_release_task_failed(temp_repo, state_manager, monkeypatch): Test releasing task with reason='failed' moves back to backlog.
- test_release_task_timeout(temp_repo, state_manager, monkeypatch): Test releasing task with reason='timeout' moves to _dead.
- test_claim_survives_restart(temp_repo, state_manager, monkeypatch): Test that claims persist across StateManager restart.
- test_claim_from_main_queue(temp_repo, state_manager, monkeypatch): Test claiming spec from main queue directory.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
