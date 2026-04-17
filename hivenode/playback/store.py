"""
store
=====

Playback store — SQLite storage for simulation playback events.

Stores simulation events for replay in PlaybackMode.
Each run (flow_id + run_id) contains ordered events stored as JSON.

Dependencies:
- from __future__ import annotations
- import json
- import sqlite3
- from datetime import datetime, UTC
- from typing import List, Dict, Any

Classes:
- PlaybackStore: SQLite store for playback events.

Functions:
- create_playback_schema(conn: sqlite3.Connection): Create playback_events table.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
