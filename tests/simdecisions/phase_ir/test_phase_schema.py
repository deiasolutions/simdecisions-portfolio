"""
test_phase_schema
=================

Tests for PHASE-IR schema: primitives, serialization, validation, ORM, and API.

TASK-070 — ADR-007 PHASE-IR Schema Definition

Dependencies:
- import uuid
- import pytest
- from fastapi.testclient import TestClient
- from sqlalchemy import create_engine
- from sqlalchemy.orm import sessionmaker
- from sqlalchemy.pool import StaticPool
- from simdecisions.database import Base, get_db
- from hivenode.main import app
- from simdecisions.phase_ir.primitives import (
- from simdecisions.phase_ir.schema import (

Functions:
- _tid(): Short random test id.
- _make_simple_flow(flow_id: str | None = None): Build a minimal valid Flow for testing.
- _make_flow_dict(flow_id: str | None = None): Return a plain dict for a simple flow (API payloads).
- db(): Yield a test DB session, rolling back after each test.
- phase_client(): TestClient with dependency override pointing at the in-memory DB.
- test_create_port(): flow_to_dict -> dict_to_flow should reconstruct an equivalent Flow.
- test_dict_to_flow_reconstruction(): dict_to_flow should handle extended primitives.
- test_yaml_roundtrip(): flow_to_yaml -> yaml_to_flow should produce an equivalent Flow.
- test_json_roundtrip(): flow_to_json -> json_to_flow should produce an equivalent Flow.
- test_validate_valid_flow(): Create, read, update, delete a FlowRecord via ORM.
- test_flow_version_crud(db): Create and read a FlowVersion via ORM.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
