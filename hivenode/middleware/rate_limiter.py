"""
rate_limiter
============

Rate limiting middleware for auth routes.

Dependencies:
- import asyncio
- from datetime import datetime, UTC
- from typing import Dict, List, Optional
- from fastapi import Request
- from starlette.middleware.base import BaseHTTPMiddleware
- from starlette.responses import Response
- import logging
- from hivenode import dependencies

Classes:
- RateLimiterMiddleware: Sliding window rate limiter middleware for auth routes.

Functions:
- clear_rate_limit_state(): Clear all rate limit tracking. Used by test fixtures.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
