"""
test_build_monitor_state_transition
===================================

Tests for build monitor state transition detection logic.

Tests the heartbeat handling logic that distinguishes silent pings (timestamp-only
updates) from logged state transitions (changes that warrant log appends).

Also tests status enum alignment and validation.

Dependencies:
- import pytest
- from datetime import datetime
- from hivenode.routes.build_monitor import (

Classes:
- TestStateTransitionDetection: Test the _is_state_transition helper method.
- TestHeartbeatLastHeartbeatField: Test that last_heartbeat field is always updated.
- TestHeartbeatLastLoggedMessageField: Test that last_logged_message field tracks the last appended message.
- TestLogAppendBehavior: Test that log array grows only on state transitions.
- TestPersistenceAndBackwardCompatibility: Test that new fields are persisted and old state is compatible.
- TestStatusEnumAlignment: Test that BuildStatus enum values align with expected statuses.
- TestHeartbeatStatusValidation: Test that HeartbeatPayload validates status values.
- TestStatusTransitionBehavior: Test status-based behavior (auto-release, active/completed grouping).

Functions:
- fresh_build_state(tmp_path): Create a fresh BuildState with temp state file (no disk pollution).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
