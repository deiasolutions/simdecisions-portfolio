"""
tabletop_routes
===============

Tabletop Mode Backend API Routes — TASK-CANVAS-007

Provides a unified /api/tabletop/interact endpoint for managing tabletop sessions.
The frontend calls this endpoint with different actions: start, decide, ask, end.

Session state is stored in memory (dict) for now. Future: persist to SQLite.

Endpoints:
    POST /api/tabletop/interact — Unified endpoint for all tabletop actions

Dependencies:
- from __future__ import annotations
- from typing import Literal
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from hivenode.tabletop_walker import GraphWalker

Classes:
- NodeSchema: Node schema from ReactFlow.
- EdgeSchema: Edge schema from ReactFlow.
- FlowSchema: Flow schema containing nodes and edges.
- MessageHistoryItem: A single message in the chat history.
- TabletopInteractRequest: Unified request for tabletop interactions.
- TabletopInteractResponse: Unified response for tabletop interactions.

Functions:
- _get_or_create_session(session_id: str): Get an existing session or create a new one.
- _flow_to_dicts(flow: FlowSchema): Convert Pydantic flow schema to dict lists.
- tabletop_interact(request: TabletopInteractRequest): Unified endpoint for tabletop session interactions.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
