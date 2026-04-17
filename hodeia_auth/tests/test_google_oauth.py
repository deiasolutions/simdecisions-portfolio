"""
test_google_oauth
=================

Tests for Google OAuth + generic provider refactor.

Dependencies:
- import base64
- import json
- from unittest.mock import AsyncMock, patch
- import pytest
- from hodeia_auth.models import User
- from hodeia_auth.config import settings

Functions:
- test_google_login_returns_url(client, mock_jwt_keys, monkeypatch): Google login endpoint returns authorization URL.
- test_google_login_501_when_not_configured(client, mock_jwt_keys): Google login returns 501 when client ID not set.
- mock_google_apis(): Mock Google token exchange and profile API.
- _make_state(origin: str): Build a valid state param.
- test_google_callback_creates_user(client, mock_jwt_keys, mock_google_apis, db_session, monkeypatch): Google callback creates new user with provider='google' and provider_id.
- test_google_callback_auto_merges_on_email(client, mock_jwt_keys, mock_google_apis, db_session, monkeypatch): Google login auto-merges with existing user that has same email.
- test_google_callback_error_param(client, mock_jwt_keys, monkeypatch): Google callback redirects with error when Google returns error.
- test_google_callback_invalid_state(client, mock_jwt_keys, monkeypatch): Google callback returns 400 on invalid state.
- mock_github_apis(): Mock GitHub token exchange and profile API.
- test_github_callback_sets_provider_id(client, mock_jwt_keys, mock_github_apis, db_session, monkeypatch): GitHub callback sets both github_id and provider_id.
- test_github_legacy_user_gets_backfilled(client, mock_jwt_keys, mock_github_apis, db_session, monkeypatch): Existing user with github_id but no provider_id gets backfilled on login.
- test_google_jwt_has_correct_provider(client, mock_jwt_keys, mock_google_apis, monkeypatch): JWT from Google login has provider='google' and correct provider_id.
- test_origin_roundtrips_through_google(client, mock_jwt_keys, mock_google_apis, monkeypatch): Origin param survives through state encoding and redirect.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
