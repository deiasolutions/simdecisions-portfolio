"""
temp_cleanup
============

hivenode/temp_cleanup.py
Temp file cleanup job: runs on boot + every 24 hours
Deletes temp files with expired TTLs (7-day default)

Dependencies:
- import asyncio
- import json
- import logging
- from datetime import datetime
- from pathlib import Path
- from typing import Callable

Functions:
- cleanup_expired_temp_files(temp_dir: Path): Scan temp directory for expired files and delete them.
- _remove_empty_parents(start_dir: Path, stop_at: Path): Remove empty parent directories up to (but not including) stop_at.
- schedule_cleanup_task(cleanup_fn: Callable[[], int], interval_hours: float = 24): Schedule cleanup task to run immediately and then every interval_hours.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
