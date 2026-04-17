"""
test_build_pipeline_counts
==========================

Tests for /build/pipeline-counts endpoint.

Dependencies:
- import json
- from pathlib import Path
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.routes.build_monitor import router, _detect_task_type

Functions:
- client(): Create FastAPI test client.
- mock_queue_dir(tmp_path: Path): Create mock queue directory structure with test specs.
- test_detect_task_type_test(): Test detection of test tasks.
- test_detect_task_type_verify(): Test detection of verify tasks.
- test_detect_task_type_doc(): Test detection of doc tasks.
- test_detect_task_type_css(): Test detection of CSS tasks.
- test_detect_task_type_code(): Test default code detection.
- test_pipeline_counts_endpoint_structure(client, mock_queue_dir, monkeypatch): Test that endpoint returns correct structure.
- test_pipeline_counts_correct_counts(client, mock_queue_dir, monkeypatch): Test that counts are correct for each stage.
- test_pipeline_counts_type_breakdown(client, mock_queue_dir, monkeypatch): Test that type breakdown is correct.
- test_pipeline_counts_empty_dirs(client, tmp_path, monkeypatch): Test endpoint with empty queue directories.
- test_pipeline_counts_missing_dirs(client, tmp_path, monkeypatch): Test endpoint when queue directories don't exist.
- test_pipeline_counts_skip_patterns(client, mock_queue_dir, monkeypatch): Test that skip patterns are correctly ignored.
- test_pipeline_counts_json_format(client, mock_queue_dir, monkeypatch): Test that response is valid JSON.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
