"""
prism_routes
============

PRISM-IR API Routes

Endpoints for validating and processing PRISM-IR commands.

Dependencies:
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from typing import Any
- from hivenode.prism.ir_validator import validate_ir, validate_ir_strict
- from hivenode.routes.auth import verify_jwt_or_local

Classes:
- ValidateRequest: Request body for IR validation.
- ValidateResponse: Response for IR validation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
