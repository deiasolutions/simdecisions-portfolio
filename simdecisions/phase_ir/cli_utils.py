"""
cli_utils
=========

PHASE-IR CLI utilities — shared constants and helpers.

Avoids circular imports between cli.py and cli_commands.py.

Dependencies:
- from __future__ import annotations
- import os
- import sys
- from simdecisions.phase_ir.primitives import Flow
- from simdecisions.phase_ir.schema import json_to_flow, yaml_to_flow

Functions:
- _supports_color(): Return True if stdout is a TTY that likely supports ANSI colours.
- _color(text: str, code: str): Wrap *text* in an ANSI colour escape if the terminal supports it.
- _green(text: str): Read a flow from a JSON or YAML file and return a Flow dataclass.
- _read_text(path: str): Read a text file, exiting on error.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
