"""
test_sync_autostart
===================

Tests for sync auto-start configuration (TASK-SYNC-AUTOSTART-A).

Dependencies:
- import tempfile

Functions:
- test_no_config_file_sync_defaults_to_true(): Test that sync_enabled defaults to True when config file missing.
- test_config_file_enables_sync_explicitly(): Test that config file can explicitly enable sync.
- test_config_file_disables_sync_explicitly(): Test that config file can explicitly disable sync.
- test_config_file_missing_sync_section_defaults_to_enabled(): Test that config file without sync section defaults to enabled.
- test_default_interval_seconds_60(): Test that default interval is 60 seconds when not specified.
- test_default_interval_seconds_from_config(): Test that interval can be overridden in config file.
- test_on_write_false_by_default(): Test that on_write defaults to False.
- test_on_write_can_be_enabled(): Test that on_write can be enabled in config.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
