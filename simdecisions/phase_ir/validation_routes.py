"""
validation_routes
=================

FastAPI routes for PHASE-IR flow validation (TASK-072).

Prefix: /api/phase

Dependencies:
- from __future__ import annotations
- from fastapi import APIRouter
- from pydantic import BaseModel, Field
- from .schema import dict_to_flow
- from .validation import (

Classes:
- ValidateRequest: Request body for POST /api/phase/validate.
- ValidationIssueResponse: Validate a PHASE-IR flow graph at the specified level and mode.

Functions:
- validate_flow_endpoint(body: ValidateRequest): Validate a PHASE-IR flow graph at the specified level and mode.
- list_validation_rules(): Return all validation rules with codes and descriptions.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
