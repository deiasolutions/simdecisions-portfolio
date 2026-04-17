"""
optimize_routes
===============

Optimize Mode API Routes — TASK-CANVAS-005C-3

Routes for parameter sweep, Pareto frontier, and AI suggestions.

Endpoints:
    POST /api/des/sweep    — parameter sweep over flow
    POST /api/des/pareto   — compute Pareto frontier from points
    POST /api/des/optimize — AI suggestion analysis (mock)

Dependencies:
- from __future__ import annotations
- import uuid
- from typing import Optional
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from simdecisions.des.sweep import (
- from simdecisions.optimization.core import (
- from hivenode.routes.des_routes import FlowSchema, _schema_to_flow

Classes:
- SweepParameterSchema: Convert Pydantic SweepConfigSchema to SweepConfig dataclass.

Functions:
- _schema_to_sweep_config(schema: Optional[SweepConfigSchema]): Convert Pydantic SweepConfigSchema to SweepConfig dataclass.
- _sweep_results_to_response(results: SweepResults): Convert SweepResults to API response format.
- des_sweep(request: SweepRequest): Run a parameter sweep over a flow.
- des_pareto(request: ParetoRequest): Compute Pareto frontier from a set of evaluated points.
- des_optimize(request: OptimizeRequest): Run AI suggestion analysis on execution ledger.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
