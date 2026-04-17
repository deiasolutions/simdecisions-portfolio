"""
sessions
========

Session management endpoints for hodeia_auth.

Dependencies:
- from datetime import datetime
- from fastapi import APIRouter, Depends, HTTPException
- from sqlalchemy import select
- from sqlalchemy.orm import Session
- from pydantic import BaseModel
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User, RefreshToken
- from hodeia_auth.dependencies import get_current_user
- from hodeia_auth.services.token import revoke_all_user_tokens
- from hodeia_auth.services.audit import emit_token_revoke_event

Classes:
- SessionInfo: Information about an active session (refresh token).
- SessionsListResponse: List of active sessions.
- SessionRevokeResponse: Response after revoking a session.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
