"""
dispatcher_daemon
=================

Dispatcher Daemon — reads schedule.json, moves specs from backlog/ to queue/.

The dispatcher is the execution arm of the scheduler. It:
1. Reads schedule.json to see what tasks are ready to dispatch
2. Counts active bees (_active/) and queued specs (queue/ root)
3. Calculates available slots: max_bees - active_count - queued_count
4. Moves top N spec files from backlog/ to queue/ root
5. Logs dispatches to dispatched.jsonl (scheduler reads this)
6. Logs actions to dispatcher_log.jsonl (ops visibility)

Usage:
    # Start daemon (default: max_bees=10)
    python dispatcher_daemon.py

    # Custom max_bees
    python dispatcher_daemon.py --max-bees 5

    # Dry-run mode (log what it would dispatch, but don't move files)
    python dispatcher_daemon.py --dry-run

    # Custom directories
    python dispatcher_daemon.py --schedule-dir .deia/hive --queue-dir .deia/hive/queue

Dependencies:
- import argparse
- import json
- import logging
- import shutil
- import signal
- import sys
- import threading
- import time
- from datetime import datetime, UTC
- from pathlib import Path

Classes:
- DispatcherDaemon: Dispatcher daemon that moves specs from backlog/ to queue/.

Functions:
- _load_max_bees_from_config(queue_dir: Path): Read max_parallel_bees from queue.yml. Default 10.
- main(): CLI entry point.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
