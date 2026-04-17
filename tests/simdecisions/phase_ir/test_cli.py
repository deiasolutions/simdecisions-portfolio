"""
test_cli
========

Tests for PHASE-IR CLI — TASK-144

Tests the main CLI entry point, argument parsing, and utility functions.
Covers parser construction, main() dispatch, file I/O helpers, and color output.

Dependencies:
- from __future__ import annotations
- import argparse
- import io
- import sys
- from unittest import mock
- import pytest
- from simdecisions.phase_ir.cli import _build_parser, main
- from simdecisions.phase_ir.cli_utils import (
- from simdecisions.phase_ir.primitives import Flow

Functions:
- test_build_parser_creates_parser(): Parser is created with correct prog name.
- test_build_parser_has_all_subcommands(): Parser includes all 13 subcommands.
- test_build_parser_init_args(): init subcommand accepts name and optional flags.
- test_build_parser_validate_args(): validate subcommand accepts file and level/mode options.
- test_build_parser_export_args(): export subcommand requires --format.
- test_build_parser_formalism_requires_target(): formalism subcommand requires --target.
- test_main_no_command(capsys): No command given prints help and returns EXIT_ERROR.
- test_main_unknown_command(): Unknown command raises SystemExit (argparse behavior).
- test_main_dispatches_to_handler(): Valid command dispatches to correct handler.
- test_main_rules_command(capsys): 'rules' command lists validation rules.
- test_main_node_types_command(capsys): 'node-types' command lists node types.
- test_main_node_types_with_category(capsys): 'node-types --category core' filters by category.
- test_load_flow_from_file_json(tmp_path): Load a JSON flow file.
- test_load_flow_from_file_yaml(tmp_path): Load a YAML flow file.
- test_load_flow_from_file_not_found(): File not found raises SystemExit.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
