"""
analytics_routes
================

Analytics API routes — beacon receiver + stats endpoint.

Dependencies:
- import logging
- from time import time
- from typing import Optional
- from fastapi import APIRouter, Request, Depends, HTTPException
- from pydantic import BaseModel
- from hivenode.dependencies import verify_jwt_or_local
- from hivenode.analytics.store import record_pageview, get_stats

Classes:
- BeaconRequest: Extract domain from Origin or Referer header.

Functions:
- _extract_domain(request: Request): Extract domain from Origin or Referer header.
- _check_rate_limit(ip: str): Check if IP is within rate limit. Returns True if allowed, False if exceeded.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
