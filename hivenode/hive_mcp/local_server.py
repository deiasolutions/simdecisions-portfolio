"""
local_server
============

Hive MCP local server - Streamable HTTP transport on localhost:8421.

This is a separate FastAPI application from the main hivenode (port 8420).
It provides MCP protocol access to hive state and operations via Streamable HTTP transport.

Phase 0 tools:
- queue_list: List specs in queue
- queue_peek: Read a specific spec
- task_list: List active tasks
- task_read: Read a specific task with frontmatter

Run: python -m hivenode.hive_mcp.local_server

Dependencies:
- import os
- import time
- import logging
- from pathlib import Path
- from typing import Any, Sequence
- from mcp.server import Server
- from mcp.types import Tool, TextContent
- from starlette.routing import Route
- from starlette.responses import Response
- from hivenode.hive_mcp.state import StateManager

Functions:
- _find_repo_root(): Find repository root by looking for .deia directory.
- _patch_repo_root(): Patch _find_repo_root in tools modules to use our implementation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
