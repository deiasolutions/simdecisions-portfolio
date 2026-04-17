"""
test_build_monitor
==================

Tests for build monitor routes.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.routes.build_monitor import (

Classes:
- TestHeartbeatPost: Test HeartbeatPayload accepts input_tokens and output_tokens.
- TestTokenCost: Tests for token-based cost calculation.
- TestRoleField: Tests for role field in heartbeats.
- TestSSEIntegration: Integration tests for SSE stream with token tracking.
- TestQueueScanning: Tests for runner_queue and feeder_queue directory scanning.
- TestQueueWakeEndpoint: Tests for POST /build/queue-wake and GET /build/queue-runner-status.

Functions:
- reset_state(tmp_path, monkeypatch): Reset singleton state between tests.
- app(): Test HeartbeatPayload accepts input_tokens and output_tokens.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
