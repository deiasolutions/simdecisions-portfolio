"""
test_bidirectional_offline_sync
===============================

Tests for bidirectional offline sync (SPEC-BIDIRECTIONAL-OFFLINE-SYNC).

Covers:
1. Online sync (cloud reachable, hivenode running)
2. Offline queue (cloud unreachable, writes queue locally)
3. Reconnect flush (hivenode starts, pulls from cloud outbox)
4. Conflict resolution (last-write-wins)
5. Quota enforcement (10 MB default limit)

Dependencies:
- import pytest
- import tempfile
- from pathlib import Path
- from unittest.mock import patch, MagicMock
- from hivenode.sync.engine import SyncEngine
- from hivenode.sync.outbox import SyncOutbox
- from hivenode.sync.sync_log import SyncLog
- from hivenode.storage.registry import VolumeRegistry
- from hivenode.storage.provenance import ProvenanceStore
- from hivenode.storage.adapters.local import LocalFilesystemAdapter

Functions:
- temp_dirs(): Create temporary directories for test volumes.
- sync_components(temp_dirs): Initialize sync engine components.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
