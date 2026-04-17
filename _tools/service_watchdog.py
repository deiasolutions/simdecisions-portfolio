"""
service_watchdog
================

Service watchdog - monitors and restarts hivenode, queue runner, and vite.
Run: python _tools/service_watchdog.py
Checks every 10 minutes. Restarts dead services. Logs everything.

Dependencies:
- import json
- import subprocess
- import time
- import urllib.request
- from datetime import datetime
- from pathlib import Path

Functions:
- log(msg): Return True if something is listening on the port.
- check_hivenode(): Check hivenode health endpoint.
- get_active_tasks(): Get active tasks from build monitor before restart.
- find_process(search_term): Find a process by command line substring. Returns PID or None.
- kill_process(pid): Kill a process by PID.
- restart_hivenode(): Restart hivenode via uvicorn.
- restart_queue_runner(): Restart the queue runner.
- restart_vite(): Restart Vite dev server.
- snapshot_active_work(): Save active tasks so we can check them after restart.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
