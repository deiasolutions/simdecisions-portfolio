"""
test_mcp_telemetry
==================

Tests for MCP telemetry dual-loop (SPEC-MCP-WAVE-5-TELEMETRY-LOOP).

This test file verifies the telemetry dual-loop architecture:
- Observer loop: heartbeats → Event Ledger
- Advisor loop: pattern detection → advisory responses

Acceptance Criteria from spec:
- AC-06: heartbeat updates monitor state
- AC-20: heartbeat logs to Event Ledger
- AC-21: Budget warning advisory when session cost >80%
- AC-22: Stall warning advisory when >15 min since last heartbeat
- AC-23: Advisories are non-blocking

Dependencies:
- import pytest
- import tempfile
- import time
- from pathlib import Path
- from unittest.mock import MagicMock, patch
- from hivenode.hive_mcp.tools import telemetry
- from hivenode.hive_mcp.state import StateManager

Functions:
- temp_state_dir(): Create a temporary directory for state files.
- state_manager(temp_state_dir): Create a StateManager instance for testing.
- temp_db(): Create a temporary Event Ledger database.
- test_ac06_heartbeat_updates_monitor_state(state_manager): AC-06: heartbeat updates monitor state.
- test_ac20_heartbeat_logs_to_event_ledger(state_manager, temp_db): AC-20: heartbeat logs to Event Ledger.
- test_ac21_budget_warning_advisory_at_80_percent(state_manager): AC-21: Budget warning advisory when session cost >80%.
- test_ac22_stall_warning_advisory_after_15_minutes(state_manager): AC-22: Stall warning advisory when >15 min since last heartbeat.
- test_ac23_advisories_are_non_blocking(state_manager): AC-23: Advisories are non-blocking.
- test_observer_loop_integration(state_manager): Integration test for observer loop: heartbeat → state + ledger.
- test_advisor_loop_integration(state_manager): Integration test for advisor loop: pattern detection → advisory.
- test_heartbeat_with_spec_id_alias(state_manager): Test heartbeat accepts spec_id as alias for task_id.
- test_heartbeat_progress_parameter(state_manager): Test heartbeat accepts and validates progress parameter.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
