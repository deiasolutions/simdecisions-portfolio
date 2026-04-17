"""
test_estimates_calibration
==========================

Tests for estimation calibration engine and CLI commands.

Dependencies:
- import sys
- from datetime import datetime, timezone
- from pathlib import Path
- import pytest
- from sqlalchemy import select
- from hivenode.inventory import store

Functions:
- db_engine(): Create in-memory SQLite engine for tests.
- sample_estimates(db_engine): Insert sample estimates for testing.
- test_update_calibration_computes_mean_ratio(sample_estimates): Test that update_calibration computes mean(actual/estimate) for each dimension.
- test_update_calibration_handles_zero_est(db_engine): Test that update_calibration skips tasks with est_hours=0 (division by zero).
- test_apply_calibration_returns_calibrated_values(sample_estimates): Test that apply_calibration multiplies estimates by factors.
- test_apply_calibration_returns_original_if_no_data(db_engine): Test that apply_calibration returns original estimates if no calibration data exists.
- test_calibration_updates_after_import_actuals(sample_estimates): Test that calibration factors update automatically after import_actuals.
- test_cli_calibration_shows_factors(sample_estimates, capsys): Test that 'estimates.py calibration' shows calibration factors table.
- test_cli_compare_shows_per_task(sample_estimates, capsys): Test that 'estimates.py compare' shows per-task comparison table.
- test_cli_budget_shows_remaining(sample_estimates, capsys): Test that 'estimates.py budget --remaining' shows remaining work projection.
- test_cli_trend_groups_by_week(sample_estimates, capsys): Test that 'estimates.py trend' groups tasks by week and shows accuracy trend.
- test_filters_work_on_compare(sample_estimates, capsys): Test that --type filter works on compare command.
- test_budget_handles_no_remaining(db_engine, capsys): Test that budget command handles case when all tasks are complete.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
