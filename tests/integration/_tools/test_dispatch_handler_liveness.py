"""
test_dispatch_handler_liveness
==============================

Tests for dispatch_handler liveness detection using last_heartbeat.

After TASK-216, last_seen only updates on state transitions, while
last_heartbeat updates on EVERY heartbeat (silent pings included).

The watchdog needs last_heartbeat to detect dead bees accurately.

Dependencies:
- import json
- import pytest
- from datetime import datetime, timedelta
- from pathlib import Path
- from unittest.mock import patch, Mock
- import sys
- from dispatch_handler import DispatchHandler

Functions:
- handler(tmp_path): Create DispatchHandler with temporary paths.
- mock_build_status(tasks): Create mock build monitor status response.
- test_fresh_heartbeat_within_8min_is_alive(handler): Fresh heartbeat (within 8 min) → bee is alive (not stale).
- test_stale_heartbeat_over_8min_is_dead(handler): Stale heartbeat (> 8 min) → bee is dead (stale).
- test_old_monitor_state_missing_last_heartbeat_falls_back_to_last_seen(handler): Task with no last_heartbeat field (old monitor state) → fall back to last_seen.
- test_task_not_found_in_monitor_is_not_stale(handler): Task not found in monitor → not stale (hasn't started yet).
- test_monitor_unreachable_does_not_kill_bee(handler): Monitor API unreachable → not stale (don't kill on monitor failure).
- test_stale_last_seen_but_fresh_last_heartbeat_is_alive(handler): last_seen is stale (10 min ago) but last_heartbeat is fresh (5 min ago) → alive.
- test_exactly_8min_boundary_is_not_stale(handler): Heartbeat exactly at 480s (8 min) boundary → NOT stale (must be > 480s).
- test_one_second_over_8min_is_stale(handler): Heartbeat at 481s (just over 8 min) → stale.
- test_watchdog_timeout_with_missing_temp_file_returns_timeout(handler): Watchdog kills process, tries to restart, but temp file is missing → TIMEOUT (no crash).
- test_watchdog_restart_with_cached_content_succeeds(handler): Watchdog kills process, restarts with cached content → success on retry.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
