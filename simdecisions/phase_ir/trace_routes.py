"""
trace_routes
============

FastAPI routes for PHASE-IR trace events (ADR-007).

Prefix: /api/phase/traces

Dependencies:
- from __future__ import annotations
- from fastapi import APIRouter, Depends, Query
- from pydantic import BaseModel, ConfigDict
- from sqlalchemy.orm import Session
- from ..database import get_db
- from .trace import (

Classes:
- TraceEventResponse: Return all trace events for a given run, ordered by sim_time.
- ImportBody: Import trace events from a JSONL string.

Functions:
- get_run_trace(run_id: str, db: Session = Depends(get_db): Return all trace events for a given run, ordered by sim_time.
- get_run_trace_summary(run_id: str, db: Session = Depends(get_db): Return a summary of the trace for a run.
- get_run_events(run_id: str,
    event_type: str | None = Query(default=None): Return trace events with optional event_type and/or node_id filters.
- export_run_trace(run_id: str, db: Session = Depends(get_db): Export all trace events for a run as JSONL.
- import_trace(body: ImportBody, db: Session = Depends(get_db): Import trace events from a JSONL string.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
