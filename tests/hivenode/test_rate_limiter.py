"""
test_rate_limiter
=================

Tests for rate limiting middleware on auth routes.

Dependencies:
- import pytest
- import asyncio
- from datetime import datetime, UTC, timedelta
- import jwt
- from httpx import AsyncClient, ASGITransport
- from hivenode.middleware.rate_limiter import RateLimiterMiddleware

Functions:
- create_test_token(user_id="test-user", expired=False): Create a test JWT token.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
