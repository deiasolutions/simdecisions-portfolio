"""
dev_login
=========

Dev-login bypass endpoint for hodeia_auth (local mode only).

TASK-136: Port GitHub OAuth + JWKS
Bee: BEE-2026-03-15-TASK-136-ra96it-git

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException
- from sqlalchemy import select
- from sqlalchemy.orm import Session
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User
- from hodeia_auth.schemas import DevLoginAvailableResponse, OAuthTokenResponse, OAuthUserResponse
- from hodeia_auth.services.jwt import create_access_token
- from hodeia_auth.config import settings

Functions:
- _dev_login_allowed(): Check if dev-login is available (local mode, no GitHub OAuth configured).
- _ensure_local_user(session: Session): Ensure local-user exists in database.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
