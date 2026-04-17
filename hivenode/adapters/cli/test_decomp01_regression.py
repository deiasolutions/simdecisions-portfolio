"""
test_decomp01_regression
========================

Regression test for SPEC-fix-DECOMP-01: False completion detection.

This test verifies that the specific output from the Q88NR bee in DECOMP-01
is correctly detected as a blocker (not success).

Dependencies:
- import pytest
- from pathlib import Path
- from hivenode.adapters.cli.claude_cli_subprocess import ClaudeCodeProcess

Functions:
- test_decomp01_q88nr_blocker_detected(): Test that Q88NR's DECOMP-01 blocker output is detected as failure.
- test_decomp01_explicit_waiting(): Test that 'waiting for explicit direction' is detected as blocker.
- test_decomp01_requires_decision(): Test that 'requires your decision' is detected as blocker.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
