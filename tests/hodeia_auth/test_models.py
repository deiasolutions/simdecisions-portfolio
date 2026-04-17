"""
test_models
===========

Tests for hodeia_auth SQLAlchemy models.

Dependencies:
- import pytest
- from datetime import datetime, UTC, timedelta
- from sqlalchemy import select
- from hodeia_auth.models import User, RefreshToken, LoginSession

Functions:
- test_user_creation(session): Test creating a user with default values.
- test_user_unique_email(session): Test that email must be unique.
- test_user_with_sms_mfa(session): Test creating a user with SMS MFA.
- test_user_tier_values(session): Test valid tier values.
- test_refresh_token_creation(session): Test creating a refresh token.
- test_refresh_token_unique_hash(session): Test that token_hash must be unique.
- test_refresh_token_cascade_delete(session): Test that refresh tokens are deleted when user is deleted.
- test_login_session_creation(session): Test creating a login session.
- test_login_session_cascade_delete(session): Test that login sessions are deleted when user is deleted.
- test_user_relationships(session): Test user model relationships.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
