"""
test_sim_routes
===============

Tests for simulation API routes.

Dependencies:
- import pytest
- from unittest.mock import MagicMock
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from hivenode import dependencies
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.ledger.reader import LedgerReader

Functions:
- client(): Create test client.
- ledger_db(tmp_path): Create temporary ledger database.
- ledger_writer(ledger_db): Create ledger writer with thread-safe connection.
- ledger_reader(ledger_db, ledger_writer): Create ledger reader with same thread-safe connection.
- mock_engine(): Create mock simulation engine.
- test_load_flow_with_engine(client, ledger_writer, ledger_reader): Test that /sim/load now returns 200 with engine integrated.
- test_load_flow_creates_run_id(client, ledger_writer, ledger_reader): Test loading a flow creates run_id.
- test_start_sim(client, ledger_writer, ledger_reader): Test starting a simulation.
- test_get_status_404_invalid_run_id(client, ledger_writer, ledger_reader): Test GET /sim/status with invalid run_id returns 404.
- test_pause_sim_404_invalid_run_id(client, ledger_writer, ledger_reader): Test POST /sim/pause with invalid run_id returns 404.
- test_inject_token_404_invalid_run_id(client, ledger_writer, ledger_reader): Test POST /sim/inject with invalid run_id returns 404.
- test_get_tokens_404_invalid_run_id(client, ledger_writer, ledger_reader): Test GET /sim/tokens with invalid run_id returns 404.
- test_get_resources_404_invalid_run_id(client, ledger_writer, ledger_reader): Test GET /sim/resources with invalid run_id returns 404.
- test_get_statistics_404_invalid_run_id(client, ledger_writer, ledger_reader): Test GET /sim/statistics with invalid run_id returns 404.
- test_get_events_empty_for_nonexistent_run(client, ledger_writer, ledger_reader): Test GET /sim/events returns empty list for non-existent run_id.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
