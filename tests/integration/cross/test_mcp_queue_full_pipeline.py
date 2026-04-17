"""
test_mcp_queue_full_pipeline
============================

Full pipeline integration tests for MCP queue notification system.

Tests the complete flow: spec moves through directories → watcher emits event →
MCP endpoint broadcasts → scheduler/dispatcher react.

These tests verify end-to-end behavior with real file operations, threading, and
HTTP communication.

Dependencies:
- import json
- import shutil
- import socket
- import tempfile
- import time
- from datetime import datetime, timezone, timedelta
- from pathlib import Path
- import pytest

Functions:
- get_free_port(): Get a free port for testing.
- temp_dirs(): Create temporary directory structure for testing.
- sample_tasks(): Sample tasks for scheduler testing.
- test_full_pipeline_spec_queued_to_done_scheduler_recalc(temp_dirs, sample_tasks): Test: spec queued → active → done → scheduler recalculates within 2s.
- test_full_pipeline_spec_done_dispatcher_frees_slot(temp_dirs, sample_tasks): Test: spec done → dispatcher frees slot → backlog dispatch within 2s.
- test_parallel_completions_all_handled(temp_dirs, sample_tasks): Test: 5 specs complete within 1s → all events handled correctly.
- test_rapid_moves_debouncing_works(temp_dirs, sample_tasks): Test: spec moves queue → active → done within 500ms → events deduplicated.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
