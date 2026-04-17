"""
test_cli_commands
=================

Tests for 8os CLI commands.

Dependencies:
- import pytest
- from click.testing import CliRunner
- from unittest.mock import patch, MagicMock
- from pathlib import Path
- from hivenode.cli import main
- import httpx

Functions:
- runner(): CLI test runner.
- test_queue_status_shows_counts(runner): Test 8os queue --status shows pending/archived counts.
- test_queue_status_empty(runner): Test 8os queue --status when no tasks exist.
- test_queue_run(runner): Test 8os queue runs the queue runner.
- run_queue(): Test 8os queue handles errors.
- run_queue(): Test 8os dispatch <task_file> calls dispatch.py.
- test_dispatch_with_options(runner): Test 8os dispatch with --model, --role, --inject-boot flags.
- test_dispatch_missing_script(runner): Test 8os dispatch when dispatch.py not found.
- test_dispatch_error(runner): Test 8os dispatch handles subprocess errors.
- test_index_rebuild(runner): Test 8os index calls build_index.py.
- test_index_full_rebuild(runner): Test 8os index --full passes flag through.
- test_index_missing_script(runner): Test 8os index when build_index.py not found.
- test_index_error(runner): Test 8os index handles subprocess errors.
- test_inventory_passthrough(runner): Test 8os inventory stats passes args to inventory.py.
- test_inventory_passthrough_complex_args(runner): Test 8os inventory passes through complex arguments.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
