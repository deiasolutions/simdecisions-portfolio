"""
preferences
===========

User preferences API routes.

GET  /api/user/preferences  — fetch preferences for authenticated user
PUT  /api/user/preferences  — upsert preferences for authenticated user

Dependencies:
- from typing import Any
- from fastapi import APIRouter, Depends
- from pydantic import BaseModel
- from hivenode.dependencies import verify_jwt_or_local, get_preferences_store
- from hivenode.preferences.store import PreferencesStore

Classes:
- PreferencesBody: Get the authenticated user's preferences.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
