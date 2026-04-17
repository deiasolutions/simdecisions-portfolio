"""
build_monitor
=============

Build monitor routes — live heartbeat tracking + file claim system.

Heartbeat endpoints:
- POST /build/heartbeat — stores heartbeat from dispatch/queue processes
- GET /build/status — returns full state snapshot
- GET /build/stream — SSE that pushes every heartbeat live
- POST /build/ping — lightweight liveness ping (no logging)

File claim endpoints (parallel bee deconfliction):
- POST /build/claim — bee claims files it will touch
- GET /build/claims — check all active claims
- POST /build/release — bee releases its claims when done

State persists to .deia/hive/queue/monitor-state.json on every heartbeat.
Loaded on startup so server restarts don't lose history.

Dependencies:
- import asyncio
- import json
- import re
- import time
- from datetime import datetime
- from enum import Enum
- from pathlib import Path
- from typing import Optional
- import yaml
- from fastapi import APIRouter, Request

Classes:
- BuildStatus: Valid build monitor task statuses.
- HeartbeatPayload: Validate status is a recognized BuildStatus value.
- BuildState: Build monitor state with local file persistence.
- CancelPayload: Cancel an active task.

Functions:
- _load_capacity(config_path: Optional[Path] = None): Load max_parallel_bees from queue.yml.
- _detect_task_type(task_id: str): Detect task type from ID prefix.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
