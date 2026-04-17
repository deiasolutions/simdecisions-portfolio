"""
test_scheduler_backlog_scanning
===============================

Tests for backlog scanning feature (TDD - written before implementation).

Tests cover:
- scan_backlog() parsing SPEC-*.md files from backlog/
- extract_task_id() handling all filename formats
- Merging backlog tasks with workdesk tasks
- Priority ordering (backlog specs use their own P0-P3)
- Dependency resolution from ## Depends On sections
- Duration estimation from model assignment
- Graceful error handling for malformed specs
- Performance (< 100ms for 100 specs)

Dependencies:
- import tempfile
- from pathlib import Path
- import pytest
- from hivenode.scheduler.scheduler_daemon import SchedulerDaemon
- from hivenode.scheduler.scheduler_mobile_workdesk import Task

Classes:
- TestExtractTaskId: Test task ID extraction from spec filenames.
- TestEstimateDuration: Test duration estimation from model assignment.
- TestScanBacklog: Test backlog directory scanning.
- TestBacklogMerging: Test merging backlog tasks with workdesk tasks.
- TestBacklogRescan: Test that daemon rescans backlog on each cycle.
- TestPerformance: Test backlog scanning performance.

Functions:
- temp_dirs(): Create temporary directories for testing.
- sample_workdesk_tasks(): Sample workdesk tasks.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
