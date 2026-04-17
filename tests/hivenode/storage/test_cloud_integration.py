"""
test_cloud_integration
======================

Integration tests for CloudAdapter + VolumeRegistry + SyncQueue.

Dependencies:
- import base64
- import json
- import os
- import pytest
- import respx
- import httpx

Functions:
- tmp_queue_dir(tmp_path): Create a temporary queue directory.
- yaml_config(tmp_path): Create a test YAML config file.
- test_registry_creates_cloud_adapter_from_config(yaml_config): Registry creates CloudAdapter from config with correct params.
- test_registry_instantiates_adapter_once(yaml_config): Registry caches adapter instances.
- test_registry_expands_queue_dir_path(tmp_path, yaml_config): Registry expands queue_dir path with tilde and env vars.
- test_cloud_adapter_read_returns_bytes(tmp_queue_dir): CloudAdapter.read() returns bytes (not coroutine) when server responds 200.
- test_cloud_adapter_write_sends_put_request(tmp_queue_dir): CloudAdapter.write() sends PUT request with correct body.
- test_cloud_adapter_raises_volume_offline_error_on_network_failure(tmp_queue_dir): CloudAdapter raises VolumeOfflineError when server unreachable.
- test_sync_queue_captures_writes_during_offline(tmp_queue_dir): SyncQueue captures writes during offline.
- test_cloud_adapter_list_returns_file_list(tmp_queue_dir): CloudAdapter.list() returns file list from server response.
- test_cloud_adapter_stat_returns_file_metadata(tmp_queue_dir): CloudAdapter.stat() returns file metadata.
- test_registry_volume_config_with_env_vars(tmp_path): Registry respects env var overrides for cloud config.
- test_registry_resolves_volume_adapter_and_config(yaml_config): Registry.resolve() returns correct adapter type and expanded config.
- test_registry_raises_on_unknown_volume(): Registry raises KeyError for unknown volume.
- test_cloud_adapter_handles_permission_errors(tmp_queue_dir): CloudAdapter handles 403 permission errors.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
