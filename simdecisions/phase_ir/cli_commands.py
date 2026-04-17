"""
cli_commands
============

PHASE-IR CLI command handlers — TASK-143 PORT

All 13 subcommand handler functions (cmd_*).
Imports from engine.phase_ir modules and file I/O helpers from .cli_utils

Dependencies:
- from __future__ import annotations
- import argparse
- import json
- import os
- import sys
- from collections import Counter
- from simdecisions.phase_ir.bpmn_compiler import compile_bpmn, decompile_to_bpmn
- from simdecisions.phase_ir.cli_utils import (
- from simdecisions.phase_ir.expressions import evaluate, parse_expression, validate_expression
- from simdecisions.phase_ir.formalism import explain_mapping, get_all_mappings

Functions:
- cmd_init(args: argparse.Namespace): Create a new PIE scaffold directory.
- cmd_validate(args: argparse.Namespace): Validate a flow file and print issues.
- cmd_lint(args: argparse.Namespace): Alias for validate with governance level.
- cmd_export(args: argparse.Namespace): Export a flow to a different format.
- cmd_compile(args: argparse.Namespace): Compile BPMN XML to PHASE-IR JSON.
- cmd_decompile(args: argparse.Namespace): Decompile PHASE-IR flow to BPMN XML.
- cmd_pack(args: argparse.Namespace): Pack a PIE directory into a .pie.zip archive.
- cmd_unpack(args: argparse.Namespace): Unpack a .pie.zip archive into a directory.
- cmd_inspect(args: argparse.Namespace): Show flow summary (nodes, edges, groups, resources).
- cmd_rules(args: argparse.Namespace): List all validation rules.
- cmd_node_types(args: argparse.Namespace): List all registered node types.
- cmd_eval(args: argparse.Namespace): Evaluate a PHASE-IR expression.
- cmd_formalism(args: argparse.Namespace): Show formalism mapping for a flow or a target formalism.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
