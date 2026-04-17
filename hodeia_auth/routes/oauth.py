"""
oauth
=====

OAuth routes for hodeia_auth — GitHub + Google.

Generic provider pattern: provider + provider_id on User model.

Dependencies:
- import base64
- import json
- import logging
- import secrets
- from urllib.parse import urlencode
- from fastapi import APIRouter, Depends, HTTPException, Query, Request
- from fastapi.responses import RedirectResponse, Response
- from sqlalchemy import select
- from sqlalchemy.orm import Session
- from hodeia_auth.db import get_session

Functions:
- _resolve_redirect_uri(origin: str | None): Validate and return the redirect URI for OAuth. Falls back to FRONTEND_URL.
- _encode_state(origin: str): Encode origin + nonce into base64 state param.
- _decode_state(state: str): Decode base64 state param. Raises on invalid.
- _find_or_create_oauth_user(session: Session,
    provider: str,
    provider_id: str,
    email: str,
    display_name: str,): Find existing user by provider_id or email, or create new.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
