"""
efemera_smoke
=============

Efemera full smoke test — backend API + frontend browser.

Usage:
    python tests/efemera_smoke.py

What it does:
  1. Kills any existing hivenode on :8420
  2. Starts fresh hivenode
  3. Runs backend API smoke tests (channels, messages, members, presence)
  4. Opens browser to frontend with test data pre-loaded
  5. Prints summary

Dependencies:
- import json
- import os
- import socket
- import subprocess
- import sys
- import time
- import urllib.parse
- import urllib.request
- import urllib.error
- import webbrowser

Functions:
- req(method: str, url: str, data: dict | None = None): Kill all processes listening on a port (Windows).
- wait_for_server(retries: int = 15): Check if Vite dev server is running, offer to open browser.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
