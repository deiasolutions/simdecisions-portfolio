"""
test_phase_trace
================

Tests for PHASE-IR Trace Format & Ledger Integration (ADR-007).

TASK-075 -- 18+ tests covering the TraceEvent dataclass, PhaseTraceEvent ORM,
all trace functions, and the API routes.

Dependencies:
- import json
- import uuid
- import pytest
- from fastapi.testclient import TestClient
- from sqlalchemy import create_engine
- from sqlalchemy.orm import sessionmaker
- from sqlalchemy.pool import StaticPool
- from simdecisions.database import Base, get_db
- from hivenode.main import app
- from simdecisions.phase_ir.trace import (

Functions:
- _tid(): Short random test id.
- db(): Yield a test DB session, rolling back after each test.
- trace_client(): TestClient with dependency override for in-memory DB.
- test_trace_event_has_correct_fields(): TraceEvent should have all required PHASE-IR extension fields.
- test_create_trace_event_valid(): create_trace_event should produce a TraceEvent with auto-generated id and timestamp.
- test_create_trace_event_invalid_type(): create_trace_event should raise ValueError for an invalid event_type.
- test_emit_trace_event_persists(db): emit_trace_event should write a row to the database.
- test_emit_flow_started(db): emit_flow_started should create and persist a flow_started event.
- test_emit_node_event_started(db): emit_node_event with node_started should persist correctly.
- test_emit_node_event_completed(db): emit_node_event with node_completed should persist correctly.
- test_emit_token_event(db): emit_token_event with token_created should persist correctly.
- test_emit_resource_event(db): emit_resource_event with resource_requested should persist correctly.
- test_get_trace_ordered(db): get_trace should return events ordered by sim_time.
- test_get_trace_by_node(db): get_trace_by_node should filter events to a single node.
- test_get_trace_by_type(db): get_trace_by_type should filter events by event_type.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
