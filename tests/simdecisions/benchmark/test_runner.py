"""
test_runner
===========

Tests for BenchmarkRunner.

TASK-BENCH-002 - Test BenchmarkRunner: manifest loading, adapter retrieval,
budget estimation, and task file generation.

Dependencies:
- import pytest
- import yaml
- from pathlib import Path
- from unittest.mock import Mock, patch
- from simdecisions.benchmark.runner import BenchmarkRunner
- from simdecisions.benchmark.types import BenchmarkTask
- from simdecisions.benchmark.adapter import BenchmarkAdapter

Classes:
- MockAdapter: Mock adapter for testing.

Functions:
- temp_manifest(tmp_path): Create a temporary benchmarks.yml manifest.
- temp_output_dir(tmp_path): Create a temporary output directory.
- test_runner_loads_manifest(temp_manifest): Test BenchmarkRunner loads manifest correctly.
- test_runner_get_adapter(temp_manifest): Test get_adapter returns correct adapter class.
- test_runner_get_adapter_not_found(temp_manifest): Test get_adapter raises error for unknown benchmark.
- test_estimate_budget_calculates_work_items(temp_manifest): Test estimate_budget calculates work items correctly.
- test_estimate_budget_with_sample_size(temp_manifest): Test estimate_budget respects sample_size.
- test_generate_tasks_creates_correct_count(temp_manifest, temp_output_dir): Test generate_tasks creates correct number of SPEC files.
- test_generate_tasks_with_multiple_models(temp_manifest, temp_output_dir): Test generate_tasks with multiple models.
- test_generate_task_file_writes_valid_spec(temp_manifest, temp_output_dir): Test _generate_task_file writes valid SPEC format.
- test_generate_task_file_includes_acceptance_criteria(temp_manifest, temp_output_dir): Test SPEC file includes acceptance criteria.
- test_generate_task_file_baseline_vs_simdecisions(temp_manifest, temp_output_dir): Test SPEC file differs for baseline vs simdecisions track.
- test_runner_manifest_path_stored(temp_manifest): Test BenchmarkRunner stores manifest path.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
