"""
schema_routes
=============

FastAPI routes for PHASE-IR flow CRUD and validation.

Prefix: /api/phase

Dependencies:
- from __future__ import annotations
- import json
- import uuid
- from fastapi import APIRouter, Depends, HTTPException
- from sqlalchemy.orm import Session
- from ..database import get_db
- from .models import (
- from .schema import dict_to_flow, flow_to_json, validate_flow_structure

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
