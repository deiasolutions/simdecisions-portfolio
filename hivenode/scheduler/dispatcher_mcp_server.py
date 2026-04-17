"""
dispatcher_mcp_server
=====================

Dispatcher MCP server — receives queue events via HTTP.

Lightweight FastAPI app that receives MCP events from hivenode and
calls dispatcher daemon's event handler.

Runs on port 8423.

Dependencies:
- import logging
- from fastapi import FastAPI, Request
- from fastapi.responses import JSONResponse

Functions:
- set_daemon(daemon): Set global daemon reference.
- run_server(daemon_instance, port: int = 8423): Run MCP server in foreground.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
