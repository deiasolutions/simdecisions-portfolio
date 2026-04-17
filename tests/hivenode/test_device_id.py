"""
test_device_id
==============

Tests for device_id generation and persistence.

Dependencies:
- import re
- import pytest
- import yaml
- from pathlib import Path
- from httpx import AsyncClient, ASGITransport
- from hivenode.config import HivenodeConfig
- from hivenode.main import app
- from tests.hivenode.conftest import TEST_PUBLIC_KEY

Functions:
- test_device_id_generated_on_first_run(tmp_path, monkeypatch): Device ID should be generated when config.yml doesn't have one.
- test_device_id_format_matches_spec(tmp_path, monkeypatch): Device ID should match device-{16 hex chars} format.
- test_device_id_persists_across_instances(tmp_path, monkeypatch): Device ID should be the same across config instances.
- test_device_id_saved_to_config_yml(tmp_path, monkeypatch): Device ID should be persisted in ~/.shiftcenter/config.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
