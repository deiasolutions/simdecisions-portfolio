"""
test_dispatcher_mcp_unit
========================

Unit tests for dispatcher MCP event-driven features — TDD.

Dependencies:
- import json
- import shutil
- import tempfile
- import threading
- from datetime import datetime, UTC
- from pathlib import Path
- import pytest
- from hivenode.scheduler.dispatcher_daemon import DispatcherDaemon

Functions:
- temp_dirs(): Create temporary directories for testing.
- test_mcp_event_spec_active_increments_counter(temp_dirs): Test on_mcp_event() increments active_count on queue.spec_active event.
- test_mcp_event_spec_done_decrements_counter(temp_dirs): Test on_mcp_event() decrements active_count on queue.spec_done event.
- test_mcp_event_spec_done_sets_wake_event(temp_dirs): Test on_mcp_event() sets wake_event on queue.spec_done (to trigger dispatch).
- test_mcp_event_spec_queued_increments_counter(temp_dirs): Test on_mcp_event() increments queued_count on queue.spec_queued event.
- test_mcp_event_counter_underflow_protection(temp_dirs): Test on_mcp_event() prevents counter underflow (never goes below 0).
- test_mcp_event_thread_safety_concurrent_events(temp_dirs): Test on_mcp_event() is thread-safe (handles concurrent events correctly).
- test_refresh_counts_syncs_from_disk(temp_dirs): Test _refresh_counts() re-counts specs from disk (fallback sync).
- test_refresh_counts_updates_mismatched_counters(temp_dirs): Test _refresh_counts() detects and corrects counter drift.
- test_mcp_disabled_mode_uses_polling_only(temp_dirs): Test MCP disabled mode (mcp_enabled=False) falls back to polling.
- test_mcp_enabled_by_default(temp_dirs): Test MCP is enabled by default (backward compatible).
- test_on_mcp_event_ignores_unknown_events(temp_dirs): Test on_mcp_event() ignores unknown event types (no crash).
- test_dispatch_cycle_uses_in_memory_counters(temp_dirs): Test _dispatch_cycle() uses in-memory counters (not direct file counting).
- test_dispatch_cycle_logs_source_field(temp_dirs): Test _dispatch_cycle() logs source field (mcp_counters vs disk_scan).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
