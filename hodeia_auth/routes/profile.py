"""
profile
=======

Profile management routes for hodeia_auth.

Dependencies:
- from fastapi import APIRouter, Depends
- from sqlalchemy.orm import Session
- from hodeia_auth.db import get_session
- from hodeia_auth.models import User
- from hodeia_auth.dependencies import get_current_user
- from hodeia_auth.services.jwt import create_access_token
- from hodeia_auth.schemas import (

Functions:
- _user_to_profile(user: User): Return the authenticated user's profile.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
