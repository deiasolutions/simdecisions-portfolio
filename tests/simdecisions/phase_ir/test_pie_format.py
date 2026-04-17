"""
test_pie_format
===============

Tests for PIE (PHASE-IR Egg) package format.

TASK-074: ADR-007 PHASE-IR — PIE Package Format
WB-001: PIE manifest workbench schema extension

Dependencies:
- import os
- import uuid
- from pathlib import Path
- import pytest
- import yaml
- from simdecisions.phase_ir.pie import (
- from simdecisions.phase_ir.primitives import Edge, Flow, Node

Classes:
- TestPIEManifest: PIEManifest with required fields only gets correct defaults.
- TestCreatePieScaffold: Scaffold creates the full directory tree and key files.
- TestLoadSavePie: load_pie returns a valid PIEManifest and Flow.
- TestValidatePie: A well-formed scaffold passes validation.
- TestPackUnpackPie: pack_pie creates a .pie.zip archive.
- TestIntent: write_intent then read_intent round-trips correctly.
- TestGetPieInfo: get_pie_info returns the expected summary dict.
- TestInjectWorkbench: inject_workbench copies workbench.html to PIE directory.
- TestPrepareWorkbench: prepare_workbench returns False when workbench=False in manifest.

Functions:
- _make_flow(name: str = "test-flow"): Create a minimal Flow with two nodes and one edge.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
