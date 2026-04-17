"""
routes
======

Playback API routes — TASK-CANVAS-006.

Backend API for simulation playback:
- POST /api/playback/store — store simulation events
- GET /api/playback/{flow_id}/{run_id} — retrieve events for playback
- GET /api/playback/{flow_id}/runs — list all runs for a flow
- DELETE /api/playback/{flow_id}/{run_id} — delete playback session

Dependencies:
- from __future__ import annotations
- from typing import List, Dict, Any, Optional
- from pathlib import Path
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from hivenode.playback.store import PlaybackStore

Classes:
- PlaybackEvent: Single playback event.
- StoreRequest: Request to store playback events.
- StoreResponse: Response after storing events.
- RetrieveResponse: Response when retrieving events.
- RunSummary: Summary of a single run.
- ListRunsResponse: Response when listing runs for a flow.
- DeleteResponse: Response after deleting a run.

Functions:
- get_store(): Get or create the global playback store instance.
- store_playback_events(request: StoreRequest): Store simulation events for playback.
- list_playback_runs(flow_id: str): List all playback runs for a flow.
- retrieve_playback_events(flow_id: str, run_id: str): Retrieve playback events for a specific run.
- delete_playback_session(flow_id: str, run_id: str): Delete playback session (all events for a run).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
