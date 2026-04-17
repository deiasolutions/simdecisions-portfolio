"""
test_tools_tasks
================

Tests for task tools (task_list, task_read).

Dependencies:
- import pytest
- from hivenode.hive_mcp.tools.tasks import task_list, task_read

Functions:
- tasks_dir(tmp_path): Create temp tasks directory structure.
- sample_tasks(tasks_dir): Create sample task files.
- test_task_list_empty_directory(tasks_dir, monkeypatch): Test task_list with empty tasks directory.
- test_task_list_all_tasks(tasks_dir, sample_tasks, monkeypatch): Test task_list returns all tasks (excluding _archive).
- test_task_list_excludes_archive(tasks_dir, sample_tasks, monkeypatch): Test task_list excludes _archive/ subdirectory.
- test_task_list_filter_by_assigned_bee(tasks_dir, sample_tasks, monkeypatch): Test task_list filters by assigned_bee.
- test_task_list_filter_by_wave(tasks_dir, sample_tasks, monkeypatch): Test task_list filters by wave.
- test_task_list_filter_by_status(tasks_dir, sample_tasks, monkeypatch): Test task_list filters by status.
- test_task_list_multiple_filters(tasks_dir, sample_tasks, monkeypatch): Test task_list with multiple filters.
- test_task_read_with_frontmatter(tasks_dir, sample_tasks, monkeypatch): Test task_read parses YAML frontmatter correctly.
- test_task_read_without_frontmatter(tasks_dir, sample_tasks, monkeypatch): Test task_read handles tasks without frontmatter.
- test_task_read_path_traversal_rejected(tasks_dir, monkeypatch): Test task_read rejects path traversal attempts.
- test_task_read_absolute_path_rejected(tasks_dir, monkeypatch): Test task_read rejects absolute paths.
- test_task_read_archive_path_rejected(tasks_dir, sample_tasks, monkeypatch): Test task_read rejects paths from _archive/.
- test_task_read_nonexistent_file(tasks_dir, monkeypatch): Test task_read handles nonexistent file gracefully.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
