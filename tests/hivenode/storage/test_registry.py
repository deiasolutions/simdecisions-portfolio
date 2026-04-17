"""
test_registry
=============

Tests for volume registry.

Dependencies:
- import pytest

Functions:
- test_load_volumes_from_yaml(temp_volumes_yaml): Test loading volume declarations from YAML.
- test_declare_custom_volume(temp_volumes_yaml): Test declaring a custom volume at runtime.
- test_reject_short_custom_volume_name(temp_volumes_yaml): Test rejection of custom volume names <=7 characters.
- test_reject_redeclare_system_volume(temp_volumes_yaml): Test rejection of attempts to redeclare system volumes.
- test_resolve_volume_to_adapter(temp_volumes_yaml, temp_dir): Test resolving volume name to adapter and config.
- test_resolve_missing_volume(temp_volumes_yaml): Test resolving non-existent volume raises error.
- test_volume_status_available(temp_volumes_yaml, temp_dir): Test checking status of available volume.
- test_list_volumes(temp_volumes_yaml): Test listing all registered volumes.
- test_system_volume_names_are_short(): Test that all system volume names are <=7 characters.
- test_custom_volume_with_8_chars_accepted(temp_volumes_yaml): Test that custom volume with exactly 8 characters is accepted.
- test_cloud_adapter_initialization(temp_dir): Test initializing cloud adapter via registry.
- test_cloud_adapter_missing_cloud_url(temp_dir): Test cloud adapter initialization fails without cloud_url.
- test_cloud_adapter_missing_auth_token(temp_dir): Test cloud adapter initialization fails without auth_token.
- test_cloud_adapter_queue_dir_expansion(temp_dir): Test that queue_dir is expanded with tilde.
- test_cloud_adapter_env_var_fallback(temp_dir, monkeypatch): Test cloud adapter falls back to env vars when config missing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
