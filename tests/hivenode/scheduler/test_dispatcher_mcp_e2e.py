"""
test_dispatcher_mcp_e2e
=======================

E2E tests for dispatcher MCP event-driven flow — TDD.

Dependencies:
- import json
- import shutil
- import tempfile
- import time
- from datetime import datetime, UTC
- from pathlib import Path
- import pytest
- from hivenode.scheduler.dispatcher_daemon import DispatcherDaemon

Functions:
- temp_dirs(): Create temporary directories for testing.
- sample_schedule(): Sample schedule.json with 3 ready tasks.
- test_e2e_mcp_event_wakes_dispatcher_and_dispatches(temp_dirs, sample_schedule): Test E2E: Send queue.spec_done event → dispatcher wakes → dispatches from backlog within 2s.
- test_e2e_fallback_polling_works_when_no_events(temp_dirs, sample_schedule): Test E2E: Fallback polling works (60s timeout) when no MCP events sent.
- test_e2e_counter_accuracy_after_multiple_events(temp_dirs, sample_schedule): Test E2E: Counters stay accurate after multiple rapid events.
- test_e2e_mcp_disabled_falls_back_to_polling(temp_dirs, sample_schedule): Test E2E: MCP disabled mode falls back to polling (10s interval).
- test_e2e_daemon_stopped_while_waiting(temp_dirs, sample_schedule): Test E2E: Daemon stops cleanly while waiting on wake_event.
- test_e2e_multiple_events_within_1s(temp_dirs, sample_schedule): Test E2E: Multiple events within 1s are handled correctly (no counter drift).
- test_e2e_refresh_counts_syncs_after_missed_event(temp_dirs): Test E2E: Fallback refresh detects counter drift and re-syncs.
- test_e2e_dispatched_jsonl_records_dispatches(temp_dirs, sample_schedule): Test E2E: Dispatches are recorded in dispatched.jsonl (event-driven mode).
- test_e2e_dispatcher_log_includes_event_source(temp_dirs, sample_schedule): Test E2E: dispatcher_log.jsonl includes source field (mcp_event vs fallback_poll).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
