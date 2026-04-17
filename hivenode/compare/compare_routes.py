"""
compare_routes
==============

Compare API Routes — Backend for CompareMode

Endpoints:
    POST /api/compare/diff       — compute diff between two flows
    POST /api/compare/snapshot   — store flow snapshot
    GET  /api/compare/snapshots/{flow_id} — list snapshots for a flow
    DELETE /api/compare/snapshot/{snapshot_id} — delete snapshot

TASK-CANVAS-008: Wire Compare Mode to Backend API

Dependencies:
- from __future__ import annotations
- import uuid
- from datetime import datetime, timezone
- from typing import Any, Optional
- from dataclasses import asdict
- from fastapi import APIRouter, HTTPException, Depends
- from pydantic import BaseModel, Field
- from sqlalchemy.orm import Session
- from simdecisions.database import get_db
- from hivenode.compare.models import FlowSnapshot as FlowSnapshotModel

Classes:
- PositionSchema: Convert Pydantic schema to internal FlowSnapshot dataclass.

Functions:
- schema_to_snapshot(schema: FlowSnapshotSchema): Convert Pydantic schema to internal FlowSnapshot dataclass.
- node_diff_to_schema(node_diff: NodeDiff): Convert internal NodeDiff to Pydantic schema.
- edge_diff_to_schema(edge_diff: EdgeDiff): Convert internal EdgeDiff to Pydantic schema.
- metrics_delta_to_schema(delta: MetricsDelta): Convert internal MetricsDelta to Pydantic schema.
- compare_diff(request: DiffRequest): Compute diff between two flows.
- store_snapshot(snapshot: FlowSnapshotSchema,
    db: Session = Depends(get_db): Store a flow snapshot for later comparison.
- list_snapshots(flow_id: str,
    db: Session = Depends(get_db): List all snapshots for a flow.
- delete_snapshot(snapshot_id: str,
    db: Session = Depends(get_db): Delete a snapshot.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
