"""
recovery_email
==============

Recovery email setup routes.

POST /recovery-email/send   — send verification code to recovery email
POST /recovery-email/verify — verify code, mark recovery email as verified

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException
- from sqlalchemy.orm import Session
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User
- from hodeia_auth.dependencies import get_current_user
- from hodeia_auth.schemas import (
- from hodeia_auth.services.mfa import send_mfa_code, verify_mfa_code
- from hodeia_auth.config import settings

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
