"""
conftest
========

Pytest fixtures for gate_enforcer tests.

Dependencies:
- import tempfile
- import pytest
- from pathlib import Path
- import yaml

Functions:
- temp_dir(): Create a temporary directory for tests.
- temp_deia_root(temp_dir): Create a .deia directory structure for tests.
- temp_ledger_db(temp_dir): Create a temporary ledger database for tests.
- sample_ethics_dict(): Sample ethics configuration as dict.
- sample_grace_config_dict(): Sample grace configuration as dict.
- write_ethics_file(temp_deia_root): Helper to write an ethics.yml file for an agent.
- write_grace_config(temp_deia_root): Helper to write grace.yml config.
- write_default_ethics(temp_deia_root): Helper to write ethics-default.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
