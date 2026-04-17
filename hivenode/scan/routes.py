"""
routes
======

SCAN API routes - sources, items, digests.

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException
- from typing import Optional
- from datetime import datetime
- from hivenode.dependencies import verify_jwt_or_local
- from .store import get_session
- from .models import ScanSource, ScanItem, ScanDigest
- from .service import ScanService

Functions:
- get_scan_service(): Dependency to get SCAN service.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
