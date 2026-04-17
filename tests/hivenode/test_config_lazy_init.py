"""
test_config_lazy_init
=====================

Tests for lazy config initialization.

Dependencies:
- import sys
- import threading
- import pytest

Functions:
- test_import_config_module_no_side_effects(tmp_path, monkeypatch): Test that importing config module does NOT create directories.
- test_accessing_settings_initializes_config(tmp_path, monkeypatch): Test that accessing settings attribute DOES initialize config.
- test_second_access_uses_cached_instance(tmp_path, monkeypatch): Test that second attribute access uses cached instance (no re-init).
- test_concurrent_access_initializes_once(): Test that multiple threads accessing settings concurrently initialize once.
- test_lazy_proxy_preserves_all_attributes(tmp_path, monkeypatch): Test that lazy proxy provides access to all config attributes.
- test_lazy_proxy_get_auth_public_key_method(tmp_path, monkeypatch): Test that lazy proxy allows method calls.
- test_lazy_proxy_validates_mode(tmp_path, monkeypatch): Test that lazy proxy still validates mode on first access.
- test_lazy_proxy_cloud_mode_requires_database_url(tmp_path, monkeypatch): Test that cloud mode validation still works with lazy proxy.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
