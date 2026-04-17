"""
test_sync_engine
================

Tests for Volume Sync Engine

Coverage:
1. Sync log CRUD operations
2. SyncEngine push (local → remote)
3. SyncEngine pull (remote → local)
4. SyncEngine conflict detection + last-write-wins
5. SyncEngine skip (hashes match)
6. Conflict file naming
7. Sync ignore patterns
8-11. HTTP routes (trigger, status, conflicts, resolve)
12. Ledger event logging
13. Sync with empty volumes
14. Sync with SyncQueue flush
15. Idempotency

Dependencies:
- import os
- import tempfile
- import time
- from pathlib import Path
- import pytest
- from fastapi import FastAPI
- from httpx import ASGITransport, AsyncClient
- from hivenode.sync.sync_log import SyncLog
- from hivenode.sync.ignore import load_ignore_patterns, should_sync
- from hivenode.sync.engine import SyncEngine

Functions:
- sync_log_db(): Temporary sync log database.
- test_sync_log_queue_sync(sync_log_db): Test queueing a sync entry.
- test_sync_log_mark_synced(sync_log_db): Test marking a sync entry as synced.
- test_sync_log_mark_conflict(sync_log_db): Test marking a sync entry as conflict.
- test_sync_log_mark_failed(sync_log_db): Test marking a sync entry as failed.
- test_load_ignore_patterns(): Test loading ignore patterns from file.
- test_should_sync_glob_pattern(): Test glob pattern matching.
- test_should_sync_directory_pattern(): Test directory pattern matching.
- test_should_sync_always_skip(): Test that .git/, node_modules/, __pycache__/ are always skipped.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
