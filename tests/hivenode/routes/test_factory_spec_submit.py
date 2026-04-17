"""
test_factory_spec_submit
========================

Tests for /factory/spec-submit endpoint.

Validates that generated specs pass Gate 0 validation.

Dependencies:
- import json
- import sys
- from pathlib import Path
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from gate0 import validate_spec
- from spec_parser import parse_spec

Functions:
- client(): FastAPI test client.
- backlog_dir(tmp_path): Create temporary backlog directory.
- mock_backlog_dir(monkeypatch, backlog_dir): Mock BACKLOG_DIR to use tmp_path.
- test_spec_submit_valid_request(client, mock_backlog_dir): Test spec submission with valid acceptance criteria passes Gate 0.
- test_spec_submit_missing_criteria_returns_422(client, mock_backlog_dir): Test spec submission without acceptance criteria returns 422.
- test_spec_submit_empty_criteria_returns_422(client, mock_backlog_dir): Test spec submission with empty acceptance criteria returns 422.
- test_generated_spec_has_all_gate0_sections(client, mock_backlog_dir): Test generated spec includes all Gate 0 required sections.
- test_generated_spec_passes_gate0_programmatically(client, mock_backlog_dir): Test generated spec passes Gate 0 validation before being written.
- test_spec_submit_with_dependencies(client, mock_backlog_dir): Test spec submission with dependencies generates correct Depends On section.
- test_spec_submit_validates_before_writing(client, mock_backlog_dir): Test that Gate 0 validation runs before spec is written to disk.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
