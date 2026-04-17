"""
sync_daemon
===========

Background daemon for orchestrating markdown export and cloud sync.

This module provides the SyncDaemon class that coordinates when and how
index records are synced to markdown files and cloud PostgreSQL based on
configurable policies (IMMEDIATE, BATCHED, MANUAL).

Ported from platform/efemera/src/efemera/indexer/sync_daemon.py.

Dependencies:
- import logging
- import os
- import threading
- import time
- from datetime import datetime
- from enum import Enum
- from typing import Optional
- from hivenode.rag.indexer.cloud_sync import CloudSyncService
- from hivenode.rag.indexer.markdown_exporter import MarkdownExporter
- from hivenode.rag.indexer.storage import IndexStorage

Classes:
- SyncPolicy: Sync policy for daemon behavior.
- SyncDaemon: Background daemon that orchestrates markdown export and cloud sync.

Functions:
- create_daemon_from_env(storage: IndexStorage,
    exporter: MarkdownExporter,
    cloud_sync: CloudSyncService,): Create SyncDaemon instance from environment variables.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
