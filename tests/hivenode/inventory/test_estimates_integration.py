"""
test_estimates_integration
==========================

Integration tests for estimation calibration system.

Full end-to-end workflows covering import, calibration, and reporting.

Dependencies:
- import os
- import sys
- import tempfile
- from datetime import datetime, timezone, timedelta
- from pathlib import Path
- from unittest.mock import Mock, patch
- import pytest
- from hivenode.inventory import store
- from _tools.estimates_db import (
- from dataclasses import dataclass

Classes:
- Task: Create mock response files for testing.

Functions:
- test_db(): Create a temporary test database.
- mock_scheduler_file(): Create a mock scheduler file for testing.
- mock_response_files(): Create mock response files for testing.
- test_full_estimation_workflow(test_db, mock_scheduler_file): Full estimation lifecycle:
- test_response_file_vs_build_monitor(test_db, mock_scheduler_file, mock_response_files): Compare actuals from two sources:
- test_manual_task_calibration(test_db): Record 10 tasks manually, compute calibration:
- test_trend_groups_by_week(test_db): Create tasks completed over 3 weeks, verify trend report:
- test_filters_on_reports(test_db): Create 20 tasks (10 spec haiku, 10 build sonnet), verify filters work.
- test_edge_case_no_data(test_db, capsys): Handle corner cases gracefully:
- test_edge_case_all_complete(test_db, capsys): All tasks complete (budget shows 0, not error).
- test_edge_case_zero_estimates(test_db): Handle est_hours=0 (skip in calibration, don't divide by zero).
- test_help_text_exists(): Verify --help works for all 9 commands.
- test_smoke_all_commands(test_db, mock_scheduler_file, mock_response_files, capsys): Run all commands with test data, verify no crashes.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
