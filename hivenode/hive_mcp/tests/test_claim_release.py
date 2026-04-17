"""
test_claim_release
==================

Tests for claim_task and release_task tools.

Dependencies:
- import pytest
- import tempfile
- import shutil
- from pathlib import Path
- from hivenode.hive_mcp.tools.tasks import claim_task, release_task
- from hivenode.hive_mcp.state import StateManager

Functions:
- temp_queue(): Create a temporary queue directory structure.
- temp_state(): Create a temporary state manager.
- test_claim_unclaimed_task(temp_queue, temp_state, monkeypatch): Test claiming an unclaimed task successfully.
- test_claim_already_claimed_task(temp_queue, temp_state, monkeypatch): Test attempting to claim an already-claimed task.
- test_claim_nonexistent_spec(temp_queue, temp_state, monkeypatch): Test claiming a spec that doesn't exist.
- test_release_task_done(temp_queue, temp_state, monkeypatch): Test releasing a task with 'done' status.
- test_release_task_failed(temp_queue, temp_state, monkeypatch): Test releasing a task with 'failed' status.
- test_release_task_timeout(temp_queue, temp_state, monkeypatch): Test releasing a task with 'timeout' status.
- test_release_unclaimed_task(temp_queue, temp_state, monkeypatch): Test releasing a task that was never claimed.
- test_state_manager_recovery(temp_queue, monkeypatch): Test that StateManager recovers claims from _active directory on startup.
- test_claim_release_integration(temp_queue, temp_state, monkeypatch): Integration test: claim → work → release cycle.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
