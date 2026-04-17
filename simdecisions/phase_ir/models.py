"""
models
======

ORM models and Pydantic schemas for persisting PHASE-IR flows in the database.

Dependencies:
- from __future__ import annotations
- import uuid
- from datetime import datetime
- from pydantic import BaseModel, ConfigDict
- from sqlalchemy import Column, DateTime, Integer, String, Text
- from sqlalchemy.sql import func
- from ..database import Base

Classes:
- FlowRecord: Persisted representation of a PHASE-IR flow.
- FlowVersion: Immutable version snapshot of a PHASE-IR flow.
- FlowRecordResponse: Body for POST /api/phase/flows.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
