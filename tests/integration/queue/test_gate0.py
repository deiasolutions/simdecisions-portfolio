"""
test_gate0
==========

Tests for Gate 0 validation — spec quality checks before dispatch.

Gate 0 validates:
1. Deliverables vs acceptance criteria coherence
2. File paths exist
3. Scope sanity (can modify files referenced in bug descriptions)
4. Priority is present
5. Acceptance criteria present

Dependencies:
- import pytest
- from pathlib import Path
- import sys
- from gate0 import (
- from spec_parser import SpecFile

Functions:
- repo_root(tmp_path): Create a temporary repo with some test files.
- valid_spec(tmp_path): Create a valid spec for testing.
- test_check_priority_present_pass(tmp_path): Priority check passes when priority is present.
- test_check_priority_present_fail(tmp_path): Priority check fails when priority is missing.
- test_check_acceptance_criteria_present_pass(): Acceptance criteria check passes when criteria exist.
- test_check_acceptance_criteria_present_fail(): Acceptance criteria check fails when no criteria exist.
- test_check_file_paths_exist_pass(valid_spec, repo_root): File paths check passes when all referenced files exist.
- test_check_file_paths_exist_fail(tmp_path): File paths check fails when referenced files don't exist.
- test_check_deliverables_coherence_pass(tmp_path): Coherence check passes when deliverables and acceptance align.
- test_check_deliverables_coherence_fail(tmp_path): Coherence check fails when deliverables contradict acceptance.
- test_check_scope_sanity_pass(tmp_path): Scope sanity check passes when spec allows modification of buggy files.
- test_check_scope_sanity_fail(tmp_path): Scope sanity check fails when spec forbids modification of buggy file.
- test_validate_spec_all_pass(valid_spec, repo_root): Full validation passes for a well-formed spec.
- test_validate_spec_missing_priority(tmp_path): Full validation fails when priority is missing.
- test_validate_spec_missing_acceptance_criteria(tmp_path): Full validation fails when acceptance criteria are missing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
