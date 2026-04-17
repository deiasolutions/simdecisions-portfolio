"""
test_tools_queue
================

Tests for queue tools (queue_list, queue_peek, queue_state).

Dependencies:
- import pytest
- from hivenode.hive_mcp.tools.queue import queue_list, queue_peek, queue_state

Functions:
- queue_dir(tmp_path): Create temp queue directory structure.
- sample_specs(queue_dir): Create sample spec files.
- test_queue_list_empty_directory(queue_dir, monkeypatch): Test queue_list with empty queue directory.
- test_queue_list_all_specs(queue_dir, sample_specs, monkeypatch): Test queue_list returns all specs with correct metadata.
- test_queue_list_filter_by_status(queue_dir, sample_specs, monkeypatch): Test queue_list filters by status.
- test_queue_list_filter_by_area_code(queue_dir, sample_specs, monkeypatch): Test queue_list filters by area_code.
- test_queue_list_filter_by_priority(queue_dir, sample_specs, monkeypatch): Test queue_list filters by priority.
- test_queue_list_multiple_filters(queue_dir, sample_specs, monkeypatch): Test queue_list with multiple filters.
- test_queue_peek_success(queue_dir, sample_specs, monkeypatch): Test queue_peek reads spec content correctly.
- test_queue_peek_dead_spec(queue_dir, sample_specs, monkeypatch): Test queue_peek reads spec from _needs_review.
- test_queue_peek_path_traversal_rejected(queue_dir, monkeypatch): Test queue_peek rejects path traversal attempts.
- test_queue_peek_absolute_path_rejected(queue_dir, monkeypatch): Test queue_peek rejects absolute paths.
- test_queue_peek_nonexistent_file(queue_dir, monkeypatch): Test queue_peek handles nonexistent file gracefully.
- test_queue_list_ignores_non_md_files(queue_dir, monkeypatch): Test queue_list ignores non-markdown files.
- queue_dir_with_states(tmp_path): Create queue directory with active, pending, and done specs.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
