"""
test_spec_submit_endpoint
=========================

Integration test for /factory/spec-submit endpoint.

Tests that the spec-submit endpoint:
1. Accepts valid spec submissions
2. Validates acceptance_criteria is provided
3. Validates the generated spec passes Gate 0
4. Writes spec to backlog directory
5. Returns correct response structure

Dependencies:
- import json
- import pytest
- from pathlib import Path
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- cleanup_test_specs(): Remove any test specs created during testing.
- cleanup(): Clean up before and after each test.
- test_spec_submit_valid_submission(): Test that a valid spec submission succeeds.
- test_spec_submit_missing_acceptance_criteria(): Test that spec submission fails when acceptance_criteria is missing.
- test_spec_submit_gate0_validation(): Test that Gate 0 validation is enforced.
- test_spec_submit_with_depends_on(): Test spec submission accepts dependsOn field (for future use).
- test_spec_submit_response_structure(): Test that the response has the expected structure.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
