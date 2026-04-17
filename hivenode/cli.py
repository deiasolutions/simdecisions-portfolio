"""
cli
===

8os CLI tool for managing ShiftCenter hivenode.

Dependencies:
- import click
- import subprocess
- import platform
- import sys
- from pathlib import Path
- import yaml
- import psutil
- import httpx

Functions:
- main(): 8os - ShiftCenter local environment manager.
- up(): Start local hivenode.
- down(): Stop local hivenode.
- status(): Show hivenode status.
- sync(status): Sync home:// with cloud://.
- queue(status): Run build queue or show queue status.
- dispatch(task_file, model, role, inject_boot): Dispatch a single task file.
- index(full): Rebuild repo semantic search index.
- inventory(args): Manage feature inventory (passthrough to _tools/inventory.py).
- volumes(): List mounted volumes and their status.
- node(): Node management commands.
- node_list(): List connected nodes.
- node_announce(): Force re-announce to cloud.
- _trigger_sync(): Trigger immediate sync cycle.
- _show_sync_status(): Show sync status.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
