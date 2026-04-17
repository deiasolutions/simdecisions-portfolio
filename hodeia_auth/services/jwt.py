"""
jwt
===

JWT token creation and verification using RS256.

Dependencies:
- from datetime import datetime, UTC, timedelta
- from typing import Dict, Any
- import jwt
- from hodeia_auth.config import settings

Functions:
- create_access_token(user_id: str,
    email: str,
    tier: str,
    private_key: str | None = None,
    provider: str | None = None,
    provider_id: str | None = None,
    display_name: str | None = None,
    scope: str = "chat",
    needs_setup: bool = False,): Create a JWT access token with RS256 signing.
- decode_access_token(token: str,
    public_key: str | None = None,): Decode and verify a JWT access token.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
