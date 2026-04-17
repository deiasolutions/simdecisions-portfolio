"""
test_build_monitor_sse
======================

Tests for SSE stream snapshot and last_heartbeat field inclusion.

Verifies that:
1. SSE snapshot includes last_heartbeat field for all tasks
2. last_heartbeat is the same in REST /status and SSE snapshot
3. Tasks without last_heartbeat (backward compat) are handled gracefully

Dependencies:
- import pytest
- from datetime import datetime
- from fastapi.testclient import TestClient
- from hivenode.routes.build_monitor import (

Classes:
- TestSSESnapshotLastHeartbeat: Tests for SSE snapshot event structure and last_heartbeat field.

Functions:
- reset_state(tmp_path, monkeypatch): Reset singleton state between tests.
- app(): Tests for SSE snapshot event structure and last_heartbeat field.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
