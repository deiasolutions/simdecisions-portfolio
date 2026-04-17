"""
test_identity
=============

Tests for hivenode.identity module.

Dependencies:
- import pytest
- import yaml
- from pathlib import Path
- from unittest.mock import patch

Functions:
- mock_home(tmp_path, monkeypatch): Mock home directory to isolate tests.
- clear_cache(): Clear module-level caches before each test.
- test_get_node_id_generates_on_first_call(mock_home): Test that get_node_id() generates a new node ID on first call.
- test_get_node_id_uses_uuid_format(mock_home): Test that get_node_id() uses uuid.uuid4().hex[:12] format.
- test_get_node_id_persists_to_config(mock_home): Test that get_node_id() persists to ~/.shiftcenter/config.yml.
- test_get_node_id_returns_same_id_on_repeated_calls(mock_home): Test that get_node_id() returns the same ID on repeated calls.
- test_get_node_id_reads_existing_config(mock_home): Test that get_node_id() reads existing node_id from config.yml.
- test_get_node_id_caches_result(mock_home): Test that get_node_id() caches result in memory.
- test_get_device_id_generates_on_first_call(mock_home): Test that get_device_id() generates a new device ID on first call.
- test_get_device_id_uses_uuid_format(mock_home): Test that get_device_id() uses uuid.uuid4().hex[:16] format.
- test_get_device_id_persists_to_config(mock_home): Test that get_device_id() persists to ~/.shiftcenter/config.yml.
- test_get_device_id_returns_same_id_on_repeated_calls(mock_home): Test that get_device_id() returns the same ID on repeated calls.
- test_get_db_path_returns_absolute_path(mock_home): Test that get_db_path() returns an absolute path.
- test_get_db_path_resolves_to_shiftcenter(mock_home): Test that get_db_path() resolves to ~/.shiftcenter/.
- test_get_db_path_creates_parent_directory(mock_home): Test that get_db_path() creates parent directory if it doesn't exist.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
