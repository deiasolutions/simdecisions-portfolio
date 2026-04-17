"""
routes
======

Bot embedding API routes — register, pi, drift check.

Dependencies:
- from typing import Optional
- from fastapi import APIRouter, Depends, HTTPException, status
- from pydantic import BaseModel
- from sqlalchemy.orm import Session
- from hivenode.dependencies import verify_jwt_or_local
- from simdecisions.database import get_db
- from hivenode.entities.embeddings import (
- from hivenode.entities.vectors_core import EntityComponent

Classes:
- RegisterRequest: Request schema for bot profile registration.
- RegisterResponse: Response schema for bot profile registration.
- PiResponse: Response schema for pi computation.
- CheckDriftRequest: Request schema for drift detection.
- DriftResponse: Response schema for drift detection.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
