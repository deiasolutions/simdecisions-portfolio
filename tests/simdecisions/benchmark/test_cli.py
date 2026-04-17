"""
test_cli
========

Tests for benchmark CLI.

TASK-BENCH-002 - Test benchmark.py CLI: estimate, run, list subcommands.

Dependencies:
- import pytest
- import sys
- from pathlib import Path
- from unittest.mock import patch, Mock
- from argparse import Namespace
- import yaml
- from _tools.benchmark import cmd_estimate, cmd_run, cmd_list

Functions:
- temp_benchmark_manifest(tmp_path): Create a temporary benchmark manifest for CLI tests.
- test_cli_estimate_displays_budget(temp_benchmark_manifest, capsys): Test 'estimate' command displays budget correctly.
- test_cli_estimate_with_sample(temp_benchmark_manifest): Test 'estimate' command with sample size.
- test_cli_list_displays_benchmarks(temp_benchmark_manifest, capsys): Test 'list' command displays registered benchmarks.
- test_cli_list_shows_only_enabled(temp_benchmark_manifest, capsys): Test 'list' command shows only enabled benchmarks by default.
- test_cli_run_dry_run_no_files_written(temp_benchmark_manifest, tmp_path, capsys): Test 'run --dry-run' does not write files.
- test_cli_run_auto_approves_below_threshold(temp_benchmark_manifest, tmp_path, capsys): Test 'run' command auto-approves when budget < $5.00.
- test_cli_run_unknown_benchmark_exits_with_error(temp_benchmark_manifest, tmp_path, capsys): Test CLI exits with error if benchmark not found in manifest.
- test_cli_run_with_models_option(temp_benchmark_manifest, tmp_path): Test 'run --models MODEL1,MODEL2'.
- test_cli_list_with_all_flag(temp_benchmark_manifest, capsys): Test 'list --all' shows disabled benchmarks.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
