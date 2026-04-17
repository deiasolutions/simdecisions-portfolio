"""
test_config
===========

Tests for storage config module.

Dependencies:
- import os
- import pytest
- import yaml

Functions:
- test_load_config_from_yaml(temp_volumes_yaml): Test loading volume config from YAML file.
- test_load_config_missing_file(): Test loading config from non-existent file raises error.
- test_expand_env_vars(temp_volumes_with_env_yaml): Test environment variable expansion in config.
- test_expand_env_vars_missing_var(temp_dir): Test handling of missing environment variables.
- test_expand_tilde_home_directory(temp_dir): Test tilde expansion for home directory.
- test_expand_path_with_env_var(): Test path expansion with environment variable.
- test_expand_path_absolute(): Test absolute path remains unchanged.
- test_get_default_config(): Test getting default volume configuration.
- test_malformed_yaml(temp_dir): Test handling of malformed YAML.
- test_empty_yaml_file(temp_dir): Test handling of empty YAML file.
- test_validate_url_valid(): Test URL validation with valid URLs.
- test_validate_url_invalid(): Test URL validation with invalid URLs.
- test_get_cloud_config_from_env(): Test loading cloud config from environment variables.
- test_get_cloud_config_fallback_queue_dir(): Test default queue_dir when not in environment.
- test_get_cloud_config_custom_queue_dir(): Test custom queue_dir from environment variable.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
