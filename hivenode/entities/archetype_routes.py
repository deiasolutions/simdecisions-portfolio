"""
archetype_routes
================

Domain Archetype API Routes — ADR-003 TASK-043

Endpoints:
- POST /api/domains/{domain}/archetype/refresh   — Generate new archetype via tribunal
- GET  /api/domains/{domain}/archetype            — Get current archetype
- GET  /api/domains/{domain}/archetype/history     — Get archetype history
- POST /api/domains/{domain}/archetype/check-drift — Check embedding drift

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException
- from sqlalchemy.orm import Session
- from simdecisions.database import get_db
- from hivenode.entities.archetypes import (

Functions:
- _archetype_to_response(arch: DomainArchetype): Convert a DomainArchetype ORM object to a JSON-safe dict.
- refresh_archetype(domain: str,
    body: RefreshRequest,
    db: Session = Depends(get_db): Generate a new archetype via tribunal consensus.
- get_archetype(domain: str, db: Session = Depends(get_db): Get the current archetype for a domain.
- get_archetype_history(domain: str, db: Session = Depends(get_db): Get the full archetype history for a domain (newest first).
- check_archetype_drift(domain: str,
    body: DriftCheckRequest,
    db: Session = Depends(get_db): Check if a new text's embedding has drifted from the current archetype.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
