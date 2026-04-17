"""
stop
====

ShiftCenter local development shutdown script.

Finds and stops all dev services by port:
- Hivenode (8420)
- Vite dev server (5173)
- Queue runner (by process name pattern)
- MCP server (8421)

Usage:
    python _tools/stop.py           # Stop all services
    python _tools/stop.py --force   # Force kill (no graceful wait)

Dependencies:
- import argparse
- import os
- import platform
- import signal
- import subprocess
- import time

Functions:
- find_pids_on_port(port: int): Find PIDs listening on a given port.
- find_queue_runner_pids(): Find queue runner processes.
- kill_pid(pid: int, force: bool = False): Kill a process by PID. Returns True if killed.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
