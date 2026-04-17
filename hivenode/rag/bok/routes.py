"""
routes
======

BOK (Body of Knowledge) API routes.

Dependencies:
- from fastapi import APIRouter, Depends, Query, HTTPException
- from pydantic import BaseModel
- from typing import List
- from hivenode.dependencies import verify_jwt_or_local
- from simdecisions.database import get_db
- from hivenode.rag.bok.rag_service import search_bok, enrich_prompt
- from sqlalchemy.orm import Session

Classes:
- BokSearchResponse: Response from BOK search.
- EnrichRequest: Request to enrich prompt with BOK.
- EnrichResponse: Response from prompt enrichment.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
