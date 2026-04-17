"""
test_cli_commands
=================

Tests for PHASE-IR CLI command handlers — TASK-144

Tests all 13 cmd_* functions with happy paths, error cases, file I/O, and exit codes.
Covers: init, validate, lint, export, compile, decompile, pack, unpack, inspect,
        rules, node-types, eval, formalism.

Dependencies:
- from __future__ import annotations
- import argparse
- from unittest import mock
- import pytest
- from simdecisions.phase_ir.cli_commands import (
- from simdecisions.phase_ir.cli_utils import (

Functions:
- valid_flow_yaml(tmp_path): Create a valid YAML flow file.
- valid_flow_json(tmp_path): Create a valid JSON flow file.
- invalid_flow_yaml(tmp_path): Create an invalid YAML flow (missing required nodes).
- sample_bpmn_xml(tmp_path): Create a sample BPMN XML file.
- test_cmd_init_creates_scaffold(tmp_path): init creates a PIE scaffold directory.
- test_cmd_init_with_metadata(tmp_path, capsys): init accepts --intent and --author.
- test_cmd_init_default_output_cwd(capsys): init defaults to current directory when no --output.
- test_cmd_validate_valid_flow(valid_flow_yaml, capsys): validate reports 'Valid' for a good flow.
- test_cmd_validate_invalid_flow(invalid_flow_yaml, capsys): validate returns EXIT_VALIDATION_FAIL for an invalid flow.
- test_cmd_validate_with_level_syntax(valid_flow_yaml): validate accepts --level syntax.
- test_cmd_validate_with_level_governance(valid_flow_yaml): validate accepts --level governance.
- test_cmd_validate_with_mode_production(valid_flow_yaml): validate accepts --mode production.
- test_cmd_validate_file_not_found(): validate exits when file not found.
- test_cmd_lint_uses_governance_level(valid_flow_yaml): lint is an alias for validate --level=governance.
- test_cmd_lint_sets_default_mode(valid_flow_yaml): lint sets mode to 'sim' if not provided.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
