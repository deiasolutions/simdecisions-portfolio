"""
test_swebench_eval
==================

Integration tests for _tools/swebench_eval.py

SPEC-SWE-002 - Tests for SWE-bench evaluation harness CLI.

Dependencies:
- import json
- import pytest
- import sys
- from pathlib import Path
- from unittest.mock import MagicMock, patch, mock_open
- from _tools import swebench_eval

Functions:
- temp_benchmark_dir(tmp_path): Create temporary benchmark directory structure.
- sample_tasks(): Sample tasks for testing.
- mock_patches(temp_benchmark_dir): Create mock patch files.
- test_collect_finds_diff_files(temp_benchmark_dir, sample_tasks, mock_patches): Test that collect subcommand finds .diff files in patches directory.
- test_collect_produces_valid_predictions_json(temp_benchmark_dir, sample_tasks, mock_patches): Test that predictions JSON has correct swebench format.
- test_collect_reports_correct_counts(temp_benchmark_dir, sample_tasks, mock_patches, capsys): Test that collect reports patches found vs total tasks.
- test_collect_handles_missing_patches(temp_benchmark_dir, sample_tasks): Test that collect handles tasks with no corresponding patch file.
- test_predictions_json_schema(temp_benchmark_dir, sample_tasks, mock_patches): Test predictions JSON matches swebench schema exactly.
- test_report_parses_result_jsons(temp_benchmark_dir): Test that report subcommand parses evaluation result JSONs.
- test_report_computes_resolved_percentage(temp_benchmark_dir): Test that report correctly computes resolved percentage.
- test_report_produces_markdown_table(temp_benchmark_dir): Test that report generates markdown with tables.
- test_status_reports_correct_counts(temp_benchmark_dir, sample_tasks, mock_patches, capsys): Test that status subcommand reports correct progress.
- test_evaluate_builds_correct_subprocess_command(temp_benchmark_dir): Test that evaluate constructs the correct swebench subprocess command.
- test_evaluate_prepends_wsl_on_windows(temp_benchmark_dir): Test that evaluate adds 'wsl' prefix on Windows platform.
- test_collect_skips_patches_not_in_sample(temp_benchmark_dir, sample_tasks): Test that collect only includes patches for tasks in sample.json.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
