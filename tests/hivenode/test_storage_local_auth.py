"""
test_storage_local_auth
=======================

Tests for local mode auth bypass on storage routes.

Dependencies:
- import pytest
- from unittest.mock import patch, MagicMock
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from hivenode import dependencies

Classes:
- TestLocalModeAuthBypass: Storage routes should work without JWT in local mode.
- TestCloudModeRequiresAuth: Storage routes should require JWT in cloud mode (no regression).

Functions:
- _make_mock_transport(): Create a mock transport with dict-backed storage for round-trip tests.
- local_mode_client(tmp_path): TestClient configured for local mode with mock storage.
- cloud_mode_client(tmp_path): TestClient configured for cloud mode — JWT required.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
