"""
token
=====

Refresh token management service.

Dependencies:
- import secrets
- import hashlib
- from datetime import datetime, UTC, timedelta
- from typing import Optional, Tuple
- from sqlalchemy import select, update
- from sqlalchemy.orm import Session
- from hodeia_auth.models import RefreshToken
- from hodeia_auth.config import settings

Functions:
- generate_token(): Generate a secure random token.
- hash_token(token: str): Hash a token using SHA-256.
- issue_refresh_token(session: Session,
    user_id: str,): Issue a new refresh token for a user.
- get_refresh_token(session: Session,
    raw_token: str,): Get refresh token by raw token value.
- is_token_valid(token: RefreshToken): Check if a refresh token is valid (not consumed, not revoked, not expired).
- rotate_refresh_token(session: Session,
    raw_token: str,): Rotate a refresh token (consume old, issue new).
- detect_replay_attack(session: Session,
    raw_token: str,): Detect if a consumed token is being reused (replay attack).
- revoke_refresh_token(session: Session,
    raw_token: str,): Revoke a single refresh token.
- revoke_all_user_tokens(session: Session,
    user_id: str,): Revoke all refresh tokens for a user (breach response).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
