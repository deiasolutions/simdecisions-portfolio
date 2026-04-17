"""
queue_watcher
=============

Queue folder watcher — watchdog-based monitoring for queue directories.

Monitors queue directories and emits MCP events when specs move between folders.
Consolidates monitoring from 3 independent polling services (queue-runner,
scheduler, dispatcher) into a single event-driven watcher.

Design: .deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md

Dependencies:
- import json
- import logging
- import threading
- import time
- from datetime import datetime, timezone
- from pathlib import Path
- from typing import Optional
- from watchdog.events import FileSystemEventHandler
- from watchdog.observers import Observer
- from hivenode.spec_utils import extract_task_id_from_spec

Classes:
- QueueEventHandler: Watchdog event handler for queue directory monitoring.
- QueueWatcher: Watchdog observer manager for queue directories.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
