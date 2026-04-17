"""
hivenode-service
================

Hivenode background service launcher.

Keeps hivenode running on port 8420 so bee heartbeats are always captured.
Restarts automatically on crash. Logs to .deia/hive/hivenode-service.log.

Install as:
  Windows:  python _tools/hivenode-service.py install
  macOS:    python _tools/hivenode-service.py install
  Manual:   python _tools/hivenode-service.py run

Uninstall:
  python _tools/hivenode-service.py uninstall

Dependencies:
- import platform
- import subprocess
- import sys
- import time
- from pathlib import Path

Functions:
- find_python(): Find the Python executable that has uvicorn installed.
- run_hivenode(): Run hivenode in a restart loop. Restarts on crash, max 5 retries.
- install_windows(): Register as a Windows Task Scheduler task that runs at logon.
- install_macos(): Register as a macOS launchd agent that runs at login.
- uninstall_windows(): Check if hivenode is responding.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
