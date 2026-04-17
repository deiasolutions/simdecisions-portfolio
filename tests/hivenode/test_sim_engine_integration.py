"""
test_sim_engine_integration
===========================

Integration tests for simulation engine wired into routes.

Dependencies:
- import pytest
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
- simple_flow(): Simple PHASE-IR flow for testing.
- flow_with_resources(): PHASE-IR flow with resources.
- test_load_flow_returns_200_and_run_id(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/load with valid PHASE-IR flow returns 200 + run_id.
- test_load_flow_creates_engine_context(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/load creates engine context in _engines dict.
- test_load_flow_creates_ledger_adapter(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/load creates ledger adapter.
- test_start_sim_returns_200(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/start returns 200 + status.
- test_pause_sim_returns_200(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/pause returns 200 + status=paused.
- test_resume_sim_returns_200(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/resume returns 200 + status=running.
- test_step_sim_advances_time(client, ledger_writer, ledger_reader, simple_flow): Test POST /sim/step advances sim_time.
- test_get_status_returns_current_state(client, ledger_writer, ledger_reader, simple_flow): Test GET /sim/status returns current status + sim_time.
- test_get_tokens_returns_list(client, ledger_writer, ledger_reader, simple_flow): Test GET /sim/tokens returns list of tokens.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
