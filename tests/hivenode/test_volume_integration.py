"""
test_volume_integration
=======================

E2E integration tests for volume storage feature.

Tests the complete flow: create volume → write files → list files → read files.
This test suite uses real backend with test volume (not mocked).

Dependencies:
- import pytest
- import base64
- from pathlib import Path
- from httpx import AsyncClient, ASGITransport
- from hivenode.main import app
- from hivenode.dependencies import get_transport, get_volume_registry
- from hivenode.storage.transport import FileTransport
- from hivenode.storage.registry import VolumeRegistry
- from hivenode.storage.adapters.local import LocalFilesystemAdapter
- from tests.hivenode.test_auth_routes import create_test_token

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
