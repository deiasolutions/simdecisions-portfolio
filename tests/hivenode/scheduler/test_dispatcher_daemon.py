"""
test_dispatcher_daemon
======================

Tests for dispatcher_daemon.py — TDD approach.

Dependencies:
- import json
- import os
- import shutil
- import tempfile
- import threading
- import time
- from datetime import datetime, UTC
- from pathlib import Path
- import pytest
- import yaml

Functions:
- create_queue_config(config_dir: Path, max_parallel_bees: int = 10): Create queue.yml in config directory.
- temp_dirs(): Create temporary directories for testing with queue.yml config.
- sample_schedule(): Sample schedule.json content.
- test_dispatcher_daemon_init(): Test DispatcherDaemon initialization.
- test_dispatcher_daemon_start_stop(temp_dirs): Test daemon starts and stops cleanly.
- test_dispatcher_dry_run_no_file_moves(temp_dirs, sample_schedule): Test --dry-run flag prevents file moves.
- test_dispatcher_slot_calculation(temp_dirs, sample_schedule): Test slot calculation (active + queued vs max_bees).
- test_dispatcher_moves_spec_files(temp_dirs, sample_schedule): Test dispatcher moves spec files from backlog/ to queue/.
- test_dispatcher_appends_dispatched_jsonl(temp_dirs, sample_schedule): Test dispatcher appends to dispatched.jsonl with correct format.
- test_dispatcher_appends_dispatcher_log_jsonl(temp_dirs, sample_schedule): Test dispatcher appends to dispatcher_log.jsonl with cycle events.
- test_dispatcher_skips_when_spec_not_found(temp_dirs, sample_schedule): Test dispatcher skips tasks when spec file not found in backlog/.
- test_dispatcher_handles_missing_schedule_json(temp_dirs): Test dispatcher handles missing schedule.json gracefully.
- test_dispatcher_respects_max_bees_limit(temp_dirs, sample_schedule): Test dispatcher respects max_bees limit (does not over-dispatch).
- test_dispatcher_sigint_graceful_shutdown(temp_dirs): Test SIGINT triggers graceful shutdown.
- test_dispatcher_case_insensitive_task_id_matching(temp_dirs): Test case-insensitive task_id matching (MW-S01 matches SPEC-mw-s01.md).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
