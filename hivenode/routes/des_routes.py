"""
des_routes
==========

DES Engine API Routes — ADR-008 / TASK-146

Minimal FastAPI endpoints for running DES flows via the unified
SimulationEngine.

Endpoints:
    POST /api/des/run       — run a flow to completion
    POST /api/des/validate  — validate a flow before running
    POST /api/des/replicate — run multiple replications
    GET  /api/des/status    — engine health check

Dependencies:
- from __future__ import annotations
- import time
- from typing import Any, Optional
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.core import SimConfig
- from simdecisions.des.replication import (
- from simdecisions.phase_ir.primitives import (

Classes:
- NodeSchema: Convert a Pydantic FlowSchema into a PHASE-IR Flow dataclass.

Functions:
- _schema_to_flow(schema: FlowSchema): Convert a Pydantic FlowSchema into a PHASE-IR Flow dataclass.
- _schema_to_sim_config(schema: Optional[SimConfigSchema]): Convert a Pydantic SimConfigSchema into a SimConfig dataclass.
- des_run(request: RunRequest): Run a flow to completion and return results.
- des_validate(request: RunRequest): Validate a flow without running it.
- des_replicate(request: ReplicateRequest): Run multiple replications and return aggregate statistics with CIs.
- des_status(): Engine health check.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
