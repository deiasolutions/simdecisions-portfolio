"""
test_auth_identity
==================

Tests for /auth/identity endpoint.

Dependencies:
- import pytest
- from httpx import AsyncClient, ASGITransport
- from hivenode.main import app
- from hivenode.config import HivenodeConfig
- from hivenode.services.jwks_cache import JWKSCache
- from hivenode.dependencies import set_jwks_cache
- from tests.hivenode.conftest import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
- import jwt
- from datetime import datetime, UTC, timedelta

Functions:
- create_test_token(user_id="test-user", email="test@example.com"): Create a test JWT token for identity tests.
- local_settings(tmp_path, monkeypatch): Local mode config for identity tests.
- cloud_settings(tmp_path, monkeypatch): Cloud mode config for identity tests.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
