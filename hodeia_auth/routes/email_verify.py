"""
email_verify
============

Email verification endpoints for hodeia_auth.

Dependencies:
- import hashlib
- import secrets
- from datetime import datetime, UTC, timedelta
- from fastapi import APIRouter, Depends, HTTPException, Request
- from sqlalchemy.orm import Session
- from pydantic import BaseModel
- from slowapi import Limiter
- from slowapi.util import get_remote_address
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User

Classes:
- EmailVerificationStore: In-memory store for email verification codes.
- SendVerificationRequest: Request to send email verification code.
- SendVerificationResponse: Response after sending verification code.
- VerifyEmailRequest: Request to verify email with code.
- VerifyEmailResponse: Response after email verification.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
