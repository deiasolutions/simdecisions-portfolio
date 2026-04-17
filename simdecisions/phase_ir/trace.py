"""
trace
=====

PHASE-IR Trace Format & Ledger Integration (ADR-007)

Extends the ADR-001 event ledger with PHASE-IR trace events for simulation
replay, debugging, and analysis.  25 standardised event types cover the full
lifecycle of flows, nodes, tokens, resources, variables, checkpoints, and
signals.

ORM model: PhaseTraceEvent  (table: phase_trace_events)
Dataclass:  TraceEvent       (in-memory representation)

Dependencies:
- from __future__ import annotations
- import json
- import uuid
- from dataclasses import dataclass, field
- from datetime import datetime, timezone
- from sqlalchemy import Column, DateTime, Float, Integer, String, Text
- from sqlalchemy.sql import func
- from sqlalchemy.orm import Session
- from ..database import Base

Classes:
- TraceEvent: A single PHASE-IR trace event (in-memory representation).
- PhaseTraceEvent: Persisted PHASE-IR trace event row.

Functions:
- create_trace_event(event_type: str,
    flow_id: str,
    run_id: str,
    **kwargs,): Create a new TraceEvent with auto-generated event_id and timestamp.
- emit_trace_event(event: TraceEvent, db: Session): Persist a TraceEvent to the database and return the ORM row.
- emit_flow_started(flow_id: str,
    run_id: str,
    mode: str,
    seed: int,
    db: Session,): Create and persist a ``flow_started`` trace event.
- emit_node_event(event_type: str,
    flow_id: str,
    run_id: str,
    node_id: str,
    db: Session,
    **payload,): Create and persist a node-level trace event.
- emit_token_event(event_type: str,
    flow_id: str,
    run_id: str,
    token_id: str,
    node_id: str,
    db: Session,
    **payload,): Create and persist a token-level trace event.
- emit_resource_event(event_type: str,
    flow_id: str,
    run_id: str,
    resource_id: str,
    token_id: str,
    db: Session,
    **payload,): Create and persist a resource-level trace event.
- get_trace(run_id: str, db: Session): Return all trace events for a run, ordered by sim_time then created_at.
- get_trace_by_node(run_id: str, node_id: str, db: Session): Return trace events for a specific node within a run.
- get_trace_by_type(run_id: str, event_type: str, db: Session): Return trace events of a specific type within a run.
- _row_to_dict(row: PhaseTraceEvent): Convert a PhaseTraceEvent row to a plain dict for JSONL export.
- export_trace_jsonl(run_id: str, db: Session): Export all trace events for a run as a JSONL string (one JSON object per line).
- import_trace_jsonl(jsonl: str, db: Session): Import trace events from a JSONL string.  Returns the count imported.
- get_trace_summary(run_id: str, db: Session): Return a summary dict for a run's trace.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
