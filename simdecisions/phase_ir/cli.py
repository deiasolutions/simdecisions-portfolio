"""
cli
===

PHASE-IR Command-Line Interface — TASK-143 PORT

Thin CLI layer over the PHASE-IR library modules. Entry point for
``python -m engine.phase_ir`` and direct invocation.

Commands:
    phase init <name>
    phase validate <file>
    phase lint <file>
    phase export <file> --format mermaid|bpmn|json|yaml
    phase compile <bpmn_file>
    phase decompile <file>
    phase pack <dir>
    phase unpack <file> <dir>
    phase inspect <file>
    phase rules
    phase node-types
    phase eval <expression>
    phase formalism <file> --target petri|bpmn|csp|des

Dependencies:
- from __future__ import annotations
- import argparse
- import sys
- from simdecisions.phase_ir.cli_utils import EXIT_ERROR
- from simdecisions.phase_ir.cli_commands import (

Functions:
- _build_parser(): Construct the CLI argument parser with all subcommands.
- main(argv: list[str] | None = None): Parse arguments and dispatch to the appropriate subcommand.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
