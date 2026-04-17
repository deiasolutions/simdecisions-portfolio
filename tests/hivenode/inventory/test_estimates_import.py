"""
test_estimates_import
=====================

Tests for estimates.py CLI — data collection for estimation calibration ledger.

Dependencies:
- from unittest.mock import MagicMock, patch
- import pytest
- from hivenode.inventory import store
- from dataclasses import dataclass
- from typing import Optional

Classes:
- Task: Create sample response files for testing.

Functions:
- temp_db(): Create a temporary SQLite database for testing.
- sample_scheduler_file(tmp_path): Create a sample scheduler file for testing.
- sample_response_files(tmp_path): Create sample response files for testing.
- test_import_scheduler_parses_tasks(temp_db, sample_scheduler_file): Test that import-scheduler parses all tasks from scheduler file.
- test_import_scheduler_derives_model(temp_db, sample_scheduler_file): Test that model is derived correctly from task_type.
- test_import_scheduler_computes_cost(temp_db, sample_scheduler_file): Test that cost is computed correctly using rate_loader.
- test_import_scheduler_computes_carbon(temp_db, sample_scheduler_file): Test that carbon is computed correctly using carbon.yml.
- test_import_actuals_fetches_build_status(temp_db): Test that import-actuals fetches from build monitor and updates actuals.
- test_import_actuals_computes_cost_from_tokens(temp_db): Test that cost is computed correctly from tokens in build monitor data.
- test_import_actuals_computes_hours(temp_db): Test that hours are computed correctly from timestamps.
- test_import_responses_parses_clock_cost_carbon(temp_db, sample_response_files): Test that response files are parsed correctly.
- test_import_responses_extracts_task_id(sample_response_files): Test that task IDs are extracted from filenames correctly.
- test_import_responses_handles_incomplete_sections(temp_db, sample_response_files): Test that incomplete Clock/Cost/Carbon sections are handled gracefully.
- test_record_inserts_new_estimate(temp_db): Test that record command inserts a new estimate.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
