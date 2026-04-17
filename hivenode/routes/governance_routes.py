"""
governance_routes
=================

Governance Routes — Approval decisions API for gate_enforcer REQUIRE_HUMAN gates.

Endpoints:
- GET  /governance/pending          — List pending approval decisions
- POST /governance/resolve          — Resolve a pending approval (approve/reject)
- GET  /governance/history          — Historical approval decisions

Dependencies:
- import logging
- from datetime import datetime
- from typing import Optional
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel

Classes:
- ResolveRequest: List all pending human approval decisions.

Functions:
- register_pending_approval(approval_id: str,
    task_id: str,
    bee_id: str,
    action: str,
    context: str,
    priority: str = "normal",
    payload: Optional[dict] = None,
    diff: Optional[str] = None,): Register a new pending approval.
- get_pending_count(): Get count of pending approvals (for badge).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
