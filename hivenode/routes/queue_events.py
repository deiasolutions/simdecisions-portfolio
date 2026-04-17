"""
queue_events
============

Queue event broadcasting routes — MCP notification endpoint.

Receives events from queue watcher and broadcasts to subscribers (scheduler, dispatcher).

Dependencies:
- import asyncio
- import logging
- import threading
- import time
- from typing import Dict, Any
- from fastapi import APIRouter, Request, HTTPException
- import httpx

Functions:
- should_emit_event(spec_file: str, directory: str): Check if event should be emitted (debounce duplicate events).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
