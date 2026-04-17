"""
test_build_monitor_integration
==============================

Integration tests for heartbeat split behavior.

Verifies the complete heartbeat system:
- Silent pings update timestamp but don't grow log
- State transitions append to log
- Liveness detection works correctly
- Frontend receives correct data

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from pathlib import Path
- import tempfile
- import shutil
- from datetime import datetime
- from hivenode.main import app
- from hivenode.routes.build_monitor import BuildState

Classes:
- TestHeartbeatSplitIntegration: E2E integration test for heartbeat split behavior.
- TestLivenessPingEndpoint: E2E tests for POST /build/ping lightweight liveness endpoint.

Functions:
- temp_state_file(): Create a temporary state file for testing.
- test_state(temp_state_file): Create a fresh BuildState instance for testing.
- client_with_state(test_state): Create a TestClient with a fresh BuildState instance.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
