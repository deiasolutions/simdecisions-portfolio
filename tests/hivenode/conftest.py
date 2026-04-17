"""
conftest
========

Shared fixtures for hivenode tests.

Dependencies:
- import os
- import tempfile
- import pytest
- from pathlib import Path
- from hivenode.config import HivenodeConfig
- from hivenode.dependencies import verify_jwt, set_jwks_cache
- from hivenode.services.jwks_cache import JWKSCache
- from hivenode.main import app
- from hivenode.ledger.reader import LedgerReader
- from hivenode.ledger.writer import LedgerWriter

Functions:
- _clear_rate_limits(): Clear rate limiter state before each test.
- mock_settings(tmp_path, monkeypatch): Create fresh HivenodeConfig per test with temp paths.
- cloud_mode_settings(tmp_path, monkeypatch): Create fresh HivenodeConfig in cloud mode for node tests.
- mock_verify_jwt_fixture(monkeypatch): Override verify_jwt dependency to accept test tokens.
- mock_ledger_reader(tmp_path): Create a mock ledger reader with test database.
- mock_volume_registry(tmp_path): Create a mock volume registry with test storage.
- mock_file_transport(tmp_path): Create a mock file transport with test storage.
- mock_node_store(tmp_path): Create a mock node store with test database.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
