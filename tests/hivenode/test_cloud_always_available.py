"""
test_cloud_always_available
===========================

Tests for cloud:// always-available local storage.

Dependencies:
- import os
- import pytest
- import base64
- from pathlib import Path
- from httpx import AsyncClient, ASGITransport
- from hivenode.main import app
- from hivenode.dependencies import get_transport, get_volume_registry
- from hivenode.storage.config import get_default_config
- from hivenode.storage.transport import FileTransport
- from hivenode.storage.registry import VolumeRegistry

Functions:
- test_default_config_uses_local_filesystem_for_cloud(): Cloud volume should use local_filesystem adapter by default.
- test_default_config_cloud_root_is_shiftcenter_cloud(): Cloud volume root should be ~/.shiftcenter/cloud/.
- test_cloud_volume_instantiates_without_env_vars(): Cloud volume should instantiate without RAILWAY_STORAGE_URL.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
