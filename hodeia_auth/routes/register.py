"""
register
========

User registration endpoint.

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException, Request
- from sqlalchemy import select
- from sqlalchemy.orm import Session
- from slowapi import Limiter
- from slowapi.util import get_remote_address
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User
- from hodeia_auth.schemas import RegisterRequest, RegisterResponse
- from hodeia_auth.services.password import hash_password
- from hodeia_auth.services.audit import emit_register_event

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
