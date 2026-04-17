"""
bot_http_server
===============

Bot HTTP Server - FastAPI server for HTTP/WebSocket communication with bots.

Provides REST API and WebSocket endpoints for:
- Bot health checks (/status)
- Task submission via HTTP (POST /api/task)
- Real-time interaction via WebSocket (/ws)
- Priority queue management (WebSocket > file queue)

Dependencies:
- from fastapi import FastAPI, WebSocket, HTTPException
- from fastapi.responses import JSONResponse, HTMLResponse
- import asyncio
- import json
- import logging
- from datetime import datetime
- from typing import Optional, Dict, Any
- import uuid
- from pathlib import Path

Classes:
- BotHTTPServer: Lightweight FastAPI server for bot HTTP/WebSocket communication.

Functions:
- create_bot_http_server(bot_id: str, port: int, bot_runner=None): Create FastAPI app for bot HTTP server.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
