"""
test_sync_queue
===============

Tests for SyncQueue.flush() async conversion.

Tests edge cases:
1. Flush with empty queue → returns {"flushed": 0, "pending": 0}
2. Flush with 5 queued writes, all succeed → returns {"flushed": 5, "pending": 0}
3. Flush with 5 queued writes, 3 succeed, 2 fail → returns {"flushed": 3, "pending": 2}
4. Adapter write raises exception → queue file preserved, counted as pending
5. Concurrent flush calls (should be safe, idempotent)
6. File read/write operations don't block event loop

Dependencies:
- import asyncio
- import base64
- import json
- import tempfile
- from pathlib import Path
- from unittest.mock import Mock
- import pytest
- from hivenode.storage.adapters.sync_queue import SyncQueue

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
