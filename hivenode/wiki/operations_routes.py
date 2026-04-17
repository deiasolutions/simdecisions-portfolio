"""
operations_routes
=================

Wiki operations and ONET API routes.

Dependencies:
- from pathlib import Path
- from typing import Optional
- from fastapi import APIRouter, Depends, HTTPException, status, Query
- from sqlalchemy import select, and_
- from hivenode.dependencies import verify_jwt_or_local
- from hivenode.wiki.store import (
- from hivenode.wiki.operations import ingest_source, query_wiki, lint_wiki
- from hivenode.wiki.schemas import (

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
