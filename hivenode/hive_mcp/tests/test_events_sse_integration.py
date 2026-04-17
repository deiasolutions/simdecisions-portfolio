"""
test_events_sse_integration
===========================

Integration test for /mcp/events SSE endpoint with full server.

Dependencies:
- import pytest
- import json
- import subprocess
- import time
- import urllib.request
- from hivenode.hive_mcp.sync import SyncQueueWriter
- import os
- import sys
- from pathlib import Path
- from hivenode.hive_mcp import local_server

Functions:
- test_sync_queue(tmp_path): Create test sync queue directory.
- test_server(tmp_path, test_sync_queue, monkeypatch): Start test MCP server on a different port.
- test_sse_endpoint_live(test_server, test_sync_queue): Test SSE endpoint with live server.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
