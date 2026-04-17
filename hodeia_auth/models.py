"""
models
======

SQLAlchemy models for hodeia_auth authentication service.

Dependencies:
- from datetime import datetime, UTC
- from uuid import uuid4
- from typing import Optional
- from sqlalchemy import String, Boolean, DateTime, ForeignKey, CheckConstraint, Index, text
- from sqlalchemy.orm import Mapped, mapped_column, relationship
- from .db import Base

Classes:
- User: User account model.
- RefreshToken: Refresh token model for JWT token rotation.
- LoginSession: Login session model for MFA verification.
- BotToken: Bot token model for bot authentication.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
