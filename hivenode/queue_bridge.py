"""
queue_bridge
============

Bridge between hivenode and the queue runner.

Runs run_queue.py in a background thread via asyncio.to_thread(),
exposing a wake_event that MCP/REST can set to interrupt Fibonacci
backoff sleeps instantly.

Standalone mode (python run_queue.py --watch) is unaffected — it
passes no wake_event, so _interruptible_sleep falls back to time.sleep().

Dependencies:
- import importlib.util
- import logging
- import threading
- from pathlib import Path
- from typing import Optional
- from hivenode.service_bridge import ServiceBridge

Classes:
- QueueRunnerBridge: Thin wrapper that runs the queue runner inside hivenode's event loop.

Functions:
- _load_run_queue(repo_root: Path): Load run_queue module from .deia path without polluting sys.path.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
