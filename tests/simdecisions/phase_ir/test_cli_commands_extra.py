"""
test_cli_commands_extra
=======================

Tests for PHASE-IR CLI command handlers (pack, unpack, inspect, rules, node-types, eval, formalism) — TASK-144

Tests remaining 7 cmd_* functions with happy paths, error cases, and exit codes.

Dependencies:
- from __future__ import annotations
- import argparse
- from unittest import mock
- import pytest
- from simdecisions.phase_ir.cli_commands import (
- from simdecisions.phase_ir.cli_utils import (

Functions:
- valid_flow_yaml(tmp_path): Create a valid YAML flow file.
- test_cmd_pack_pie_directory(tmp_path, capsys): pack creates a .pie.zip from a PIE directory.
- test_cmd_pack_directory_not_found(): pack returns EXIT_ERROR when directory not found.
- test_cmd_pack_to_specific_output(tmp_path): pack --output specifies output file path.
- test_cmd_unpack_archive(tmp_path): unpack extracts a .pie.zip archive.
- test_cmd_unpack_file_not_found(): unpack returns EXIT_ERROR when archive not found.
- test_cmd_inspect_shows_summary(valid_flow_yaml, capsys): inspect displays flow metadata and components.
- test_cmd_inspect_with_resources(valid_flow_yaml, capsys): inspect shows resources if present.
- test_cmd_inspect_file_not_found(): inspect exits when file not found.
- test_cmd_rules_lists_all_rules(capsys): rules lists all validation rules.
- test_cmd_node_types_lists_all_types(capsys): node-types lists all registered node types.
- test_cmd_node_types_with_category_core(capsys): node-types --category core filters by category.
- test_cmd_node_types_with_category_flow_control(capsys): node-types --category flow_control filters by category.
- test_cmd_node_types_with_category_domain(capsys): node-types --category domain filters by category.
- test_cmd_eval_simple_expression(capsys): eval evaluates a simple expression.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
