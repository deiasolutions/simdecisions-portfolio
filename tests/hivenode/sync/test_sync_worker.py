"""
test_sync_worker
================

Tests for sync worker and file watcher.

Tests:
1. CLI `8os sync` command — success
2. CLI `8os sync` command — hivenode not running
3. CLI `8os sync --status` command
4. PeriodicSyncWorker scheduling (runs on interval)
5. PeriodicSyncWorker flush (flushes SyncQueue on each cycle)
6. PeriodicSyncWorker error handling (logs errors, doesn't crash)
7. FileWatcher detects file writes
8. FileWatcher respects sync_ignore patterns
9. FileWatcher debouncing (multiple writes = single queue entry)
10. Startup sync (pulls from cloud on startup)

Dependencies:
- import asyncio
- import tempfile
- import time
- from pathlib import Path
- from unittest.mock import Mock, AsyncMock, patch
- import pytest
- from hivenode.sync.worker import PeriodicSyncWorker
- from hivenode.sync.watcher import FileWatcher
- from hivenode.sync.sync_log import SyncLog

Functions:
- test_file_watcher_detects_writes(): Test that FileWatcher detects file writes.
- test_file_watcher_respects_ignore_patterns(): Test that FileWatcher respects sync_ignore patterns.
- test_file_watcher_debouncing(): Test that FileWatcher debounces multiple writes to same file.
- test_cli_sync_success(mock_post): Test `8os sync` command — success.
- test_cli_sync_hivenode_not_running(mock_post): Test `8os sync` command — hivenode not running.
- test_cli_sync_status(mock_get): Test `8os sync --status` command.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
