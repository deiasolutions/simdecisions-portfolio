"""
test_phase_validation
=====================

Tests for PHASE-IR Validation Engine — TASK-072

Covers all validation rules V-101 through V-404, plus the API endpoints.
Target: 40+ tests.

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
- from simdecisions.phase_ir.validation import (

Classes:
- TestV101UniqueNodeIds: A single node with no edges is acceptable.

Functions:
- _tid(): Build a minimal valid flow with N nodes chained by edges.
- _has_code(issues: list[ValidationIssue], code: str): TestClient with dependency override.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
