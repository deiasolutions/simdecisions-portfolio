"""
watcher
=======

File System Watcher

Watches volume paths for file changes and queues them for sync.
Supports:
- File write detection
- Ignore patterns (gitignore syntax)
- Debouncing (wait for writes to settle before queueing)

Dependencies:
- import logging
- import time
- from pathlib import Path
- from typing import Dict
- from watchdog.observers import Observer
- from watchdog.events import FileSystemEventHandler, FileSystemEvent
- from hivenode.sync.sync_log import SyncLog
- from hivenode.storage.provenance import compute_content_hash
- from hivenode.sync.ignore import should_sync

Classes:
- SyncFileHandler: File system event handler for sync operations.
- FileWatcher: File system watcher for sync operations.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
