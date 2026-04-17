"""
dependencies
============

FastAPI dependencies for hodeia_auth routes.

Dependencies:
- from fastapi import Depends, HTTPException, status
- from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
- from sqlalchemy import select
- from sqlalchemy.orm import Session
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User
- from hodeia_auth.services.jwt import decode_access_token
- from hodeia_auth.services.bot_token import BotTokenService

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
