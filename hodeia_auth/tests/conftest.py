"""
conftest
========

Pytest fixtures for hodeia_auth tests.

Dependencies:
- import os
- import tempfile
- import pytest
- from sqlalchemy import create_engine
- from sqlalchemy.orm import sessionmaker
- from fastapi.testclient import TestClient
- from sqlalchemy import text
- from hodeia_auth.db import Base, get_session
- from hodeia_auth.main import app
- from hodeia_auth.config import settings

Functions:
- test_db(): Create a temporary SQLite database for testing.
- db_session(test_db): Provide a database session for tests.
- client(test_db): Provide a TestClient with test database.
- mock_jwt_keys(monkeypatch, tmp_path): Generate mock RSA keys for JWT testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
