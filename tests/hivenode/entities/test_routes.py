"""
test_routes
===========

Tests for bot embedding routes.

Dependencies:
- import pytest
- from unittest.mock import Mock, patch, MagicMock
- from fastapi import HTTPException
- from fastapi.testclient import TestClient

Classes:
- TestRegisterEndpoint: Tests for POST /api/bots/{entity_id}/register.
- TestPiEndpoint: Tests for GET /api/bots/{entity_id}/pi/{domain}.
- TestCheckDriftEndpoint: Tests for POST /api/bots/{entity_id}/check-drift.
- TestAuthFailure: Tests for auth failures in cloud mode.

Functions:
- mock_db(): Mock SQLAlchemy DB session.
- mock_auth(): Mock verify_jwt_or_local to bypass auth.
- mock_get_db(): Mock get_db dependency.
- client(mock_auth, mock_get_db): FastAPI test client.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
