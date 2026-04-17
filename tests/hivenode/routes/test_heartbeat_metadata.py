"""
test_heartbeat_metadata
=======================

Tests for heartbeat metadata verification and build monitor cost tracking.

Tests:
1. test_heartbeat_includes_tokens — HeartbeatPayload includes model, input_tokens, output_tokens, cost_usd
2. test_build_monitor_accumulates_cost — Multiple heartbeats accumulate total_cost
3. test_heartbeat_zero_tokens_handled — Zero tokens don't crash, cost remains 0
4. test_build_monitor_status_response — /status endpoint returns non-zero totals after heartbeats

Dependencies:
- import pytest
- from pathlib import Path
- from tempfile import NamedTemporaryFile
- from hivenode.routes.build_monitor import HeartbeatPayload, BuildState

Classes:
- TestHeartbeatMetadata: Test heartbeat payload structure and data integrity.
- TestBuildMonitorCostAccumulation: Test BuildState accumulates cost and tokens from heartbeats.

Functions:
- temp_state_file(): Create a temporary state file for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
