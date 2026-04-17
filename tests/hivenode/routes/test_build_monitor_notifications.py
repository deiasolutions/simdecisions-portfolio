"""
test_build_monitor_notifications
================================

Tests for build monitor notification system.

Tests:
1. record_notification creates notification with proper fields
2. GET /build/notifications returns notifications in reverse chronological order
3. GET /build/notifications?since=TIMESTAMP filters by timestamp
4. SSE /build/stream broadcasts notification events
5. Notifications persist in monitor-state.json
6. Notifications kept to last 50 entries (pruning test)
7. Queue event watcher triggers notifications on spec_done
8. Queue event watcher triggers notifications on spec_dead with rejection reason

Dependencies:
- import asyncio
- import json
- import tempfile
- from datetime import datetime, timedelta
- from pathlib import Path
- from typing import AsyncGenerator
- import pytest
- from fastapi import FastAPI
- from fastapi.testclient import TestClient
- from hivenode.routes.build_monitor import (

Functions:
- temp_state_file(): Create temporary state file for isolated testing.
- build_state(temp_state_file: Path): Create BuildState instance with temp file.
- app(): Create test FastAPI app with build monitor routes.
- client(app: FastAPI): Create test client.
- test_record_notification_creates_proper_structure(build_state: BuildState): Test that record_notification creates notification with all required fields.
- test_record_notification_with_message(build_state: BuildState): Test record_notification with failure message.
- test_notifications_appended_to_list(build_state: BuildState): Test that notifications are appended in chronological order.
- test_notifications_pruned_to_50(build_state: BuildState): Test that notifications list is pruned to last 50 entries.
- test_notifications_persist_to_disk(temp_state_file: Path): Test that notifications persist to monitor-state.json.
- test_get_notifications_endpoint_returns_reverse_chronological(client: TestClient, build_state: BuildState, monkeypatch,): Test GET /build/notifications returns notifications newest-first.
- test_get_notifications_with_since_filter(client: TestClient, build_state: BuildState, monkeypatch,): Test GET /build/notifications?since=TIMESTAMP filters properly.
- test_sse_stream_broadcasts_notification_events(build_state: BuildState, monkeypatch,): Test that SSE subscribers receive notification events.
- test_queue_event_done_triggers_notification(temp_state_file: Path): Test that queue.spec_done event triggers notification.
- test_queue_event_dead_triggers_notification_with_rejection(temp_state_file: Path, tmp_path: Path,): Test that queue.spec_dead event triggers notification with rejection reason.
- test_notifications_survive_restart(temp_state_file: Path): Test that notifications persist across BuildState restarts.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
