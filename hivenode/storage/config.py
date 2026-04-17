"""
config
======

Volume configuration loading and path expansion.

Dependencies:
- import os
- import re
- from typing import Any, Dict
- from urllib.parse import urlparse
- import yaml

Functions:
- load_config(yaml_path: str): Load volume configuration from YAML file.
- _expand_env_vars_recursive(obj: Any): Recursively expand environment variables in config structure.
- _expand_env_var(value: str): Expand ${VAR} environment variables in string.
- expand_path(path: str): Expand path with environment variables and tilde.
- validate_url(url: str): Validate that a string is a valid URL.
- get_cloud_config(): Get cloud volume configuration from environment variables.
- get_default_config(): Get default volume configuration.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
