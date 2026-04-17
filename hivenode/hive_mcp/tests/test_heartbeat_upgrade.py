"""
test_heartbeat_upgrade
======================

Tests for heartbeat tool progress and spec_id upgrade (MCP-002).

Dependencies:
- import pytest
- import tempfile
- from pathlib import Path
- from hivenode.hive_mcp.tools.telemetry import heartbeat
- from hivenode.hive_mcp.state import StateManager

Functions:
- state_manager(): Create a temporary state manager for testing.
- test_heartbeat_with_progress(state_manager): Heartbeat accepts optional progress parameter (0.0-1.0).
- test_heartbeat_with_spec_id_alias(state_manager): Heartbeat accepts spec_id as alias for task_id.
- test_heartbeat_backward_compatibility(state_manager): Heartbeat works with old parameters only (no progress, no spec_id).
- test_heartbeat_both_task_id_and_spec_id(state_manager): When both task_id and spec_id provided, spec_id takes precedence.
- test_heartbeat_progress_validation(): Heartbeat validates progress is between 0.0 and 1.0.
- test_heartbeat_progress_boundary_values(state_manager): Heartbeat accepts boundary values 0.0 and 1.0.
- test_heartbeat_writes_to_event_ledger(state_manager, tmp_path): Heartbeat writes to Event Ledger via telemetry_logger.log_build_attempt.
- test_heartbeat_returns_ack_format(state_manager): Heartbeat returns {'ack': True, 'timestamp': '...'} format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
