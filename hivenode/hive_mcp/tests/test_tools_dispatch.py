"""
test_tools_dispatch
===================

Tests for dispatch tools.

Dependencies:
- import pytest
- from unittest.mock import MagicMock, patch
- from hivenode.hive_mcp.tools import dispatch

Functions:
- repo_root(tmp_path): Create temporary repo structure.
- dispatch_script(repo_root): Create mock dispatch.py script.
- test_dispatch_bee_validates_task_file(repo_root, dispatch_script): dispatch_bee validates task file exists.
- test_dispatch_bee_validates_role(repo_root, dispatch_script): dispatch_bee validates role parameter.
- test_dispatch_bee_runs_subprocess(repo_root, dispatch_script): dispatch_bee spawns subprocess and returns PID.
- test_dispatch_bee_passes_all_args(repo_root, dispatch_script): dispatch_bee passes all args to dispatch.py.
- test_dispatch_bee_background_mode(repo_root, dispatch_script): dispatch_bee runs in background by default.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
