"""
conftest
========

Pytest fixtures for storage tests.

Dependencies:
- import tempfile
- import pytest
- from pathlib import Path
- import yaml
- import os

Functions:
- temp_dir(): Create a temporary directory for tests.
- temp_ledger_db(temp_dir): Create a temporary ledger database for tests.
- temp_provenance_db(temp_dir): Create a temporary provenance database for tests.
- temp_volumes_yaml(temp_dir): Create a temporary YAML config file with test volumes.
- temp_volumes_with_env_yaml(temp_dir): Create a temporary YAML config with env var expansion.
- local_adapter_root(temp_dir): Create a root directory for local filesystem adapter tests.
- mock_ledger_writer(temp_ledger_db): Create a mock ledger writer for transport tests.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
