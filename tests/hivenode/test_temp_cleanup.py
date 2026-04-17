"""
test_temp_cleanup
=================

tests/hivenode/test_temp_cleanup.py
Tests for temp file cleanup job: boot, 24-hour schedule, TTL expiration

Dependencies:
- import asyncio
- import pytest
- from datetime import datetime, timedelta
- from hivenode.temp_cleanup import cleanup_expired_temp_files, schedule_cleanup_task

Functions:
- temp_storage(tmp_path): Create a temporary storage directory with test files.
- test_cleanup_deletes_expired_files(temp_storage): Test that cleanup job deletes files with expired TTL.
- test_cleanup_skips_files_without_ttl(temp_storage): Test that cleanup skips files without TTL field.
- test_cleanup_handles_corrupt_json(temp_storage): Test that cleanup handles corrupt JSON gracefully.
- test_cleanup_deletes_content_files(temp_storage): Test that cleanup deletes expired per-pane content files.
- test_cleanup_empty_directory(temp_storage): Test cleanup on empty directory.
- test_cleanup_removes_empty_parent_dirs(temp_storage): Test that cleanup removes empty parent directories after deletion.
- test_cleanup_handles_permission_errors(temp_storage): Test that cleanup handles permission errors gracefully.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
