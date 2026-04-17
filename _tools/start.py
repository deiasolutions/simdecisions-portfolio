"""
start
=====

ShiftCenter local development startup script.

Launches all 4 services needed for development:
1. Hivenode (FastAPI backend on port 8420)
2. Vite dev server (browser frontend on port 5173)
3. Queue runner (watches queue, dispatches bees)
4. MCP server (live telemetry on port 8421)

Usage:
    python _tools/start.py              # Start all services
    python _tools/start.py --no-queue   # Skip queue runner
    python _tools/start.py --no-mcp     # Skip MCP server

Press Ctrl+C to stop all services cleanly.

Dependencies:
- import argparse
- import platform
- import subprocess
- import sys
- import time
- import urllib.request
- from pathlib import Path

Classes:
- Colors: ANSI color codes for terminal output.
- ServiceManager: Manages lifecycle of all 4 services.

Functions:
- color(text: str, color_code: str): Colorize text if colors are enabled.
- find_python(): Find the Python executable with required packages.
- find_npm(): Find npm executable.
- check_port(port: int, timeout: int = 30): Wait for a service to respond on localhost:port.
- check_vite_ready(timeout: int = 30): Wait for Vite dev server to be ready.
- main(): CLI entry point.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
